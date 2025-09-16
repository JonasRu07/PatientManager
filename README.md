
This is a program for solving the problem of having multiple Patients, which have weekly repeating appointments.

This is the GUI-Branch. The base control over the algorithms are implemented in the UI, but changing the data (hours and/or patients) may still require manual changes in the config files. 
If done a restart of the UI is needed to reload the data. 

Tested and developed on:
    Linux (tested: Ubuntu 21.2)
    Windows 10

__Installation:__

* Linux:
    ```
    git clone https://github.com/JonasRu07/PatientManager.git
    cd ./PatientManager
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -e .
    ```

* Windows:

    ```
    git clone https://github.com/JonasRu07/PatientManager.git
    cd PatientManager
    python -m venv .venv
    .venv\scripts\activate
    python -m pip install -e .
    ```

__Setup:__

* In the path PatientManager/manager/config are 2 file. 

    __hours.json__

    Enter all of your Hours you offer here.
    With installation there is are hours added as a baseline for what you need to do, but here is the base structure:


    ```
    {
        "Monday" : [
            {"time":"0700",
            duration:50},
            {"time":"0700",
            duration:50},
            
        ],
        "Tuesday " : [],
        ...
    }
    ```

    time is a for letter long string with the first two the hour, the last   two the minutes
    duration is how long the hour is
    The order the days, or the hours on each day is not important, but it makes it easier to fill out the patients
    and is later in the README assumed to be for each day from earliest to latest
    
    __patients.json:__

    Enter all patient you have here
    With installation there is are hours added as a baseline for what you need to do, but here is the base structure:

    ```
    [
        {
            "name":"Name of patient",
            "possible hours" : [0, 2, 16, 72]
        },
         {
             "name":"Name of patient",
             "possible hours" : [0, 2, 16, 72]
         },
         ...
    ]
    ```

    name is simply the name of the patient
    possible hours is a list [] of all hours the patient can attend to.
    The hours are defined with integers, later called IDs
    The ID is calculated by the day (Mo -> 0, Tu -> 16, We -> 32, ...) and the number of what hour is it on that day.
    And yes, I start counting at 0 ; )

    Example:
    
    You have Thursday 4 Hours, and Peter can come to the second. Than the ID you need to enter is 49
    (48, because Thursday is 48, + 1, because it is the second hour of the day)




__Run:__

* Linux

    ```
    python3 manager 
    ```
* Windows:

    ```
    python manager 
    ```


