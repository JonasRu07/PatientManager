from .patient import Patient
from .patient_manager import PatientManager
from .patient_wrapper import PatientWrapper
from .week import Week
from .hour import Hour

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