
class Hour:
    def __init__(self, ID:int, time:str, duration:int):
        """
        Implemenatation of the time unit, which can be taken by a Patient.
        ID: int: Unique indentification of the hour. Is made up of an 8-Bit integer.
                 The first 4 bits define the day, the latter 4 the unique ID of the hour on this day
        time: str: When does the hour start. ex "0750"
        duration: int: How long the hour is in minutes 
        """
        self.ID = ID
        self.time = time
        self.duration = duration
        self.taken_by = None