"""
UI implementation for the application.
It is based on FOSS-library tkinter for the graphics part.

The connection to the UI-Controller is handled over the MainUI class.

Inside this file the word "window" may refer to either a own instance 
of a window (tk.Tk() / tk.Toplevel()), or, when used in quotation marks
it refers to a context. Those context are (mostly) independent from
each other. Those are for example the mainpage, and and editorial page.

Different "windows" are represented as different Frames, which are 
loaded and unloaded, dependent on the current selected window.

Each Frame inheritances from the BaseUI to ensure properly and 
consistent implementation of showing hand hiding methods for the Frame.

Each Frames has reference to the UI-Controller to handle User-Inputs
and a reference to the root window, to tell tkinter, where the Frame
is supposed to be placed.

A Frame also can have SubFrames. They should keep knowledge of the
UI-Controller and their parent.

Local Naming Convention:
    Classes that create their own proper Window (ex. via tk.Tk()) 
        should have a UI at the end
    Classes that represent a "window" should be prefixed with "Frame"
    Classes that are supporting frames for "windows" should be prefixed
        with SubFrame
    Functions that are called from he User-Input (Buttons, ...) should
        be prefixed with call_...

Raises:
    UIMissingMethod: load() from BaseFrame is not overwritten
    UIMissingMethod: hide() from BaseFrame is not overwritten

"""

import tkinter as tk
import tkinter.ttk as ttk
from typing import TypedDict, Literal

from .hour import Hour
from .week import Week
from .patient import Patient

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui_controller import UIController

class UIMissingMethod(Exception):
    def __init__(self, hint:str) -> None:
        super().__init__(hint)

class UITypes:
    """
    Class keeps track of more complex types inside the UI-file for 
    type hinting, within reasonable space use.
    """
    Days = list[str]
    Times = list[str]
    DayConst = TypedDict(
        "DayConst",
        {
            "width" : int,
            "height" : int
        }
    )
    TimeConst = TypedDict(
        "TimeConst",
        {
            "width" : int,
            "height" : int,
            "px_per_hour" : int
        }
    )
    PosConstants = TypedDict(
        "PosConstants",
        {
            "Day" : DayConst,
            "Time" : TimeConst
        }
    )
    DayPos = TypedDict(
        "DayPos",
        {
            "Monday" : tuple[int, int],
            "Tuesday" : tuple[int, int],
            "Wednesday" : tuple[int, int],
            "Thursday" : tuple[int, int],
            "Friday" : tuple[int, int]
        }
    )
    TimePos = TypedDict(
        "TimePos",
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
            "Day" : DayPos,
            "Time" : TimePos
        })
    States = Literal["Main", "Manager", "EditPatient"]
    Frames = TypedDict(
        "Frames",
        {
            "Main" : 'FrameMainWindow',
            "Manager" : 'FrameManager',
            "EditPatient" : 'FrameEditPatient'
        }
    )


class BaseFrame:
    """
    Minimum requirement for any frames used. To keep them consistent.
    """
    def __init__(self, con:'UIController', root_window:tk.Tk|tk.Frame):
        self.controller = con
        self.root = root_window
        
    def hide(self) -> None:
        raise UIMissingMethod("Missing function to hide UI")
    
    def load(self) -> None:
        raise UIMissingMethod("Missing function to load UI")
    
    def deactivate(self) -> None:
        """
        Deactivates the User Input for this frame
        """
        pass
    
    def activate(self) -> None:
        """
        Deactivates the User Input for this frame
        """
        pass
       
