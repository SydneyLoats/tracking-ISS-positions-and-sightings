International Space Station Positional and Sighting Data
========================================================
NASA estimates data about the position and local sightings of the International Space Station (ISS) based on its trajectory as it orbits Earth. The purpose of this project is to use Docker to containerize a Flask application to easily retrieve this positional and sighting data for the ISS. Positional data is organized by epochs where each epoch has specific positional data. Sighting data is organized by location where each sighting is at a location that has a country, region, and city and each sighting has specific data about the ISS. The Flask application allows the user to narrow their search to easily retrieve information from the data sets.

# Download Positional and Sighting Data #
1. Navigate to `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq`

2. Download the positional data by typing `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml` into the terminal.

3. Download the sightings data by typing `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA11.xml` into the terminal.

