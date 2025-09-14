import os

from .patient_wrapper import PatientWrapper
from .static_io import InputPatients
from .week import Week


class Controller:
    def __init__(self) -> None:
        self.config_path = os.path.join("manager", "config")

        self.week = Week(os.path.join(self.config_path, "hours.json"))
        print(f"Loaded {len(self.week.hours)} hours from config")
        self.patient_wrapper = PatientWrapper(os.path.join(self.config_path, "patients.json"))
        self.patient_wrapper = PatientWrapper(os.path.join(self.config_path, "patients.json"))
        self.patient_data = InputPatients.get_data(os.path.join(self.config_path, "patients.json"))
        print(f"Loaded {len(self.patient_wrapper.patients)} patients from config")
        print(f"Loaded {len(self.patient_wrapper.patients)} patients from config")
        
    def solve_define_answers(self) -> None:
        """
        It checks every hour if an hour is only occupied by one person
        :return: None
        """
        changes = False
        for hour in self.week.hours:
            patient_index = None
            patient_ref = None
            for index, patient in enumerate(self.patient_wrapper.patients):
                if hour.ID in patient.pos_times:
                    if patient_index is None:
                        patient_index = index
                        patient_ref = patient
                    else:
                        print(f"Hour {hour.ID} is taken 2 or more times")
                        break
            else:
                if patient_ref is not None:
                    print(f"Patient {patient_ref.name} has hour {hour.ID}")
                    hour.taken_by = patient_ref
                    self.patient_wrapper.patients.remove(patient_ref)
                    changes = True

        return self.solve_define_answers() if changes else None
    
    def solve_recursive(self) -> list[Week]:
        """Wrapper to call self.__solve_recursive"""
        return self.__solve_recursive(self.patient_wrapper, self.week)
    
    def __solve_recursive(self, pw:PatientWrapper, week:Week, start=0) -> list[Week,]:
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
        solutions = []
        for hour_index, hour in enumerate(week.hours):
            if hour_index < start or hour.taken_by is not None: continue
            for patient_index, patient in enumerate(pw.patients):
                if hour.ID in patient.pos_times:
                    new_week = week.copy()
                    new_week.hours[hour_index].taken_by = patient
                    new_pw = pw.copy()
                    new_pw.patients.pop(patient_index)
                    solutions += self.__solve_recursive(new_pw, new_week, start=hour_index)
                    new_pw = pw.copy()
                    new_pw.patients.pop(patient_index)
                    solutions += self.__solve_recursive(new_pw, new_week, start=hour_index)

        return solutions