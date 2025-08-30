import os
import json

from typing import TypedDict

from .hour import Hour
from .patient import Patient

__dict_day = TypedDict("__dict_day", {"time" : str,
                                      "duration" : int})
__dict_hours_data = TypedDict("__dict_hours_data", {"Monday" : list[__dict_day],
                                                    "Tuesday" : list[__dict_day],
                                                    "Wednesday" : list[__dict_day],
                                                    "Thursday" : list[__dict_day],
                                                    "Friday" : list[__dict_day],})

__dict_patient_data = TypedDict("__dict_patient_data", {"name" : str,
                                                        "possible hours" : list[int,]})



class InputHours:
    @classmethod
    def load(cls, path=os.path.join(".", "configs", "hours.json")) -> list[Hour,]:
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
    def get_data(cls, path=os.path.join("..", "configs", "hours.json")) -> __dict_hours_data:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

class InputPatients:
    @classmethod
    def load(cls, path:str=os.path.join("..", "configs", "patients.json")):
        patients = []
        data = InputPatients.get_data(path)
        for patient in data:
            patients.append(Patient(patient["name"], patient["possible hours"]))
        return patients

    @classmethod
    def get_data(cls, path:str=os.path.join("..", "configs", "patients.json")) -> list[__dict_patient_data]:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

