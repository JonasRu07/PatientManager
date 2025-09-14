
from .gui import MainGUI

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller


class UIController:
    def __init__(self, controller:'Controller') -> None:
            
        self.base_controller = controller
        
        self.main_ui = MainGUI(self)
        
    def handle_solve_define(self):
        self.base_controller.solve_define_answers()
        self.main_ui.load_hours(self.base_controller.week.hours)
        
    def handle_solve_recursive(self):
        solutions = self.base_controller.solve_recursive()
        if len(solutions) == 0:
            print('No solutions found')
            return
        else:
            print(f'Found {len(solutions)} Solutions. Taking the First one')
            self.main_ui.load_hours(solutions[0].hours)
        
    def start(self):    
        self.main_ui.load_hours(self.base_controller.week.hours)
        self.main_ui.start()
        
    def terminate(self):
        print('Terminating the process')
        self.main_ui.destroy()