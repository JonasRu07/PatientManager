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
    
    def edit_patient(self, old_patient:Patient, new_patient:Patient) -> None:
        if old_patient.name == '':
            self.add_patient(new_patient)
        else:
            self.patient_manager.delete_patient(old_patient)
            self.patient_manager.add_patient(new_patient)
        
    def solve_define_answers(self) -> None:
        self.week = self.find_solution.define_answers()
    
    def solve_recursive_all(self) -> list[Week]:
        return self.find_solution.all_solutions()
    
    def solve_recursive_first(self) -> None:
        self.week = self.find_solution.all_solutions()[0]
        
    def solve_evolution(self):
        self.find_solution.evo_solution(self)
    
    def close(self) -> None:
        print('Closing a controller instance')
        InputPatients.save(self.patient_manager.patients)