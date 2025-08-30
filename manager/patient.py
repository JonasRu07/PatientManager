class Patient:
    def __init__(self, name:str, pos_times:list[int, ]):
        """
        Representation of a patient.
        name: str: Name of the patient. Should only be used with "UTF-8" encoding
        pos_times: list[int,]: The patient has a number of possible hours, s/he 
                               can attend to. The integers are the IDs of the Hour.
        """
        self.name = name
        self.pos_times = pos_times