from .patient import Patient
from .static_io import InputPatients
from .patient_wrapper import PatientWrapper


class PatientManager:
    def __init__(self) -> None:
        patients:list[Patient] = InputPatients.load()
        self.patients = {}
        for patient in patients:
            self.patients[patient.ID] = patient
            
    def add_patient(self, patient:Patient) -> None:
        self.patients[patient.ID] = patient
        
    def delete_patient(self, target_patient:Patient, _raise:bool=False) -> bool:
        self.patients.pop(target_patient.ID)
        return True
        
    def get_patients_inside_wrapper(self):
        return PatientWrapper(patients=list(self.patients.values()))