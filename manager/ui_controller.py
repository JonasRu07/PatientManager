
from .gui import MainGUI, AddPatientGUI, PatientManagerUI
from .patient import Patient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller


class UIController:
    def __init__(self, controller:'Controller') -> None:
            
        self.base_controller = controller
        
        self.main_ui = MainGUI(self)
        
    def handle_solve_define(self) -> None:
        self.base_controller.solve_define_answers()
        self.main_ui.load_hours(self.base_controller.week.hours)
        
    def handle_solve_recursive(self) -> None:
        solutions = self.base_controller.solve_recursive()
        if len(solutions) == 0:
            print('No solutions found')
            return
        else:
            print(f'Found {len(solutions)} Solutions. Taking the First one')
            self.main_ui.load_hours(solutions[0].hours)
            
    def handle_call_add_patient(self, name:str, pos_hours:list[int,]) -> bool:
        for char in name:
            if not (char.isalnum() or char == ' '):
                return False
        self.base_controller.add_patient(Patient(name, pos_times=pos_hours))
        return True
        
    # def handle_call_delete_patient(self, ui:PatientManagerUI, patient:Patient) -> None:
    def handle_call_delete_patient(self, ui, patient:Patient) -> None:
        self.base_controller.delete_patient(patient)
        ui.load_patients(self.base_controller.patient_manager.patients)
    
    def start(self) -> None:    
        self.main_ui.load_hours(self.base_controller.week.hours)
        
        self.main_ui.start()
        
    def handle_ui_add_patient(self) -> None:
        add_patient_ui = AddPatientGUI(self,
                                       self.main_ui.root,
                                       self.base_controller.week.copy())
        add_patient_ui.start()
        del add_patient_ui
        
    def handle_patient_manager_ui(self) -> None:
        ui = PatientManagerUI(self, self.main_ui.root)
        ui.load_patients(self.base_controller.patient_manager.patients)
        ui.start()
        
    def terminate(self) -> None:
        print('Terminating the process')
        self.main_ui.destroy()