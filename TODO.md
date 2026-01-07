[x] **Create scripts folder and update the README.md and SESSION_STATE.md to reflect the change**.

[x] **In the script folder create a new python script loading_data.py**.

[x] **loading_data.py** script will load the data at the -8 quality mark. The number of time steps is 10312. Create a global variable named QUALITY for quality and NUMBER_OF_TIME_STEPS so I can change them before rerunning the script. The script will load the salinity data in a limited range, as was done in the LLC4320_metadata.ipynb. Look at the functions in this notebook and implement loading of the timesteps data at the quality speicifed for the limited range of langitude and latitude specified. After loading the data save it into the data folder. Do not run the script, as we will see how much space the data will take up. Also create a range of the depth we want to load.


[x] **Set up Flask server**: Create Flask API server structure with endpoints to access LLC4320 data. Server should load data directly from OpenVisus servers (not local files) and provide RESTful API for frontend access.

[x] **Create frontend test page**: Build simple HTML test interface to verify Flask API is sending data correctly. Include forms for testing metadata, data slices, and coordinates endpoints.

[x] Remove the get coordinates api call. We should NOT expose this data, as it is big. 150MB big. If user queried the whole coordinates transformation map, the website would lag, as it would need to get 150MB of data.

[x] update the README.md to reflect the current structure changes

[x] reason how we could host this server on the internet. Can flask host this on the internet for us?

[x] **Add data visualization to frontend**: Implement interactive heatmap visualization using Plotly.js to display fetched 2D data slices with geographic coordinates, colorbar, and hover tooltips. Support both array and base64 data formats.

[x] **Fix stack overflow error**: Replace `.flat()` and spread operators with iterative functions for processing large coordinate arrays to prevent "Maximum call stack size exceeded" errors.

