
This is a program for solving the problem of having multiple Patients, which have weekly repeating appointments.
Each patients has a number of possible hours s/he can attend to. There are currently 2 algorithms to find solution.
The first one, only finds hours only one patient can attend to.
The second one solves for every possible solution and choses one. A solution is considered an arrangement of ALL patients. Due to the fact, that this algorithm is very! slow, I can only recommend it for a small number of patients.

If you encounter any issues with this program, you can leave a detailed description inside the issue page ([this link](https://github.com/JonasRu07/PatientManager/issues)).

Same can be done if there are any features, that you'd like to have


It was develop on:
* Linux (tested: Ubuntu 21.2)
* Windows 10 (limited)

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


