import tkinter as tk

from .hour import Hour

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller

class MainGUI:
    def __init__(self, controller:'Controller') -> None:
        self.controller = controller
        
        self.root = tk.Tk()
        self.root.title('Patient Manager')
        self.root.geometry('1250x580')
        self.root.configure(background='#1f1f1f')
        self.root.bind_all('<Escape>', lambda event : self.root.destroy())
        
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
        self.b_solve_define.place(x=20, y=90, width=160, height=50)
        
    def call_solve_recursive(self):
        solutions = self.controller.solve_recursive()
        if len(solutions) == 0:
            print('No solutions found')
            return
        else:
            print(f'Found {len(solutions)} Solutions. Taking the First one')
            self.load_hours(solutions[0].hours)
    
    def call_solve_define(self):
        self.controller.solve_define_answers()
        self.load_hours(self.controller.week.hours)
    
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