class MainUI:
    """
    Main proper window for the whole application.
    
    It keeps track of all frames, which may appear during the us of the
    app.
    
    If a new Frame... is added, add it in the frames dict and adjust 
    the closing hierarchy in the close method. Also update the UITypes.
    As it is the interaction point. It also has all loading functions, 
    as not all Frames support all loading functions, make sure only 
    frames, which support the function call be called.
    """
    def __init__(self, con:'UIController'):
        self.controller = con
        
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
            "Manager" : FrameManager(self.controller, self.root),
            "EditPatient" :FrameEditPatient(self.controller, self.root)
        }
    
    def progress_bar(self, progress:float):
        assert not progress < 0, "Progress cannot be smaller 0"
        assert not progress > 1, "Progress cannot exceed 1"
        if hasattr(self.frames[self.current_state], "set_progress"):
            self.frames[self.current_state].set_progress(progress) #type: ignore
        
    def load_hours(self, hours:list[Hour,]|None=None):
        """
        Load the given hours into the current UI. If the current Frame
        does not support it, it raises a RuntimeError
        """
        if hours is not None:
            self.hours = hours
        if hasattr(self.frames[self.current_state], "load_hours"):
            self.frames[self.current_state].load_hours(self.hours) # type: ignore
        else:
            raise RuntimeError(f"Current UI-Frame {self.current_state} has no method load_hours")
            
    def load_patients(self, patients:list[Patient,]|None=None):
        """
        Load the given patients into the current UI. If the current Frame
        does not support it, it raises a RuntimeError
        """
        if patients is not None:
            self.patients = patients
        if hasattr(self.frames[self.current_state], "load_patients"):
            self.frames[self.current_state].load_patients(self.patients) # type: ignore
        else:
            raise RuntimeError(f"Current UI-Frame {self.current_state} has no method load_patients")
            
    def load_patient(self, patient:Patient) -> None:
        """
        Load the given patients into the current UI. If the current Frame
        does not support it, it raises a RuntimeError
        """
        if hasattr(self.frames[self.current_state], "load_patient"):
            self.frames[self.current_state].load_patient(patient) # type: ignore
        else:
            raise RuntimeError(f"Current UI-Frame {self.current_state} has no method load_patient")
            
    def load_frame(self, frame:UITypes.States) -> None:
        """
        Load a new frame as a "window"
        """
        self.frames[self.current_state].hide()
        self.current_state = frame
        self.frames[self.current_state].load()
            
    def deactivate(self):
        self.frames[self.current_state].deactivate()
        
    def activate(self):
        self.frames[self.current_state].activate()
            
    def load(self):
        """
        Start of the internal logic of the UI
        """
        self.frames["Main"].load()
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
        elif self.current_state == "EditPatient":
            self.current_state = "Manager"
            self.frames["EditPatient"].hide()
            self.frames["Manager"].load()
        
    def destroy(self):
        """
        Close all windows
        """
        self.root.destroy()
        
    def show_calc_frame(self):
        self.frames[self.current_state].show_calc_frame() #type: ignore
        
    def hide_calc_frame(self):
        self.frames[self.current_state].hide_calc_frame() #type: ignore
        
class FrameMainWindow(BaseFrame):
    """
    Main "Window" Frame. 
    Starting page of the program

    Args:
        con(UIController) : Controller for UI handling
        root_window(tk.Tk) : parental window, in which it will be 
            placed in
    """
    def __init__(self, con:'UIController', root_window:tk.Tk):
        super().__init__(con, root_window)
                
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
        self.b_solve_recursive = tk.Button(master=self.f_interaction,
                                           background='#11515C',
                                           foreground='#F0F0F0',
                                           text='Find all \nanswers',
                                           command=self.call_solve_recursive)
        self.b_solve_recursive.place(x=20, y=80, width=160, height=50)
        
        # Button Solve Evolution
        self.b_solve_evolution = tk.Button(master=self.f_interaction,
                                           background='#11515C',
                                           foreground='#F0F0F0',
                                           text='Find evo \nanswers',
                                           command=self.call_solve_evolution)
        self.b_solve_evolution.place(x=20, y=140, width=160, height=50)
        
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
        """
        Showing the hours in the time table.
        If a hour is taken by a patient, the patient name is shown in 
        the hour.
        
        As the UI does not keep track of a shared patients list, each 
        time the patients are updated, this function needs to be called.

        Args:
            hours(list[Hour, ]): Hours, which will be loaded
            
        Returns:
            None
        """
        
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
        
    def show_calc_frame(self):
        self.sf_calc_frame = SubFrameCalculatingSolution(self.controller, self.main)
        self.sf_calc_frame.load()
        
    def hide_calc_frame(self):
        if self.sf_calc_frame is not None:
            self.sf_calc_frame.main.destroy()
            self.sf_calc_frame = None
        
    def set_progress(self, value:float):
        value = int(value*100)
        if self.sf_calc_frame is not None:
            self.sf_calc_frame.progress.set(value)
        else:
            raise RuntimeError("Cannot increase progress of None Frame")
        
    def deactivate(self) -> None:
        self.b_patient_managing.configure(state="disabled")
        self.b_solve_define.configure(state="disabled")
        self.b_solve_recursive.configure(state="disabled")
        self.b_solve_evolution.configure(state="disabled")
        
    def activate(self) -> None:
        self.b_patient_managing.configure(state="normal")
        self.b_solve_define.configure(state="normal")
        self.b_solve_recursive.configure(state="normal")
        self.b_solve_evolution.configure(state="normal")
        
    def load(self,) -> None:
        print("Placing Main")
        self.main.place(x=0, y=0)
        
    def hide(self) -> None:
        self.main.place_forget()
        
