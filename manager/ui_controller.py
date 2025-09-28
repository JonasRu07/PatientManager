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
        self.base_controller.solve_evolution()
        self.main_ui.load_hours(self.base_controller.week.hours)

    # UI-Calls
    def handle_call_add_patient(self, name:str, pos_hours:list[int,]) -> bool:
        raise NotImplementedError
    
    def handle_call_confirm_edit_patient(self, patient:Patient, name:str, pos_hours:list[int]) -> bool:
        raise NotImplementedError
        
    def handle_call_delete_patient(self, patient:Patient) -> None:
        raise NotImplementedError
              
    # Handle UI-Changes 
    def handle_patient_manager_ui(self) -> None:
        self.main_ui.load_frame("Manager")
        self.main_ui.load_patients(self.base_controller.patient_manager.patients)
        
    def handle_add_patient_ui(self) -> None:
        raise NotADirectoryError    
    
    def start(self) -> None:    
        self.main_ui.load_hours(self.base_controller.week.hours)
        self.main_ui.start()
        
    def terminate(self) -> None:
        print('Terminating the process')
        self.main_ui.destroy()