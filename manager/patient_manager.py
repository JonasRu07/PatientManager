from .patient import Patient
from .static_io import InputPatients
from .patient_wrapper import PatientWrapper


class PatientManager:
    def __init__(self) -> None:
        self.patients:list[Patient] = InputPatients.load()
        self.patients.sort(key=lambda x:x.name)
        
    def add_patient(self, patient:Patient) -> None:
        self.patients.append(patient)
        self.patients.sort(key=lambda x:x.name)
        
    def delete_patient(self, target_patient:Patient, _raise:bool=False) -> bool:
        for index, patient in enumerate(self.patients):
            if patient == target_patient:
                self.patients.pop(index)
                return True

        if _raise:
            raise ValueError('Patient was not in list')
        
        return False
    
    def get_patients_inside_wrapper(self):
        return PatientWrapper(patients=self.patients)