class FrameManager(BaseFrame):
    """
    Frame for the Manager "window"
    It allows the user to see all patients and edit them and/or add
    new ones.
    
    Args:
        con(UIController) : Controller for UI handling.
        root_window(tk.Tk) : parental window in which it will be 
            placed in.
    
    """
    def __init__(self, con:'UIController', root_window:tk.Tk):
        super().__init__(con, root_window)
                
        # Tkinter has some dodgy behavior so force update
        self.root.update()
        
        # Main Frame
        self.main = tk.Frame(master=self.root,
                             background="#1F1F1F",
                             width=self.root.winfo_width(),
                             height=self.root.winfo_height())
        
        self.bs_patients:list[tk.Button] = []
        self.bs_deletion:list[tk.Button] = []
        
        self.sf_list_patients = SubFramePatientList(
            self.controller,
            self.main,
            [])
        self.sf_list_patients.load()
        
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
        """
        Moves the frame, in which the patients buttons are placed up 
        and down, due to the limited window size in creates an illusion
        of scrolling

        Args:
            up (bool): direction of scrolling
            
        Return:
            None
        """
        self.sf_list_patients.scroll(up)

    def load_patients(self, patients:list[Patient,]) -> None:
        """
        Shows all given patients.
        Each patient is shown as a button to edit, and a delete button.
        
        As the UI does not keep track of a shared patients list, each 
        time the patients are updated, this function needs to be called.

        Args:
            patients(list[Patient, ]): Patients, which will be loaded
            
        Returns:
            None
        """
        self.sf_list_patients.load_patients(patients)

    def destroy(self) -> None:
        self.root.destroy()
        
    def load(self) -> None:
        # Binding scroll wheel
        self.root.bind("<Button-4>", lambda event:
            self.sf_list_patients.scroll(up=False))
        self.root.bind("<Button-5>", lambda event:
            self.sf_list_patients.scroll(up=True))
        self.main.place(x=0, y=0)
        
    def hide(self) -> None:
        # Unbinding scroll wheel
        self.root.unbind("<Button-4>")
        self.root.unbind("<Button-5>")
        self.main.place_forget()
        
