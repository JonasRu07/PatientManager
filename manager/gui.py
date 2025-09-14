import tkinter as tk

from .hour import Hour
from .week import Week

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ui_controller import UIController

class MainGUI:
    def __init__(self, controller:'UIController') -> None:
        self.controller = controller
        
        self.root = tk.Tk()
        self.root.title('Patient Manager')
        self.root.geometry('1250x580')
        self.root.configure(background='#1f1f1f')
        self.root.bind_all('<Escape>', lambda event : self.close())
        
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
                                height=20 + self.__POSITIONS_CONSTANTS["Day"]["height"] + 20 + 12*(self.__POSITIONS_CONSTANTS["Time"]["height"] + 10))
        
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
                                 height=560)
        
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
        
        # Button add patient
        self.b_add_patient = tk.Button(master=self.f_interaction,
                                       background='#11515C',
                                       foreground='#F0F0F0',
                                       text='Add Patient',
                                       command=self.call_add_patient)
        self.b_add_patient.place(x=20, y=140, width=160, height=35)
        
    def call_add_patient(self):
        self.controller.handle_ui_add_patient()
        
    def call_solve_recursive(self):
        self.controller.handle_solve_recursive()
    
    def call_solve_define(self):
        self.controller.handle_solve_define()
    
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
        
    def start(self):        
        self.root.mainloop()
        
    def close(self):
        self.root.forget(self.root)
        # As closing the main window does't terminate the mainloop
        # we have to manually call the main termination
        self.controller.terminate()
        
    def destroy(self):
        self.root.destroy()
        
    
    
