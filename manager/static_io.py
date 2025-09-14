import os
import json

from typing import TypedDict

from .hour import Hour
from .patient import Patient

_dict_day = TypedDict("_dict_day", {"time" : str,
                                      "duration" : int})
_dict_hours_data = TypedDict("_dict_hours_data", {"Monday" : list[_dict_day],
                                                  "Tuesday" : list[_dict_day],
                                                  "Wednesday" : list[_dict_day],
                                                  "Thursday" : list[_dict_day],
                                                  "Friday" : list[_dict_day],})

_dict_patient_data = TypedDict("_dict_patient_data", {"name" : str,
                                                      "possible hours" : list[int,]})



class InputHours:
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
    def get_data(cls, path=os.path.join("manager", "config", "hours.json")) -> _dict_hours_data:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)


class InputPatients:
    @classmethod
    def load(cls, path:str=os.path.join("manager", "config", "patients.json")):
        patients = []
        data = InputPatients.get_data(path)
        for patient in data:
            patients.append(Patient(patient["name"], patient["possible hours"]))
        return patients

    @classmethod
    def get_data(cls, path:str=os.path.join("manager", "config", "patients.json")) -> list[_dict_patient_data]:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def save(cls,
             patients:list[Patient],
             path:str=os.path.join("manager", "config", "patients.json")) -> None:
        
        data:list[_dict_patient_data] = []
        
        for patient in patients:
            data.append({"name" : patient.name,
                         "possible hours" : patient.pos_times})
        
        json.dump(data,
                  open(path, 'w+', encoding='utf-8'),
                  indent=4)
        