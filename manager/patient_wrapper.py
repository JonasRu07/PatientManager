import os
import copy

from .static_io import InputPatients
from .patient import Patient

class PatientWrapper:
    """
    Handler of all patients. It loads all patients given in the config file, 
    if not given patients directly
    path: str: (optional) Path to the config file to load the hors from
    patients: list[Patient,]: (optional) Patients to keep track of
    """
    def __init__(self, path:str=os.path.join("manager", "configs", "patients.json"), patients:list[Patient,]=[]):
        if patients == []:
            self.patients = InputPatients.load(path)
        else:
            self.patients = patients
        
    def add(self, patient:Patient) -> None:
        self.patients.append(patient)

    def copy(self) -> 'PatientWrapper':
        """
        Copies all patients directly. Preventing any shenanigans with changing one patient
        """
        return type(self)(patients=[copy.deepcopy(hour) for hour in self.patients])

