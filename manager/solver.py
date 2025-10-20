import copy
import time
import threading
import random as rnd
from hashlib import sha256

from .patient import Patient
from .patient_manager import PatientManager
from .patient_wrapper import PatientWrapper
from .week import Week
from .hour import Hour

class EvoThread(threading.Thread):
    def __init__(self, pm:PatientManager, week:Week):
        super().__init__()
        self.patient_manager = pm
        self.week = week
        self.solution = None
        
        self.hash = {}
        
        self.generations_per_iter = 100
        # Too long. TODO: Do maths
        self.max_gen = self.generations_per_iter
        count_patients = len(self.patient_manager.patients)
        for depth in range(1, count_patients):
            options = int((count_patients-depth) * self.generations_per_iter)
            for i in range(options):
                self.max_gen += 1
                
        self.current_gen = 0
        
        self.done = False
        self.stop_event = threading.Event()
        
    def run(self):
        print("Thread is Running")
            
        T = time.time()
        solution_path = SolutionPath(self.patient_manager.get_patients_inside_wrapper().copy(),
                                     self.week.copy())
        
        current_path = []
        current_path_evaluation = float("-inf")
        best_path = []
        best_path_evaluation = float("-inf")
        
        # Generating a good baseline
        for i in range(self.generations_per_iter):
            self.current_gen += 1
            current_path = solution_path.gen_path()
            current_path_evaluation = solution_path.evaluate_path(current_path)
            if current_path_evaluation > best_path_evaluation:
                best_path_evaluation = current_path_evaluation
                best_path = current_path
        print('Baseline completed')

        # Evolving around the best path
        count_patients = len(self.patient_manager.patients)
        for depth in range(1, count_patients):
            options = int((count_patients-depth) * self.generations_per_iter)
            for i in range(options):
                self.current_gen += 1
                current_path = solution_path.gen_path_option(best_path, start=depth)
                current_path_evaluation = solution_path.evaluate_path(current_path)
                if current_path_evaluation > best_path_evaluation:
                    best_path_evaluation = current_path_evaluation
                    best_path = current_path
                    print(f"New best evaluation = {best_path_evaluation}")
                    
        print(f"Solution with {len(best_path)} out of {len(self.patient_manager.patients)} patients "
              + f"with an evaluation of {best_path_evaluation}")
        
        print(f"Calculation time: {time.time()-T:.2f} seconds. "
              + f"{(time.time()-T)*1_000_000/self.current_gen:.3f} microseconds per path")
        
        print(f"Explored a total of {self.current_gen} Paths.")
        
        self.solution = solution_path.get_week(best_path, self.week.copy())
        
        print("Done with calculating")
        self.done = True
        while not self.stop_event.is_set():
            time.sleep(0.05)
        
    def stop(self):
        self.stop_event.set()

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
    
    def evo_solution(self):
        # T = time.time()
        # solution_path = SolutionPath(self.patient_manager.get_patients_inside_wrapper().copy(),
        #                              self.week.copy())
        # # Pulling n umber out of my ass
        # gens_per_patient = 1000
        
        # current_path = []
        # current_path_evaluation = 0
        # best_path = []
        # best_path_evaluation = 0
        
        # exp_path = 0
        
        # # Generating a good baseline
        # for i in range(gens_per_patient):
        #     exp_path += 1
        #     current_path = solution_path.gen_path()
        #     current_path_evaluation = solution_path.evaluate_path(current_path)
        #     if current_path_evaluation > best_path_evaluation:
        #         best_path_evaluation = current_path_evaluation
        #         best_path = current_path

        # # Evolving around the best path
        # count_patients = len(self.patient_manager.patients)
        # for depth in range(1, count_patients):
        #     options = int((count_patients-depth)/count_patients * gens_per_patient)
        #     for i in range(options):
        #         exp_path += 1
        #         current_path = solution_path.gen_path_option(best_path, start=depth)
        #         current_path_evaluation = solution_path.evaluate_path(current_path)
        #         if current_path_evaluation > best_path_evaluation:
        #             best_path_evaluation = current_path_evaluation
        #             best_path = current_path
        #             print(f"New best evaluation = {best_path_evaluation}")
                    
        # print(f"Solution with {len(best_path)} out of {len(self.patient_manager.patients)} patients "
        #       + f"with an evaluation of {best_path_evaluation}")
        
        # print(f"Calculation time: {time.time()-T:.2f} seconds. "
        #       + f"{(time.time()-T)*1_000_000/exp_path:.3f} microseconds per path")
        
        # print(f"Explored a total of {exp_path} Paths.")
        # return solution_path.get_week(best_path, self.week.copy())
        
        self.evo_thread = EvoThread(self.patient_manager, self.week)
        print("Setup Thread complete")
        self.evo_thread.start()
        print("Run started")
    
class SolutionPath:
    def __init__(self,
                 pw:PatientWrapper,
                 week:Week) -> None:
        self.patient_wrapper = pw.copy()
        self.week = week.copy()
        
    def gen_path(self):
        path = []
        taken_hours = []
        
        patients_id = [i for i in range(len(self.patient_wrapper.patients))]
        rnd.shuffle(patients_id)
        for patient_id in patients_id:
            pos_hours = copy.deepcopy(self.patient_wrapper.patients[patient_id].pos_times)
            rnd.shuffle(pos_hours)
            for pos_hour in pos_hours:
                if pos_hour not in taken_hours:
                    taken_hours.append(pos_hour)
                    hour_index = self.patient_wrapper.patients[patient_id].pos_times.index(pos_hour)
                    break
            else:
                # All of the hours the patient can attend to already
                # have been taken
                continue
            path.append([patient_id, hour_index])
        return path
                
    def gen_path_option(self, path:list[list[int,]], start:int):
        path = path[:start]
        
        taken_hours = []
        patients = self.patient_wrapper.copy().patients
        ref_patients = self.patient_wrapper.copy().patients
        # Ignoring times and patients with place
        for combo in path[:start]:
            patient = self.patient_wrapper.patients[combo[0]]
            taken_hours.append(patient.pos_times[combo[1]])
            patients.remove(patient)
        
        rnd.shuffle(patients)
        for patient in patients:
            for p_index, ref_patient in enumerate(ref_patients):
                if ref_patient == patient:
                    break
            else:
                raise ValueError("Cannot find patient in ref_patients")
            pos_hours = copy.deepcopy(patient.pos_times)
            rnd.shuffle(pos_hours)
            for pos_hour in pos_hours:
                if pos_hour not in taken_hours:
                    taken_hours.append(pos_hour)
                    break
            else:
                # All of the hours the patient can attend to already
                # have been taken
                continue
            h_index = patient.pos_times.index(pos_hour)
            path.append([p_index, h_index])
        return path
    
    def evaluate_path(self, path:list[list[int,]]) -> float | int:
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
    
    def get_week(self, path:list[list[int,]], week:Week) -> Week:
        for combo in path:
            patient = self.patient_wrapper.patients[combo[0]]
            for hour in week.hours:
                if hour.ID == patient.pos_times[combo[1]]:
                    hour.taken_by = patient
                    break
        return week