class AddPatientGUI:

    def __init__(self, controller:'UIController', parent:tk.Tk, week_buffer:Week):

        self.controller = controller
        self.week_buffer=week_buffer

        self.patient_name = ''
        self.pos_hours = []

        # Time
        self.DAY_WIDTH = 170
        self.TIME_SPACING = 20
        self.PX_PER_HOUR = int(self.TIME_SPACING + 10)

        self.POSITIONS: dict[str, dict[str, tuple[int, int]]] = \
            {
                'Day': {
                    'Monday': (120, 20),
                    'Tuesday': (120 + self.DAY_WIDTH + 10, 20),
                    'Wednesday': (120 + (self.DAY_WIDTH + 10) * 2, 20),
                    'Thursday': (120 + (self.DAY_WIDTH + 10) * 3, 20),
                    'Friday': (120 + (self.DAY_WIDTH + 10) * 4, 20)
                },
                'Time': {
                    '0700': (20, 80),
                    '0800': (20, 80 + (self.TIME_SPACING + 10) * 1),
                    '0900': (20, 80 + (self.TIME_SPACING + 10) * 2),
                    '1000': (20, 80 + (self.TIME_SPACING + 10) * 3),
                    '1100': (20, 80 + (self.TIME_SPACING + 10) * 4),
                    '1200': (20, 80 + (self.TIME_SPACING + 10) * 5),
                    '1300': (20, 80 + (self.TIME_SPACING + 10) * 6),
                    '1400': (20, 80 + (self.TIME_SPACING + 10) * 7),
                    '1500': (20, 80 + (self.TIME_SPACING + 10) * 8),
                    '1600': (20, 80 + (self.TIME_SPACING + 10) * 9),
                    '1700': (20, 80 + (self.TIME_SPACING + 10) * 10),
                    '1800': (20, 80 + (self.TIME_SPACING + 10) * 11),
                }
            }

        self.bs_hours: list[tk.Button,] = []

        self.child = tk.Tk()
        self.child.title('Add Patient')
        self.child.geometry('1320x500')
        self.child.configure(background='#1e1f22')
        self.child.bind('<Escape>', lambda event: self.destroy())

        # Frame Time plan
        self.f_time_plan = tk.Frame(master=self.child,
                                    background='#2b2d30',
                                    border=2,
                                    relief='solid')
        self.f_time_plan.place(x=20, y=20, width=1040, height=460)

        # Labels Days
        self.l_monday = tk.Label(master=self.f_time_plan,
                                 background='#4a267c',
                                 foreground='#ced0d6',
                                 text='Monday',
                                 font='Mono, 20',
                                 )
        self.l_monday.place(x=self.POSITIONS['Day']['Monday'][0],
                            y=self.POSITIONS['Day']['Monday'][1],
                            width=self.DAY_WIDTH,
                            height=40)

        self.l_tuesday = tk.Label(master=self.f_time_plan,
                                  background='#4a267c',
                                  foreground='#ced0d6',
                                  text='Tuesday',
                                  font='Mono, 20',
                                  )
        self.l_tuesday.place(x=self.POSITIONS['Day']['Tuesday'][0],
                             y=self.POSITIONS['Day']['Tuesday'][1],
                             width=self.DAY_WIDTH,
                             height=40)

        self.l_wednesday = tk.Label(master=self.f_time_plan,
                                    background='#4a267c',
                                    foreground='#ced0d6',
                                    text='Wednesday',
                                    font='Mono, 20',
                                    )
        self.l_wednesday.place(x=self.POSITIONS['Day']['Wednesday'][0],
                               y=self.POSITIONS['Day']['Wednesday'][1],
                               width=self.DAY_WIDTH,
                               height=40)

        self.l_thursday = tk.Label(master=self.f_time_plan,
                                   background='#4a267c',
                                   foreground='#ced0d6',
                                   text='Thursday',
                                   font='Mono, 20',
                                   )
        self.l_thursday.place(x=self.POSITIONS['Day']['Thursday'][0],
                              y=self.POSITIONS['Day']['Thursday'][1],
                              width=self.DAY_WIDTH,
                              height=40)

        self.l_friday = tk.Label(master=self.f_time_plan,
                                 background='#4a267c',
                                 foreground='#ced0d6',
                                 text='Friday',
                                 font='Mono, 20',
                                 )
        self.l_friday.place(x=self.POSITIONS['Day']['Friday'][0],
                            y=self.POSITIONS['Day']['Friday'][1],
                            width=self.DAY_WIDTH,
                            height=40)

        # Label Times
        self.l_0700 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='07:00',
                               font='Mono, 12',
                               )
        self.l_0700.place(x=self.POSITIONS['Time']['0700'][0],
                          y=self.POSITIONS['Time']['0700'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_0800 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='08:00',
                               font='Mono, 12',
                               )
        self.l_0800.place(x=self.POSITIONS['Time']['0800'][0],
                          y=self.POSITIONS['Time']['0800'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_0900 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='09:00',
                               font='Mono, 12',
                               )
        self.l_0900.place(x=self.POSITIONS['Time']['0900'][0],
                          y=self.POSITIONS['Time']['0900'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1000 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='10:00',
                               font='Mono, 12',
                               )
        self.l_1000.place(x=self.POSITIONS['Time']['1000'][0],
                          y=self.POSITIONS['Time']['1000'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1100 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='11:00',
                               font='Mono, 12',
                               )
        self.l_1100.place(x=self.POSITIONS['Time']['1100'][0],
                          y=self.POSITIONS['Time']['1100'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1200 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='12:00',
                               font='Mono, 12',
                               )
        self.l_1200.place(x=self.POSITIONS['Time']['1200'][0],
                          y=self.POSITIONS['Time']['1200'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1300 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='13:00',
                               font='Mono, 12',
                               )
        self.l_1300.place(x=self.POSITIONS['Time']['1300'][0],
                          y=self.POSITIONS['Time']['1300'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1400 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='14:00',
                               font='Mono, 12',
                               )
        self.l_1400.place(x=self.POSITIONS['Time']['1400'][0],
                          y=self.POSITIONS['Time']['1400'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1500 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='15:00',
                               font='Mono, 12',
                               )
        self.l_1500.place(x=self.POSITIONS['Time']['1500'][0],
                          y=self.POSITIONS['Time']['1500'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1600 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='16:00',
                               font='Mono, 12',
                               )
        self.l_1600.place(x=self.POSITIONS['Time']['1600'][0],
                          y=self.POSITIONS['Time']['1600'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1700 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='17:00',
                               font='Mono, 12',
                               )
        self.l_1700.place(x=self.POSITIONS['Time']['1700'][0],
                          y=self.POSITIONS['Time']['1700'][1],
                          width=80,
                          height=self.TIME_SPACING)

        self.l_1800 = tk.Label(master=self.f_time_plan,
                               background='#24beca',
                               foreground='#0b1215',
                               text='18:00',
                               font='Mono, 12',
                               )
        self.l_1800.place(x=self.POSITIONS['Time']['1800'][0],
                          y=self.POSITIONS['Time']['1800'][1],
                          width=80,
                          height=self.TIME_SPACING)


        # Input name
        self.frame_config = tk.Frame(master=self.child,
                                     background='#2b2d30')
        self.frame_config.place(x=1100, y=20, width=200, height=200)

        self.l_patient_name = tk.Label(master=self.frame_config,
                                       background='#24beca',
                                       foreground='#0b1215',
                                       text='Patient Name',
                                       font='Aral, 16')
        self.l_patient_name.place(x=20, y=20, width=160, height=30)

        self.e_patient_name = tk.Entry(master=self.frame_config)
        self.e_patient_name.place(x=20, y=60, width=160, height=20)

        self.b_confirm = tk.Button(master=self.frame_config,
                                   background='#126875',
                                   foreground='#24beca',
                                   text='Confirm',
                                   command=self.call_confirm)
        self.b_confirm.place(x=20, y=100, width=160, height=30)

        # Hours
        self.bs_hours = []

        for index, hour in enumerate(self.week_buffer.hours):
            day = hour.ID >> 4
            if day == 0:
                day = 'Monday'
            elif day == 1:
                day = 'Tuesday'
            elif day == 2:
                day = 'Wednesday'
            elif day == 3:
                day = 'Thursday'
            elif day == 4:
                day = 'Friday'
            else:
                print(f'Invalid Day ID {day}')
                return

            self.bs_hours.append(tk.Button(master=self.f_time_plan,
                                           background='red',
                                           activebackground='red',
                                           foreground='#0b1215',
                                           command= lambda i=index: self.add_hour_to_pos_hours(i)
                                           )
                                 )
            self.bs_hours[-1].place(x=self.POSITIONS['Day'][day][0],
                                    y=self.POSITIONS['Time']['0700'][1]
                                      + (int(hour.time[:2]) - 7) * 30
                                      + int(hour.time[2:]) * self.PX_PER_HOUR / 60,
                                    width=self.DAY_WIDTH,
                                    height=self.PX_PER_HOUR / 60 * hour.duration
                                    )
            

    def add_hour_to_pos_hours(self, index:int):
        print(self.week_buffer.hours[index].ID)
        if self.week_buffer.hours[index].ID in self.pos_hours:
            self.pos_hours.remove(self.week_buffer.hours[index].ID)
            self.bs_hours[index].configure(background='red',
                                           activebackground='red')
        else:
            self.pos_hours.append(self.week_buffer.hours[index].ID)
            self.bs_hours[index].configure(background='green',
                                           activebackground='green')

    def call_confirm(self):
        self.controller.handle_call_add_patient(self.e_patient_name.get(), self.pos_hours)

    def start(self):
        self.child.mainloop()
        
    def destroy(self):
        self.child.destroy()