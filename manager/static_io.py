"""



"""

import os
import json

from typing import TypedDict

from .hour import Hour
from .patient import Patient

class DayDict(TypedDict):
    time : str
    duration : int
    
class WeekDataDict(TypedDict):
    Monday : list[DayDict]
    Tuesday : list[DayDict]
    Wednesday : list[DayDict]
    Thursday : list[DayDict]
    Friday : list[DayDict]
    
PatientDataDict = TypedDict("PatientDataDict",
                            {
                                "name" : str,
                                "possible hours" : list[int]
                            })

class EvoParameters(TypedDict):
    sample_size : int
    reward_per_patient : int
    reward_consecutive_hours : int
    reward_time_limit : int
    
    
class InputHours:
    """
    Loader and Saver for Hours described in the hours.json config.
    Hours are only saved and read with the time and duration stats
    """
    @classmethod
    def load(cls, path=os.path.join("manager", "config", "hours.json")) -> list[Hour,]:
        hours = []
        data = InputHours.get_data(path)

        for index, hour in enumerate(data["Monday"], ):
            hours.append(Hour(ID=0 + index, time=hour["time"], duration=hour["duration"]))
        for index, hour in enumerate(data["Tuesday"]):
            hours.append(Hour(ID=16 + index, time=hour["time"], duration=hour["duration"]))
        for index, hour in enumerate(data["Wednesday"]):
            hours.append(Hour(ID=32 + index, time=hour["time"], duration=hour["duration"]))
        for index, hour in enumerate(data["Thursday"]):
            hours.append(Hour(ID=48 + index, time=hour["time"], duration=hour["duration"]))
        for index, hour in enumerate(data["Friday"]):
            hours.append(Hour(ID=64 + index, time=hour["time"], duration=hour["duration"]))
        return hours

    @classmethod
    def get_data(cls, path=os.path.join("manager", "config", "hours.json")) -> WeekDataDict:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

class InputPatients:
    @classmethod
    def load(cls, path:str=os.path.join("manager", "config", "patients.json")) -> list[Patient,]:
        patients = []
        data = InputPatients.get_data(path)
        for patient in data:
            patients.append(Patient(patient["name"], patient["possible hours"]))
        return patients

    @classmethod
    def get_data(cls, path:str=os.path.join("manager", "config", "patients.json")) -> list[PatientDataDict]:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def save(cls,
             patients:list[Patient],
             path:str=os.path.join("manager", "config", "patients.json")) -> None:
        
        data:list[PatientDataDict] = []
        
        for patient in patients:
            data.append({"name" : patient.name,
                         "possible hours" : patient.pos_times})
        
        json.dump(data,
                  open(path, 'w+', encoding='utf-8'),
                  indent=4)
        
class ConstEvoParams:
    @classmethod
    def load(cls,
             path:str=os.path.join("manager", "config", "evo_parameters.json")
             ) -> EvoParameters:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return {
                "sample_size" : data["sample_size"],
                "reward_per_patient" : data["reward_per_patient"],
                "reward_consecutive_hours" : data["reward_consecutive_hours"],
                "reward_time_limit" : data["reward_time_limit"]
            }
    
    @classmethod
    def save(cls,
             data:EvoParameters,
             path:str=os.path.join("manager", "config", "evo_parameters")
             )-> None:
        
        json.dump(data,
                  open(path, "w+",encoding="utf-8"),
                  indent=4
                  )
        
class InputPlan:
    @classmethod
    def load(cls, 
             path:str):
        patients = InputPatients.load()
        patients_dict = {}
        for patient in patients:
            patients_dict[patient.name] = patient
                
        with open(os.path.join("manager", "config", "plan.json"), "r") as plan_file:
            plan_data = json.load(plan_file)
            hours = []
            for data_set in plan_data:
                hours.append(Hour(
                    data_set["hourID"],
                    data_set["time"],
                    data_set["duration"]
                ))
                if data_set["taken_by"] is not None:
                    hours[-1].taken_by = patients_dict[data_set["taken_by"]]

        return hours
        
    @classmethod
    def save(cls,
             hours:list[Hour,]):
        data = []
        for hour in hours:
            set = {
                "hourID" : hour.ID,
                "time" : hour.time,
                "duration" : hour.duration
            }
            if hour.taken_by is None:
                set["taken_by"] = None
            else:
                set["taken_by"] = hour.taken_by.name
            data.append(set)
            
        json.dump(data,
                  open(os.path.join("manager", "config", "plan.json"), "w"),
                  indent=4)
                    