
__Patient Manager__

The program is made for organizations, which have weakly repeating appointments with patients.


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

    Microsoft may be an ass and stop that due it thinking any script that exits shall be malware. In that case you can try to force them to do it by running:
    ```
    Set-ExecutionPolicy Unrestricted -Scope Process
    ```

__Setup:__

* Before running it the first time, you need to setup your work hours. It may be a bit complicate, but there is an improvement planned for version 1.1.0. 
But for now please do the following:

    __open manager/config/hours.json__

    Enter all of your Hours you offer here.
    With installation there is are hours added as a baseline for what you need to do, but here is the base structure:


    ```
    {
        "Monday" : [
            {"time":"0700",
            duration:50},
            {"time":"0800",
            duration:50},
            
        ],
        "Tuesday " : [],
        ...
    }
    ```

    "time" is a four letter long string with the first two the hour, the last two the minutes.

    "duration" is how long the hour is.


__Run:__

* Linux

    ```
    python3 manager 
    ```
* Windows:

    ```
    python manager 
    ```

__Bugs:__
    
* The patients, which are shown in the window are different than the patients in the weekly plan:

    It may be that the stored plan is out of date and cannot be updated.

    *Fix:*
    
    Go into the folder :manager/config/ and delete the plan.json file.

    If that didn't fixed it, you may need to delete the content of the /patient.json file also and replace it with "[ ]". 
    As you will lose all data of the patients, you may want to make a backup, so you can redo your work.
    
* Program gets stuck after clicking "Find all solutions"

    Program refuses to react to interaction; your OS may even say the app isn't responding anymore.

    Problem:

    Due to the exponential runtime of the function the function takes a very long time to find the nest solution. If you experience this behavior please try one of the following fixes:

    Fixes:

    * Reduce the number of patients, well obvious not always reasonable

    * Using the "Find Evo answers" Button. This Button executes an optimized function to find a reasonable good solution. It may not be the absolute best, but most of the time good enough