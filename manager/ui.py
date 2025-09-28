import tkinter as tk
import tkinter.ttk as ttk
from typing import TypedDict, Literal

from .hour import Hour
from .patient import Patient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui_controller import UIController

class UITypes:
    Days = list[str]
    Times = list[str]
    __DayConst = TypedDict(
        "__DayConst",
        {
            "width" : int,
            "height" : int
        }
    )
    __TimeConst = TypedDict(
        "__TimeConst",
        {
            "width" : int,
            "height" : int,
            "px_per_hour" : int
        }
    )
    PosConstants = TypedDict(
        "PosConstants",
        {
            "Day" : __DayConst,
            "Time" : __TimeConst
        }
    )
    __DayPos = TypedDict(
        "__DayPos",
        {
            "Monday" : tuple[int, int],
            "Tuesday" : tuple[int, int],
            "Wednesday" : tuple[int, int],
            "Thursday" : tuple[int, int],
            "Friday" : tuple[int, int]
        }
    )
    __TimePos = TypedDict(
        "__TimePos",
        {
            "0700" : tuple[int, int],
            "0800" : tuple[int, int],
            "0900" : tuple[int, int],
            "1000" : tuple[int, int],
            "1100" : tuple[int, int],
            "1200" : tuple[int, int],
            "1300" : tuple[int, int],
            "1400" : tuple[int, int],
            "1500" : tuple[int, int],
            "1600" : tuple[int, int],
            "1700" : tuple[int, int],
            "1800" : tuple[int, int],
            "1900" : tuple[int, int],
        }
    )
    Positions = TypedDict(
        "Positions",
        {
            "Day" : __DayPos,
            "Time" : __TimePos
        })
    States = Literal["Main", "Manager"]
    Frames = TypedDict(
        "Frames",
        {
            "Main" : 'FrameMainWindow',
            "Manager" : 'FrameMainManager'
        }
    )

class MainUI:
    def __init__(self, controller:'UIController') -> None:
        self.controller = controller
        
        self.hours = []
        self.patients = []
        
        # Window:
        self.root = tk.Tk()
        self.root.title("Patient Manager UI")
        self.root.geometry("1250x620")
        self.root.configure(background="#1F1F1F")
        self.root.bind("<Escape>", lambda event: self.close())
        
        # States
        self.current_state:UITypes.States = "Main"
        self.frames:UITypes.Frames = {
            "Main" : FrameMainWindow(self.controller, self.root),
            "Manager" : FrameMainManager(self.controller, self.root)
        }
        
    def load_hours(self, hours:list[Hour,]|None=None):
        """
        Load the given hours into the current UI
        """
        if hours is not None:
            self.hours = hours
        if hasattr(self.frames[self.current_state], "load_hours"):
            self.frames[self.current_state].load_hours(self.hours) # type: ignore
            
    def load_patients(self, patients:list[Patient,]|None=None):
        """
        Load the given patients into the current UI
        """
        if patients is not None:
            self.patients = patients
        if hasattr(self.frames[self.current_state], "load_patients"):
            self.frames[self.current_state].load_patients(self.patients) # type: ignore
            
    def load_frame(self, frame:UITypes.States) -> None:
        self.frames[self.current_state].hide()
        self.current_state = frame
        self.frames[self.current_state].load()
        
    
    def start(self):
        """
        Start of the internal logic of the UI
        """
        self.frames[self.current_state].load()
        self.root.mainloop()
        
    def close(self):
        """
        Closes all windows down the hierarchy
        """
        if self.current_state == "Main":
            self.destroy()
        elif self.current_state == "Manager":
            self.current_state = "Main"
            self.frames["Manager"].hide()
            self.frames["Main"].load()
        
    def destroy(self):
        """
        Close all windows
        """
        self.root.destroy()
        
