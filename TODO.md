[x] **Build initial SESSION_STATE.md**: look through the files and create your initial session state of what you percieve we have

[x] **Plan the structure of the project**: reason and come up with 2 plans of how to tidy the files to get a functional and readable environment. Create a plan a structure that reflects what this project is.

[x] **Format the directory as stated in the PROJECT_STRUCTURE_PLANS.md under the plan 1**

[x] **Updating paths in documentation**: update the cursor commands and rules to reflect the change in directories.

[x] **Update README.md paths to reflect new structure**

[x] **Update installation.md references**

[x] **Update `.gitignore` to reflect new data location**

[x] **Update the SESSION_STATE.md with a section "Project Map"**: this section depicts whre the model should find files. It gives the model the "big picture" of the file system. It tells the model where to place any new files if it should create them.

[x] **Research the ieee_scivis_llc4320.ipynb file**: find out how the data is presented and accessed. What data can we get from the end point and how we could process it to use it with this paper: https://www.allnans.com/jekyll/update/2018/04/04/beautiful-streamlines.html. Present your findings into the ANALYSIS folder, where I can read it.


[x] **Create scripts folder and update the README.md and SESSION_STATE.md to reflect the change**.

[x] **In the script folder create a new python script loading_data.py**.

[x] **loading_data.py** script will load the data at the -8 quality mark. The number of time steps is 10312. Create a global variable named QUALITY for quality and NUMBER_OF_TIME_STEPS so I can change them before rerunning the script. The script will load the salinity data in a limited range, as was done in the LLC4320_metadata.ipynb. Look at the functions in this notebook and implement loading of the timesteps data at the quality speicifed for the limited range of langitude and latitude specified. After loading the data save it into the data folder. Do not run the script, as we will see how much space the data will take up. Also create a range of the depth we want to load.

[x] **Set up Flask server**: Create Flask API server structure with endpoints to access LLC4320 data. Server should load data directly from OpenVisus servers (not local files) and provide RESTful API for frontend access.

[x] **Create frontend test page**: Build simple HTML test interface to verify Flask API is sending data correctly. Include forms for testing metadata, data slices, and coordinates endpoints.

