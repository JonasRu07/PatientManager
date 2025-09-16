from hashlib import sha256

class Patient:
    def __init__(self, name:str, pos_times:list[int, ]) -> None:
        """
        Representation of a patient.
        name: str: Name of the patient. Should only be used with "UTF-8" encoding
        pos_times: list[int,]: The patient has a number of possible hours, s/he 
                               can attend to. The integers are the IDs of the Hour.
        """
        self.name = name
        self.pos_times = pos_times
        self.ID = sha256(self.name.encode("utf-8")).hexdigest()
                              
    def __str__(self) -> str:
        return  f'Patient: {self.name}; {self.pos_times}'
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Patient):
            return self.ID == value.ID
        else:
            raise ValueError(f"Cannot compare type {type(value)} to type Patient")