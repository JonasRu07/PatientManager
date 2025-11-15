import time

from .ui import MainUI
from .patient import Patient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller


class UIController:
    def __init__(self, controller:'Controller') -> None:
            
        self.base_controller = controller
        
        self.main_ui = MainUI(self)
        
    # Solution functions
    def handle_solve_define(self) -> None:
        self.base_controller.solve_define_answers()
        self.main_ui.load_hours(self.base_controller.week.hours)
        
    def handle_solve_recursive(self) -> None:
        solutions = self.base_controller.solve_recursive_all()
        if len(solutions) == 0:
            print('No solutions found')
            return
        else:
            print(f'Found {len(solutions)} Solutions. Taking the First one')
            self.main_ui.load_hours(solutions[0].hours)
            
    def handle_solve_evolution(self) -> None:
        self.main_ui.show_calc_frame()
        self.main_ui.deactivate()
        self.main_ui.root.update() # Tkinter is stupid
        self.base_controller.solve_evolution()
        solution_finder = self.base_controller.find_solution.evo_thread
        max_gen = solution_finder.max_gen
        while solution_finder.is_alive():
            current_gen = solution_finder.current_gen
            self.main_ui.progress_bar(current_gen / max_gen)
            self.main_ui.root.update() # Tkinter is stupid
            if solution_finder.done:
                solution_finder.stop()
                time.sleep(0.05)
        self.main_ui.activate()
        self.main_ui.hide_calc_frame()
        self.main_ui.load_hours(self.base_controller.week.hours)


    # UI-Calls
    def handle_call_confirm_edit_patient(self, patient:Patient, name:str, pos_hours:list[int]) -> None:
        # Name should not be empty and only chars and spaces
        if name == '': return 
        for split in name.split(' '):
            if not split.isalpha():
                return
        new_patient = Patient(name, pos_hours)
        if patient.name == '':
            self.base_controller.add_patient(new_patient)
        else:
            self.base_controller.edit_patient(patient, new_patient)
        self.main_ui.load_frame("Manager")
        self.main_ui.load_patients(self.base_controller.patient_manager.get_patients_inside_wrapper().patients)
        
    def handle_call_delete_patient(self, patient_idx:int) -> None:
        patient = self.base_controller.patient_manager.patients[patient_idx]
        self.base_controller.delete_patient(patient)
        self.main_ui.load_patients(self.base_controller.patient_manager.get_patients_inside_wrapper().patients)
              
    # Handle UI-Changes 
    def handle_patient_manager_ui(self) -> None:
        self.main_ui.load_frame("Manager")
        self.main_ui.load_patients(self.base_controller.patient_manager.get_patients_inside_wrapper().patients)
        
    def handle_add_patient_ui(self) -> None:
        self.main_ui.load_frame("EditPatient")
        
    def handle_edit_patient_ui(self, index:int) -> None:
        patient = self.base_controller.patient_manager.patients[index]
        self.main_ui.load_frame("EditPatient")
        self.main_ui.load_patient(patient)
    
    def start(self) -> None:    
        self.main_ui.load_hours(self.base_controller.week.hours)
        self.main_ui.load()
        
    def terminate(self) -> None:
        print('Terminating the process')
        self.main_ui.destroy()