class FrameMainWindow:
    def __init__(self, controller:'UIController', root_window:tk.Tk) -> None:
        self.controller = controller
        self.root = root_window
        
        # Constants
        # TODO: They can be moved into a config file to allow better 
        # change but who cares, it's UI ;)
        self.DAYS:UITypes.Days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
        self.TIMES:UITypes.Times = [
            "0700",
            "0800",
            "0900",
            "1000",
            "1100",
            "1200",
            "1300",
            "1400",
            "1500",
            "1600",
            "1700",
            "1800",
            "1900"
        ]
        self.POS_CONSTANTS:UITypes.PosConstants = \
            {
                "Day" : \
                    {
                        "width" : 160,
                        "height" : 40
                    },
                "Time" : \
                    {
                        "width" : 80,
                        "height" : 30,
                        "px_per_hour" : 40
                    }
            }
        self.POSITIONS:UITypes.Positions = {
            "Day" : {
                
                "Monday" : (20 + self.POS_CONSTANTS["Time"]["width"] + 20,
                            20),
                "Tuesday" : (20 + self.POS_CONSTANTS["Time"]["width"] + 20 + self.POS_CONSTANTS["Day"]["width"]+20,
                             20),
                "Wednesday" : (20 + self.POS_CONSTANTS["Time"]["width"] + 20 + (self.POS_CONSTANTS["Day"]["width"]+20)*2,
                               20),
                "Thursday" : (20 + self.POS_CONSTANTS["Time"]["width"] + 20 + (self.POS_CONSTANTS["Day"]["width"]+20)*3,
                              20),
                "Friday" : (20 + self.POS_CONSTANTS["Time"]["width"] + 20 + (self.POS_CONSTANTS["Day"]["width"]+20)*4,
                            20)
            },
            "Time" : {
                "0700" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20),
                "0800" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + self.POS_CONSTANTS["Time"]["height"]+10),
                "0900" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*2),
                "1000" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*3),
                "1100" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*4),
                "1200" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*5),
                "1300" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*6),
                "1400" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*7),
                "1500" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*8),
                "1600" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*9),
                "1700" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*10),
                "1800" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*11),
                "1900" : (20,
                          20 + self.POS_CONSTANTS["Day"]["height"] + 20 + (self.POS_CONSTANTS["Time"]["height"]+10)*12),
            }
        }
        # Tkinter has some dodgy behavior so force update
        self.root.update()
        
        # Main Frame
        self.main = tk.Frame(master=self.root,
                             background="#1F1F1F",
                             width=self.root.winfo_width(),
                             height=self.root.winfo_height())
        
        # Frame Time
        width = 20 + self.POS_CONSTANTS["Time"]["width"] + 20 + 5*(self.POS_CONSTANTS["Day"]["width"] + 20)
        height =20 + self.POS_CONSTANTS["Day"]["height"] + 20 + 13*(self.POS_CONSTANTS["Time"]["height"] + 10)
        self.f_time_table = tk.Frame(master=self.main,
                                     background='#333333',
                                     relief='ridge',
                                     border=2,
                                     cursor='arrow')
        self.f_time_table.place(x=10, y=10, width=width, height=height)
        
        # Labels Day
        self.ls_day : list[tk.Label] = []
        for day in self.DAYS:
            self.ls_day.append(tk.Label(master=self.f_time_table,
                                        background="#11515C",
                                        foreground='#F0F0F0',
                                        font='Aral, 18',
                                        text=day))
            self.ls_day[-1].place(x=self.POSITIONS["Day"][day][0],
                                  y=self.POSITIONS["Day"][day][1],
                                  width=self.POS_CONSTANTS['Day']["width"],
                                  height=self.POS_CONSTANTS['Day']["height"])
        
        # Labels Time
        self.ls_time: list[tk.Label,] = []
        
        for time in self.TIMES:
            self.ls_time.append(tk.Label(master=self.f_time_table,
                                         background='#11515C',
                                         foreground='#F0F0F0',
                                         text=time[:2] + ':' + time[2:]))
            self.ls_time[-1].place(x=self.POSITIONS["Time"][time][0],
                                   y=self.POSITIONS["Time"][time][1],
                                   width=self.POS_CONSTANTS['Time']["width"],
                                   height=self.POS_CONSTANTS['Time']["height"])
        
        # Frame User Interaction
        self.f_interaction = tk.Frame(master=self.main,
                                     background='#333333',
                                     border=2,
                                     cursor='arrow',
                                     relief='ridge')
        self.f_interaction.place(x=10 + 20 + self.POS_CONSTANTS["Time"]["width"] 
                                   + 20 + 5*(self.POS_CONSTANTS["Day"]["width"] + 20) + 10,
                                 y=10,
                                 width=200,
                                 height=600)
        
        # Button Solve define
        self.b_solve_define = tk.Button(master=self.f_interaction,
                                        background='#11515C',
                                        foreground='#F0F0F0',
                                        text='Solve define \nanswers',
                                        command=self.call_solve_define)
        self.b_solve_define.place(x=20, y=20, width=160, height=50)
        
        # Button Solve recursive
        self.b_solve_define = tk.Button(master=self.f_interaction,
                                        background='#11515C',
                                        foreground='#F0F0F0',
                                        text='Find all \nanswers',
                                        command=self.call_solve_recursive)
        self.b_solve_define.place(x=20, y=80, width=160, height=50)
        
        # Button Solve Evolution
        self.b_solve_define = tk.Button(master=self.f_interaction,
                                        background='#11515C',
                                        foreground='#F0F0F0',
                                        text='Find evo \nanswers',
                                        command=self.call_solve_evolution)
        self.b_solve_define.place(x=20, y=140, width=160, height=50)
        
        # Button Patient manager
        self.b_patient_managing = tk.Button(master=self.f_interaction,
                                            background='#11515C',
                                            foreground='#F0F0F0',
                                            text='Manage patients',
                                            command=self.call_patient_managing)
        self.b_patient_managing.place(x=20, y=210, width=160, height=35)
        
    def call_patient_managing(self) -> None:
        self.controller.handle_patient_manager_ui()
        
    def call_solve_recursive(self) -> None:
        self.controller.handle_solve_recursive()
    
    def call_solve_define(self) -> None:
        self.controller.handle_solve_define()
        
    def call_solve_evolution(self) -> None:
        self.controller.handle_solve_evolution()
    
    def load_hours(self, hours:list[Hour, ]) -> None:
        
        self.ls_hours:list[tk.Label] = []
        
        for hour in hours:
            day_index = hour.ID >> 4
            day = self.DAYS[day_index]
            self.ls_hours.append(tk.Label(master =self.f_time_table,
                                          background='#424242',
                                          foreground='#F0F0F0',
                                          relief='ridge',
                                          text='' if hour.taken_by is None else hour.taken_by.name))
                                          #text=f'{hour.time} // {hour.duration}'))
            self.ls_hours[-1].place(x=self.POSITIONS["Day"][day][0],
                                    y=self.POSITIONS["Time"][hour.time[:2]+ '00'][1]
                                      +self.POS_CONSTANTS["Time"]["px_per_hour"]*int(hour.time[2:])/60,
                                    width=self.POS_CONSTANTS["Day"]["width"],
                                    height=self.POS_CONSTANTS["Time"]["px_per_hour"] * hour.duration / 60)
        
    def load(self,) -> None:
        print("Placing Main")
        self.main.place(x=0, y=0)
        
    def hide(self) -> None:
        self.main.place_forget()
        
