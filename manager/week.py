import os
import copy
import pickle

from .static_io import InputHours
from .hour import Hour

class Week:
    """
    Representation of the working week. It loads all hours given in the config file, 
    if not given hours directly
    path: str: (optional) Path to the config file to load the hors from
    hours: list[Hour,]: (optional) Hours containing the week
    """
    def __init__(self, path:str=os.path.join("manager", "config"), hours:list[Hour, ]=[]) -> None:
        if hours == []:
            if os.path.exists(os.path.join(path, "plan.pickle")):
                try:
                    self.hours = pickle.load(open(os.path.join(path, "plan.pickle"), "rb+"))
                    print("Loaded plan.pickle")
                except BaseExceptionGroup:
                    self.hours = InputHours.load()
                    print("Couldn't open pickle; loading Week")
            else:
                self.hours = InputHours.load()
                print("Didn't find pickle; Loading Week")
        else:
            self.hours = hours
            
    def save(self):
        pickle.dump(self.hours,
                    open(os.path.join("manager", "config", "plan.pickle"), "wb+"))

    def copy(self) -> 'Week':
        """
        Copies the content of the week directly. Preventing any shenanigans with changing one hour 
        """
        return type(self)(hours=[copy.deepcopy(hour) for hour in self.hours])

    def __repr__(self) -> str:
        return f"Week:\n{[h.taken_by.name if h.taken_by is not None else None for h in self.hours]}"