class FrameEditPatient(BaseFrame):
    """
    Frame for the Edit "window"
    It allows the user to edit a patient or add a new one
    
    Args:
        con(UIController) : Controller for UI handling.
        root_window(tk.Tk) : parental window in which it will be 
            placed in.
    
    """
    def __init__(self, con:'UIController', root_window:tk.Tk):
        super().__init__(con, root_window)
        
        self.patient_name = ''
        self.pos_hours:list[int] = []
        self.patient = Patient(self.patient_name, self.pos_hours)
        self.week = Week()
        
        # Constants
        self.DAY_WIDTH = 170
        self.TIME_SPACING = 40
        self.PX_PER_HOUR = int(self.TIME_SPACING + 10)
        
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
        
        # Main Frame
        self.main = tk.Frame(master=self.root,
                             background="#1F1F1F",
                             width=self.root.winfo_width(),
                             height=self.root.winfo_height()
                             )
        # Frame Time
        self.f_time_table = tk.Frame(master=self.main,
                                     background='#333333',
                                     relief='ridge',
                                     border=2,
                                     cursor='arrow')
        self.f_time_table.place(x=10,
                                y=10,
                                width= 20 + self.POS_CONSTANTS["Time"]["width"] + 20 
                                       + 5*(self.POS_CONSTANTS["Day"]["width"] + 20),
                                height= 20 + self.POS_CONSTANTS["Day"]["height"] + 20 
                                        + 13*(self.POS_CONSTANTS["Time"]["height"] + 10))
        
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
        
        # Input name
        self.frame_config = tk.Frame(master=self.main,
                                     background='#2b2d30')
        self.frame_config.place(x=1040, y=10, width=200, height=200)

        self.l_patient_name = tk.Label(master=self.frame_config,
                                       background='#24beca',
                                       foreground='#0b1215',
                                       text='Patient Name',
                                       font='Aral, 16')
        self.l_patient_name.place(x=20, y=20, width=160, height=30)

        self.e_patient_name = tk.Entry(master=self.frame_config)
        self.e_patient_name.insert(0, self.patient.name)
        self.e_patient_name.place(x=20, y=60, width=160, height=20)

        self.b_confirm = tk.Button(master=self.frame_config,
                                   background='#126875',
                                   foreground='#24beca',
                                   text='Confirm',
                                   command=self.call_confirm)
        self.b_confirm.place(x=20, y=100, width=160, height=30)
        
        # Show Hours
        self.bs_hours:list[tk.Button] = []
        
        for index, hour in enumerate(self.week.hours):
            day_index = hour.ID >> 4
            day = self.DAYS[day_index]
            colour = "green" if hour.ID in self.patient.pos_times else "red"
            self.bs_hours.append(tk.Button(master =self.f_time_table,
                                          background=colour,
                                          foreground='#F0F0F0',
                                          relief='ridge',
                                          text='' if hour.taken_by is None else hour.taken_by.name,
                                          command=lambda i=index : self.add_hour_to_pos_hours(i)))
                                          #text=f'{hour.time} // {hour.duration}'))
            self.bs_hours[-1].place(x=self.POSITIONS["Day"][day][0],
                                    y=self.POSITIONS["Time"][hour.time[:2]+ '00'][1]
                                      +self.POS_CONSTANTS["Time"]["px_per_hour"]*int(hour.time[2:])/60,
                                    width=self.POS_CONSTANTS["Day"]["width"],
                                    height=self.POS_CONSTANTS["Time"]["px_per_hour"] * hour.duration/60)
        
    def call_confirm(self):
        self.controller.handle_call_confirm_edit_patient(
            self.patient,
            self.e_patient_name.get(),
            self.pos_hours)
            
            
    def add_hour_to_pos_hours(self, index:int) -> None:
        print(self.week.hours[index].ID)
        if self.week.hours[index].ID in self.pos_hours:
            self.pos_hours.remove(self.week.hours[index].ID)
            self.bs_hours[index].configure(background='red',
                                           activebackground='red')
        else:
            self.pos_hours.append(self.week.hours[index].ID)
            self.bs_hours[index].configure(background='green',
                                           activebackground='green')
    
    def load_patient(self, patient:Patient) -> None:
        """
        Loads a patient to edit.
        If not called the frame will assume that the user wants to 
        create a new one.

        Args:
            patient (Patient): Patient to edit
        """
        self.patient = patient
        self.patient_name = patient.name
        self.pos_hours = patient.pos_times
        self.e_patient_name.insert('end', patient.name)
        for index, button in enumerate(self.bs_hours):
            if self.week.hours[index].ID in self.pos_hours:
                button.configure(background='green',
                                 activebackground='green')
            else:
                button.configure(background='red',
                                 activebackground='red')
    
    def load(self,) -> None:
        self.main.place(x=0, y=0)
        
    def hide(self):
        """
        Frame persist in the background, so after cancellation or 
        successful creation ofd patient all data needs to be cleared
        to not have side effects.
        """
        self.patient_name = ''
        self.pos_hours = []
        self.patient = Patient(self.patient_name, self.pos_hours)
        self.e_patient_name.delete(0, 'end')
        self.e_patient_name.insert('end', '')
        for button in self.bs_hours:
            button.configure(background='red')
        self.main.place_forget()

