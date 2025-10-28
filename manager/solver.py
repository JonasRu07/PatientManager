import copy
import time
import threading
import random as rnd

from .patient import Patient
from .patient_manager import PatientManager
from .patient_wrapper import PatientWrapper
from .static_io import ConstEvoParams, EvoParameters
from .utils import total_size
from .week import Week
from .hour import Hour

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller

class EvoThread(threading.Thread):
    def __init__(self,
                 pm:PatientManager,
                 week:Week,
                 controller:'Controller'):
        
        super().__init__()
        self.patient_manager = pm
        self.week = week
        self.controller = controller
        self.solution = None
        
        self.params = ConstEvoParams.load()
        # Each patient can be seen as one gen
        # Prevent zero division
        self.gens = max(len(self.patient_manager.patients), 1)
        self.gen_size = int(self.params["sample_size"] / self.gens)
        
        self.max_gen = self.get_max_paths()
        self.current_gen = 0

        self.done = False
        self._stop_event = threading.Event()
        
    def run(self) -> None:
            
        solution_path = SolutionPath(self.patient_manager.get_patients_inside_wrapper().copy(),
                                     self.week.copy(),
                                     self.params)
        
        current_path = []
        current_path_evaluation = float("-inf")
        best_path = []
        best_path_evaluation = float("-inf")
        
        hash_map_counter = 0
        
        # Base line
        T1 = time.perf_counter_ns()
        for _ in range(self.gen_size):
            self.current_gen += 1
            current_path = solution_path.gen_path()
            current_path_evaluation = solution_path.evaluate(current_path)
            if best_path_evaluation < current_path_evaluation:
                best_path_evaluation = current_path_evaluation
                best_path = current_path
                
        
        for progress in range(self.gens):
            gen_path = best_path
            for __ in range(self.gen_size):
                self.current_gen += 1
                current_path = solution_path.gen_path_option(gen_path, progress)
                if (frozenset(current_path)) not in solution_path.exp_paths:
                    current_path_evaluation = solution_path.evaluate(current_path)
                    if best_path_evaluation < current_path_evaluation:
                        best_path_evaluation = current_path_evaluation
                        best_path = current_path
                    solution_path.exp_paths[(frozenset(current_path))] = current_path_evaluation
                else:
                    hash_map_counter += 1
                    
        T2 = time.perf_counter_ns()
                
        print(f"Calculation time: {(T2-T1)/10**9:.2f} seconds. \n"
                + f"{(T2-T1)/(self.current_gen*10**3):.3f} microseconds per path")
        
        print(f"Found hashes: {hash_map_counter}")
        
        print(f"Size of hashmap: {total_size(solution_path.exp_paths)/1_000_000} Mb")
        
        print(f"Solution with {len(best_path)} out of {len(self.patient_manager.patients)} patients "
                + f"with an evaluation of {best_path_evaluation}")
        print(f"Explored a total of {self.current_gen} Paths.")
        
        self.solution = solution_path.get_week(best_path, self.week.copy())

        self.done = True
        while not self._stop_event.is_set():
            time.sleep(0.05)
            
        self.controller.week = self.solution
        
    def get_max_paths(self) -> int:
        return self.gen_size + self.gens*self.gen_size
        
    def stop(self):
        self._stop_event.set()
        
class Solver:
    def __init__(self, patient_manager:PatientManager, week:Week) -> None:
        self.patient_manager = patient_manager
        self.week = week
        
    def define_answers(self, max_iterations:int=-1) -> Week:
        """
        This function tries to find every hour, which can only be taken
        up by one patient and assigns this patient to the hour. If more
        than one patient has the hour as possible, no one will be 
        assigned to to the hour.

        Args:
            max_iterations (int, optional): Optional limit on attempts 
            to find a solution. Every negative number and 0 are 
            interpreted as no limit, meaning the function will as long
            as it can find new hours with only on patient. Defaults to -1.

        Returns:
            Week: the solution found
        """
        return self.__define_answers(
            self.patient_manager.get_patients_inside_wrapper().copy().patients,
            self.week.copy(),
            max_iterations)
            
    def __define_answers(self, remaining_patients:list[Patient,],
                         week:Week,
                         max_iterations=-1) -> Week:
        """
        Internal function for handling the logic of the 
        self.define_solution function

        Args:
            remaining_patients (list[Patient,]): a list with all 
                patients to assign hours
            week (Week): all available hours
            max_iterations (int):
            max_iterations (int, optional): Optional limit on attempts 
                to find a solution. Every negative number and 0 are 
                interpreted as no limit, meaning the function will as 
                long as it can find new hours with only on patient. 
                Defaults to -1. 

        Returns:
            Week: Found solution 
        """
        if max_iterations == 0:
            return week
        
        changes = False
        for hour in week.hours:
            patient_ref = None
            for patient in remaining_patients:
                if hour.ID in patient.pos_times:
                    if patient_ref is None:
                        patient_ref = patient
                    else:
                        print(f"Hour {hour.ID} is taken 2 or more times")
                        break
            else:
                if patient_ref is not None:
                    print(f"Patient {patient_ref.name} has hour {hour.ID}")
                    hour.taken_by = patient_ref
                    remaining_patients.remove(patient_ref)
        
        return self.__define_answers(remaining_patients, week, max_iterations-1) if changes else week
    
    def all_solutions(self) -> list[Week]:
        """
        This function finds all solution. That's mean every patient
        has an hour assigned to it.

        Returns:
            list[Week]: Every solution found. Empty list if no solution
                found
        """
        return self.__all_solutions(self.patient_manager.get_patients_inside_wrapper().copy(), self.week.copy())
    
    def __all_solutions(self, pw:PatientWrapper, week:Week, start=0) -> list[Week]:
        """
        Internal function for handling the logic of the 
        self.__all_solution function

        Returns:
            list[Week]: Every solution found. Empty list if no solution
                found
        """
        if len(pw.patients) == 0:
            return [week]
        solutions:list[Week] = []
        for hour_index, hour in enumerate(week.hours):
            if hour_index < start or hour.taken_by is not None: continue
            for patient_index, patient in enumerate(pw.patients):
                if hour.ID in patient.pos_times:
                    new_week = week.copy()
                    new_week.hours[hour_index].taken_by = patient
                    new_pw = pw.copy()
                    new_pw.patients.pop(patient_index)
                    solutions += self.__all_solutions(new_pw, new_week, start=hour_index)
                    new_pw = pw.copy()
                    new_pw.patients.pop(patient_index)
                    solutions += self.__all_solutions(new_pw, new_week, start=hour_index)

        return solutions
    
    def evo_solution(self, controller:'Controller'):
        """
        Finds a "good" solution by creating different solutions and 
        evaluating it, based on the evaluation it creates abbreviations.
        It takes a special thread to run the calculations. After the 
        calculations the solution will be asserted to the week of the 
        given controller.
        Args:
            controller (Controller): Solution will be be asserted to 
                the week argument
        """
        self.evo_thread = EvoThread(
            self.patient_manager,
            self.week,
            controller)
        self.evo_thread.start()
    