class FrameMainManager:
    """
    Main Frame for the Manager "window" 
    """
    def __init__(self, controller:'UIController', root:tk.Tk) -> None:
        self.controller = controller
        self.root = root
        
        # Tkinter has some dodgy behavior so force update
        self.root.update()
        
        # Main Frame
        self.main = tk.Frame(master=self.root,
                             background="#1F1F1F",
                            #  background="red",
                             width=self.root.winfo_width(),
                             height=self.root.winfo_height())
        
        self.bs_patients:list[tk.Button] = []
        self.bs_deletion:list[tk.Button] = []

        self.window_height = self.root.winfo_height()
        self.f_patients_position = [10, 0, 320, self.root.winfo_height()]
        
        # List of all patients
        self.f_patients = tk.Frame(master=self.main,
                                   background='#2b2d30',
                                   border=2,
                                   relief='solid')
        self.f_patients.place(x=10,
                              y=0,
                              width=320,
                              height=self.root.winfo_height()-20)

        # Show options
        self.f_options = tk.Frame(master=self.main,
                                    background='#2b2d30',
                                    border=2,
                                    relief='solid')
        self.f_options.place(x=340, y=10, width=140, height=self.root.winfo_height()-20)
        
        self.b_new_patient = tk.Button(self.f_options,
                                       background='#11515C',
                                       foreground='#F0F0F0',
                                       text='New Patient',
                                       command=self.call_new_patient)
        self.b_new_patient.place(x=20, y=20, width=100, height=35)

    def call_new_patient(self):
        self.controller.handle_add_patient_ui()

    def scroll_ui(self, up:bool) -> None:
        delta = 10
        if up:
            if self.f_patients_position[1] + self.f_patients_position[3] - delta > self.window_height:
                self.f_patients_position[1] -= delta
            else:
                self.f_patients_position[1] = self.window_height - self.f_patients_position[3]
        else:
            if self.f_patients_position[1] > -delta -10:
                self.f_patients_position[1] = 0
            else:
                self.f_patients_position[1] += delta

        self.f_patients.place(x=self.f_patients_position[0],
                              y=self.f_patients_position[1],
                              width=self.f_patients_position[2],
                              height=self.f_patients_position[3])


    def load_patients(self, patients:list[Patient,]) -> None:
        print('Loading patients to show')
        self.patients = patients
        # Delete old labels
        for b_patient, b_delete in zip(self.bs_patients, self.bs_deletion):
            b_patient.destroy()
            b_delete.destroy()
        self.bs_patients = []
        self.bs_deletion = []
        
        
        count_patients = len(patients)
        self.f_patients_position[3] = max(count_patients*25 + 10, self.root.winfo_height())

        for index, patient in enumerate(patients):
            self.bs_patients.append(tk.Button(master=self.f_patients,
                                             background='#ACAB00',
                                             foreground='#000000',
                                             text=patient.name,
                                             command=lambda i=index : self.call_edit_patient(i)))
            self.bs_patients[-1].place(x=10, y=25*index+5, width=270, height=20)
            
            self.bs_deletion.append(tk.Button(master=self.f_patients,
                                              background="#C00812",
                                              foreground='#081505',
                                              text="X",
                                              command=lambda i=index : self.call_patient_deletion(i)))
            self.bs_deletion[-1].place(x=290, y=25*index+5, width=20, height=20)
            
    def call_patient_deletion(self, index:int) -> None:
        raise NotImplementedError
        self.controller.handle_call_delete_patient(self, self.patients[index])
    
    def call_edit_patient(self, index:int) -> None:
        raise NotImplementedError
        edit_ui = EditPatientUI(self.controller, self.root, self.patients[index], self.controller.base_controller.week)
        edit_ui.root.mainloop()

    def start(self) -> None:
        self.root.mainloop()
        
    def destroy(self) -> None:
        self.root.destroy()
        
    def load(self) -> None:
        self.root.bind("<Button-4>", lambda event:self.scroll_ui(up=False))
        self.root.bind("<Button-5>", lambda event:self.scroll_ui(up=True))
        self.main.place(x=0, y=0)
        
    def hide(self) -> None:
        self.main.place_forget()