class SubFramePatientList(BaseFrame):
    """
    Sub frame for scrolling thought the patients.
    Args:
        con(UIController): Controller for UI handling
        root_window(tk.Tk) : parental window in which it will be 
            placed in.
    """
    def __init__(self,
                 con:'UIController',
                 root_window:tk.Tk|tk.Frame,
                 patients:list[Patient,]):
        
        super().__init__(con, root_window)
        
        self.patients = patients
        self.bs_deletion = []
        self.bs_patients = []
        
        self.root.update()
        
        # Main Frame
        self.main = tk.Frame(master=self.root,
                             bg='#2b2d30',
                             border=2,
                             relief="solid",
                             width=320,
                             height=600)
        
        # Scrollable
        self.scrollable = tk.Frame(master=self.main,
                                   bg="#2B2D30",
                                   border=2,
                                   relief="solid",
                                   width=316)
        self.scrollable.place(x=0, y=2)
        
    def scroll(self, up:bool) -> None:
        delta = 25
        self.root.update()
        loc_height = self.scrollable.winfo_height()
        main_height = self.main.winfo_height()
        old_y = self.scrollable.winfo_y()
        dir = -delta if up else delta
        test_y = old_y + dir
        if loc_height - main_height <= 0:
            # Scrollable Window is smaller than parent, no need for scrolling
            return
        elif test_y > 0:
            # Upper stop
            new_y = 0
        elif main_height - test_y > loc_height:
            # Lower Stop
            new_y = main_height - loc_height
        else:
            new_y = test_y
            
        self.scrollable.place_configure(y=new_y)
        
    def load(self):
        self.main.place(x=10, y=10)
        
    def load_patients(self, patients:list[Patient,]) -> None:
        """
        Shows all given patients.
        Each patient is shown as a button to edit, and a delete button.
        
        As the UI does not keep track of a shared patients list, each 
        time the patients are updated, this function needs to be called.

        Args:
            patients(list[Patient, ]): Patients, which will be loaded
            
        Returns:
            None
        """
        
        self.patients = patients
        # Delete old labels
        for b_patient, b_delete in zip(self.bs_patients, self.bs_deletion):
            b_patient.destroy()
            b_delete.destroy()
        self.bs_patients = []
        self.bs_deletion = []
        
        # Adjust scrollable height 
        self.root.update()
        self.scrollable.place_configure(height=5 + len(patients)*25 + 5)
        self.root.update()
        
        for index, patient in enumerate(patients):
            self.bs_patients.append(tk.Button(master=self.scrollable,
                                             background='#ACAB00',
                                             foreground='#000000',
                                             text=patient.name,
                                             command=lambda i=index : self.call_edit_patient(i)))
            self.bs_patients[-1].place(x=10, y=25*index+5, width=270, height=20)
            
            self.bs_deletion.append(tk.Button(master=self.scrollable,
                                              background="#C00812",
                                              foreground='#081505',
                                              text="X",
                                              command=lambda i=index : self.call_patient_deletion(i)))
            self.bs_deletion[-1].place(x=290, y=25*index+5, width=20, height=20)
        
    def call_patient_deletion(self, index:int) -> None:
        self.controller.handle_call_delete_patient(index)

    def call_edit_patient(self, index:int) -> None:
        self.controller.handle_edit_patient_ui(index)
        
class SubFrameCalculatingSolution(BaseFrame):
    """
    Frame for showing the User, that the program is currently running
    the calculation for the clicked solution and not just stuck.

    Args:
        con(UIController): Controller for UI handling
        root_window(tk.Tk) : parental window in which it will be 
            placed in.
    """
    def __init__(self, con:'UIController', root_window:tk.Tk|tk.Frame):
        super().__init__(con, root_window)
        
        # Tkinter has some dodgy behavior so force update
        self.root.update()
        self.height = self.root.winfo_height()
        self.width = self.root.winfo_width()
        # Main
        self.main = tk.Frame(master=self.root,
                             bg="grey",
                             height=self.height // 3,
                             width=self.width // 3,
                             border=10,
                             relief="groove")
        
        # Calc Explanation
        self.l_text = tk.Label(master=self.main,
                               background="#4A0215",
                               foreground="#F0F0F0",
                               font=("Aral, 16"),
                               text="Calculating Solutions")
        self.l_text.place(x=30, y=40, height=40, width=self.width//3 - 80)
        
        # Progress
        self.progress = tk.IntVar()        
        self.progress_bar = ttk.Progressbar(master=self.main,
                                            orient="horizontal",
                                            length=max(0, self.width//3-80),
                                            maximum=100.1, # Increase by .1 to prevent floating point stuff
                                            variable=self.progress)
        
        self.progress_bar.place(x=30, y=100, height=30)
        
    def load(self):
        self.main.place(x=self.width//3, y=self.height//3)
        
    def hide(self):
        self.main.place_forget()