class SolutionPath:
    def __init__(self,
                 pw:PatientWrapper,
                 week:Week,
                 params:EvoParameters) -> None:
        self.patient_wrapper = pw.copy()
        self.week = week.copy()
        self.exp_paths = {}
        self.params = params
            
    def gen_path(self): # ~28.005 micro/path
        path:list[tuple[int, int]] = []
        patients_idx = [i for i in range(len(self.patient_wrapper.patients))]
        hours_taken = {} # Dict for faster look up times
        rnd.shuffle(patients_idx)
        for patient_idx in patients_idx:
            pos_times = self.patient_wrapper.patients[patient_idx].pos_times
            hours_idx = [i for i in range(len(pos_times))]
            rnd.shuffle(hours_idx)
            for hour_idx in hours_idx:
                if pos_times[hour_idx] not in hours_taken:
                    hours_taken[pos_times[hour_idx]] = True
                    path.append((patient_idx, hour_idx))
                    break
        return path
        
    def gen_path_option(self,
                        path:list[tuple[int, int]],
                        start:int) -> list[tuple[int, int]]:
        path = path[:start]
        patients_idx = [i for i in range(len(self.patient_wrapper.patients))]
        hours_taken = {} # Dict for faster look up times
        
        for combo in path:
            patients_idx.remove(combo[0])
            hours_taken[combo[1]] = True
        
        rnd.shuffle(patients_idx)
        for patient_idx in patients_idx:
            pos_times = self.patient_wrapper.patients[patient_idx].pos_times
            hours_idx = [i for i in range(len(pos_times))]
            rnd.shuffle(hours_idx)
            for hour_idx in hours_idx:
                if pos_times[hour_idx] not in hours_taken:
                    hours_taken[pos_times[hour_idx]] = True
                    path.append((patient_idx, hour_idx))
                    break
        return path
    
    def evaluate(self, path:list[tuple[int, int]]) -> float:
        evaluation = 0
        # Constants:
        # The higher absolute number is, the more important is the 
        # condition. But is also highly influenced by the absolute
        # occurrence of the event. Ex: there may be 40 patients which
        # each have a multiplier of 10, but the time_limit condition 
        # can only be triggered 5 times. So the time limit has less 
        # of an effect than the number of patients even if the value
        # is absolute bigger
        NUMBER_PATIENTS = 10
        CONSECUTIVE_HOURS = 2.5
        TIME_LIMIT = -10
        
        
        # The more patients the better
        evaluation += len(path) * NUMBER_PATIENTS
        # Try to clamp the patients together
        days = [[], [], [], [], []]
        for combo in path:
            patient = self.patient_wrapper.patients[combo[0]]
            hour_id = patient.pos_times[combo[1]]
            days[hour_id >> 4].append(hour_id)
        consecutive_hours = 0
        for day in days:
            current_id = -2
            for hour_id in day:
                if hour_id - 1 == current_id:
                    consecutive_hours += 1
                current_id = hour_id
                
        evaluation += consecutive_hours * CONSECUTIVE_HOURS
        
        # I dont't want to work for more than 8 hours a day
        bad_days = 0
        for day in days:
            if len(day) > 0:
                day.sort()
                if day[-1] - day[0] > 8:
                    bad_days += 1
        evaluation += bad_days*TIME_LIMIT
        
        return evaluation
        
    def get_week(self, path:list[tuple[int, int]], week:Week) -> Week:
        for combo in path:
            patient = self.patient_wrapper.patients[combo[0]]
            for hour in week.hours:
                if hour.ID == patient.pos_times[combo[1]]:
                    hour.taken_by = patient
                    break
        return week
