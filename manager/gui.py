import tkinter as tk

from .hour import Hour
from .patient import Patient
from .week import Week

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui_controller import UIController

class MainGUI:
    def __init__(self, controller:'UIController') -> None:
        self.controller = controller
        
        self.root = tk.Tk()
        self.root.title('Patient Manager')
        self.root.geometry('1250x620')
        self.root.configure(background='#1f1f1f')
        self.root.bind('<Escape>', lambda event : self.close())
        
        # Constants
        self.DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.TIMES = ["0700",
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
        
        self.__POSITIONS_CONSTANTS = \
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
        self.__POSITIONS = \
            {
                "Day" : \
                    {
                        "Monday" : (20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20, 20),
                        "Tuesday" : (20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + self.__POSITIONS_CONSTANTS["Day"]["width"]+20, 20),
                        "Wednesday" : (20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.__POSITIONS_CONSTANTS["Day"]["width"]+20)*2, 20),
                        "Thursday" : (20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.__POSITIONS_CONSTANTS["Day"]["width"]+20)*3, 20),
                        "Friday" : (20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.__POSITIONS_CONSTANTS["Day"]["width"]+20)*4, 20)
                        
                    },
                "Time" : \
                    {
                        "0700" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20),
                        "0800" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + self.__POSITIONS_CONSTANTS["Time"]["height"]+10),
                        "0900" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*2),
                        "1000" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*3),
                        "1100" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*4),
                        "1200" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*5),
                        "1300" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*6),
                        "1400" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*7),
                        "1500" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*8),
                        "1600" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*9),
                        "1700" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*10),
                        "1800" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*11),
                        "1900" : (20, 20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.__POSITIONS_CONSTANTS["Time"]["height"]+10)*12),
                    }
            }
        # Frame Time
        self.f_time_table = tk.Frame(master=self.root,
                                     background='#333333',
                                     relief='ridge',
                                     border=2,
                                     cursor='arrow')
        self.f_time_table.place(x=10,
                                y=10,
                                width= 20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + 5*(self.__POSITIONS_CONSTANTS["Day"]["width"] + 20),
                                height=20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + 13*(self.__POSITIONS_CONSTANTS["Time"]["height"] + 10))
        
        # Labels Day
        self.ls_day : list[tk.Label] = []
        for day in self.DAYS:
            self.ls_day.append(tk.Label(master=self.f_time_table,
                                        background="#11515C",
                                        foreground='#F0F0F0',
                                        font='Aral, 18',
                                        text=day))
            self.ls_day[-1].place(x=self.__POSITIONS["Day"][day][0],
                                  y=self.__POSITIONS["Day"][day][1],
                                  width=self.__POSITIONS_CONSTANTS['Day']["width"],
                                  height=self.__POSITIONS_CONSTANTS['Day']["height"])
        
        # Labels Time
        self.ls_time: list[tk.Label,] = []
        
        for time in self.TIMES:
            self.ls_time.append(tk.Label(master=self.f_time_table,
                                         background='#11515C',
                                         foreground='#F0F0F0',
                                         text=time[:2] + ':' + time[2:]))
            self.ls_time[-1].place(x=self.__POSITIONS["Time"][time][0],
                                   y=self.__POSITIONS["Time"][time][1],
                                   width=self.__POSITIONS_CONSTANTS['Time']["width"],
                                   height=self.__POSITIONS_CONSTANTS['Time']["height"])
            
        # Frame User Interaction
        self.f_interaction = tk.Frame(master=self.root,
                                     background='#333333',
                                     border=2,
                                     cursor='arrow',
                                     relief='ridge')
        self.f_interaction.place(x=10 + 20 + self.__POSITIONS_CONSTANTS["Time"]["width"] + 20 + 5*(self.__POSITIONS_CONSTANTS["Day"]["width"] + 20) + 10,
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
            self.ls_hours[-1].place(x=self.__POSITIONS["Day"][day][0],
                                    y=self.__POSITIONS["Time"][hour.time[:2]+ '00'][1]+self.__POSITIONS_CONSTANTS["Time"]["px_per_hour"]*int(hour.time[2:])/60,
                                    width=self.__POSITIONS_CONSTANTS["Day"]["width"],
                                    height=self.__POSITIONS_CONSTANTS["Time"]["px_per_hour"] * hour.duration / 60)
        
    def start(self) -> None:        
        self.root.mainloop()
        
    def close(self) -> None:
        self.root.forget(self.root)
        # As closing the main window does't terminate the mainloop
        # we have to manually call the main termination
        self.controller.terminate()
        
    def destroy(self) -> None:
        self.root.destroy()
        

class PatientManagerUI:
    """
    This UI contains the handling operation regarding everything, the
    patient and it's data.
    It may also create its own children to fulfill its needs. These 
    should be controlled and killed by this class
    """
    def __init__(self,controller:'UIController', parent:tk.Tk) -> None:
        
        self.controller = controller
        
        self.patients = []

        self.root = tk.Toplevel(parent)
        self.root.title('Patients')
        self.root.geometry('600x300')
        self.root.configure(background='#1e1f22')
        self.root.bind('<Escape>', lambda event : self.destroy())
        self.root.bind_all('<Button-4>', lambda event: self.scroll_ui(up=False))
        self.root.bind_all('<Button-5>', lambda event : self.scroll_ui(up=True))

        self.bs_patients:list[tk.Button] = []
        self.bs_deletion:list[tk.Button] = []

        self.window_height = 300
        
        # List of all patients
        self.f_patients_position = [0, 0, 300, 300]
        self.f_patients_max_y = 300

        self.f_patients = tk.Frame(master=self.root,
                                    background='#2b2d30',
                                    border=2,
                                    relief='solid')
        self.f_patients.place(x=self.f_patients_position[0],
                              y=self.f_patients_position[1],
                              width=self.f_patients_position[2],
                              height=self.f_patients_position[3])

        # Show options
        self.f_options = tk.Frame(master=self.root,
                                    background='#2b2d30',
                                    border=2,
                                    relief='solid')
        self.f_options.place(x=340, y=20, width=140, height=260)
        
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
            if self.f_patients_position[1] + self.f_patients_position[3] - delta > self.f_patients_max_y:
                self.f_patients_position[1] -= delta
            else:
                self.f_patients_position[1] = self.f_patients_max_y - self.f_patients_position[3]
        else:
            if self.f_patients_position[1] > -delta:
                self.f_patients_position[1] = 0
            else:
                self.f_patients_position[1] += delta

        self.f_patients.place(x=self.f_patients_position[0],
                              y=self.f_patients_position[1],
                              width=self.f_patients_position[2],
                              height=self.f_patients_position[3])


    def load_patients(self, patients) -> None:
        print('Loading patients to show')
        self.patients = patients
        # Delete old labels
        for b_patient, b_delete in zip(self.bs_patients, self.bs_deletion):
            b_patient.destroy()
            b_delete.destroy()
        self.bs_patients = []
        self.bs_deletion = []
        
        count_patients = len(patients)
        self.f_patients_position[3] = max(count_patients*25 + 10, 600)

        for index, patient in enumerate(patients):
            self.bs_patients.append(tk.Button(master=self.f_patients,
                                             background='#ACAB00',
                                             foreground='#000000',
                                             text=patient.name,
                                             command=lambda i=index : self.call_edit_patient(i)))
            self.bs_patients[-1].place(x=0, y=25*index+5, width=260, height=20)
            
            self.bs_deletion.append(tk.Button(master=self.f_patients,
                                              background="#C00812",
                                              foreground='#081505',
                                              text="X",
                                              command=lambda i=index : self.call_patient_deletion(i)))
            self.bs_deletion[-1].place(x=270, y=25*index+5, width=20, height=20)
            
    def call_patient_deletion(self, index:int) -> None:
        self.controller.handle_call_delete_patient(self, self.patients[index])
    
    def call_edit_patient(self, index:int) -> None:
        # TODO: Rework week knowledge
        edit_ui = EditPatientUI(self.controller, self.root, self.patients[index], self.controller.base_controller.week)
        edit_ui.root.mainloop()

    def start(self) -> None:
        self.root.mainloop()
        
    def destroy(self) -> None:
        self.root.destroy()
        
class EditPatientUI:
    """
    This UI is responsible to allow the User to edit the Hours the 
    patient can attend to etc
    """
    
    def __init__(self, 
                 controller:'UIController',
                 parent: tk.Tk | tk.Toplevel,
                 patient:Patient | None,
                 week_buffer:Week) -> None:
        
        
        self.controller = controller
        self.week_buffer = week_buffer
        self.patient = patient if patient is not None else Patient('', [])
        
        self.root = tk.Toplevel(parent)
        self.root.title('Add Patient')
        self.root.geometry('1360x580')
        self.root.configure(background='#1e1f22')
        self.root.bind('<Escape>', lambda event: self.destroy())

        self.patient_name = ''
        self.pos_hours:list[int] = []
        
        # Time
        self.DAY_WIDTH = 170
        self.TIME_SPACING = 40
        self.PX_PER_HOUR = int(self.TIME_SPACING + 10)        
        
        # Constants
        self.DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.TIMES = ["0700",
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
        
        self.POSITIONS_CONSTANTS = \
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
        self.POSITIONS = \
            {
                "Day" : \
                    {
                        "Monday" : (20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20, 20),
                        "Tuesday" : (20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20 + self.POSITIONS_CONSTANTS["Day"]["width"]+20, 20),
                        "Wednesday" : (20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.POSITIONS_CONSTANTS["Day"]["width"]+20)*2, 20),
                        "Thursday" : (20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.POSITIONS_CONSTANTS["Day"]["width"]+20)*3, 20),
                        "Friday" : (20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20 + (self.POSITIONS_CONSTANTS["Day"]["width"]+20)*4, 20)
                        
                    },
                "Time" : \
                    {
                        "0700" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20),
                        "0800" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + self.POSITIONS_CONSTANTS["Time"]["height"]+10),
                        "0900" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*2),
                        "1000" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*3),
                        "1100" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*4),
                        "1200" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*5),
                        "1300" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*6),
                        "1400" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*7),
                        "1500" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*8),
                        "1600" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*9),
                        "1700" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*10),
                        "1800" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*11),
                        "1900" : (20, 20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + (self.POSITIONS_CONSTANTS["Time"]["height"]+10)*12),
                    }
            }
        # Frame Time
        self.f_time_table = tk.Frame(master=self.root,
                                     background='#333333',
                                     relief='ridge',
                                     border=2,
                                     cursor='arrow')
        self.f_time_table.place(x=10,
                                y=10,
                                width= 20 + self.POSITIONS_CONSTANTS["Time"]["width"] + 20 + 5*(self.POSITIONS_CONSTANTS["Day"]["width"] + 20),
                                height=20 + self.POSITIONS_CONSTANTS["Day"]["height"] + 20 + 13*(self.POSITIONS_CONSTANTS["Time"]["height"] + 10))
        
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
                                  width=self.POSITIONS_CONSTANTS['Day']["width"],
                                  height=self.POSITIONS_CONSTANTS['Day']["height"])
        
        # Labels Time
        self.ls_time: list[tk.Label,] = []
        
        for time in self.TIMES:
            self.ls_time.append(tk.Label(master=self.f_time_table,
                                         background='#11515C',
                                         foreground='#F0F0F0',
                                         text=time[:2] + ':' + time[2:]))
            self.ls_time[-1].place(x=self.POSITIONS["Time"][time][0],
                                   y=self.POSITIONS["Time"][time][1],
                                   width=self.POSITIONS_CONSTANTS['Time']["width"],
                                   height=self.POSITIONS_CONSTANTS['Time']["height"])
            
        # Hours
        self.bs_hours:list[tk.Button] = []
        
        for index, hour in enumerate(self.week_buffer.hours):
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
                                    +self.POSITIONS_CONSTANTS["Time"]["px_per_hour"]*int(hour.time[2:])/60,
                                    width=self.POSITIONS_CONSTANTS["Day"]["width"],
                                    height=self.POSITIONS_CONSTANTS["Time"]["px_per_hour"] * hour.duration/60)
        
        # Input name
        self.frame_config = tk.Frame(master=self.root,
                                     background='#2b2d30')
        self.frame_config.place(x=1050, y=10, width=200, height=200)

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
        
    def call_confirm(self):
        if self.controller.handle_call_confirm_edit_patient(self.patient,
                                                            self.e_patient_name.get(),
                                                            self.pos_hours):
            self.destroy()
            
    def add_hour_to_pos_hours(self, index:int) -> None:
        print(self.week_buffer.hours[index].ID)
        if self.week_buffer.hours[index].ID in self.pos_hours:
            self.pos_hours.remove(self.week_buffer.hours[index].ID)
            self.bs_hours[index].configure(background='red',
                                           activebackground='red')
        else:
            self.pos_hours.append(self.week_buffer.hours[index].ID)
            self.bs_hours[index].configure(background='green',
                                           activebackground='green')
    def destroy(self):
        self.root.destroy()
        
        