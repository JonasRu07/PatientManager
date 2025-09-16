import os

from .patient_wrapper import PatientWrapper
from .patient_manager import PatientManager
from .patient import Patient
from .solver import Solver
from .static_io import InputPatients
from .week import Week


class Controller:
    def __init__(self) -> None:
        self.config_path = os.path.join("manager", "config")

        self.week = Week(os.path.join(self.config_path, "hours.json"))
        print(f"Loaded {len(self.week.hours)} hours from config")
        self.patient_manager = PatientManager()
        print(f"Loaded {len(self.patient_manager.patients)} patients from config")
        
        self.find_solution = Solver(self.patient_manager, self.week)
        
    def add_patient(self, patient:Patient) -> None:
        self.patient_manager.add_patient(patient)
        
    def delete_patient(self, patient:Patient) -> bool:
        return self.patient_manager.delete_patient(patient)
        
    def solve_define_answers(self) -> None:
        self.week = self.find_solution.define_answers()
    
    def solve_recursive(self) -> list[Week]:
        """Wrapper to call self.__solve_recursive"""
        return self.__solve_recursive(self.patient_manager.get_patients_inside_wrapper(), self.week)
    
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
    
    def close(self) -> None:
        print('Closing a controller instance')
        InputPatients.save(self.patient_manager.patients)