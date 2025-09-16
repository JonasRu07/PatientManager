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
        return self.__define_answers(self.patient_manager.get_patients_inside_wrapper().copy().patients, self.week.copy(), max_iterations)
            
        
    def __define_answers(self, remaining_patients:list[Patient,], week:Week, max_iterations) -> Week:
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
        return self.__all_solutions(self.patient_manager.get_patients_inside_wrapper().copy(), self.week.copy())
    
    def __all_solutions(self, pw:PatientWrapper, week:Week, start=0) -> list[Week]:
        """
        Recursively generates all possible solutions to the calender and return them
        :param pw: PatientWrapper
        :param week: Week
        :param start : int [optional] Not needed for starting. Helps to cut out hours, which has been tested and
                                      generated before
        :return: list[Week,] Empty if no solution has been found. Each week is completely deep copied, incl. content
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