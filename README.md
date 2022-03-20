International Space Station Positional and Sighting Data
========================================================
NASA estimates data about the position and local sightings of the International Space Station (ISS) based on its trajectory as it orbits Earth. The purpose of this project is to use Docker to containerize a Flask application to easily retrieve this positional and sighting data for the ISS. Positional data is organized by epochs where each epoch has specific positional data. Sighting data is organized by location where each sighting is at a location that has a country, region, and city and each sighting has specific data about the ISS. The Flask application allows the user to narrow their search to easily retrieve information from the data sets.

Download Positional and Sighting Data
-------------------------------------
1. Navigate to `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq` if you would like to see the data in a browser.

2. Login to the TACC computer and download the positional data by typing `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml` into the terminal.

3. Download the sightings data by typing `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA11.xml` into the terminal.

Build a Container from Dockerfile
---------------------------------
1. To containerize the file using Docker, it is standard practice for the user to create a file describing the required libraries and packages. In your command line, create a txt file called requirements.txt by typing `vi requirements.txt`. In the requirements.txt file, press `i` and type `Flask=2.0.3`. Save the file by pressing `Esc` and typing `:wq`.

2. Build the docker image by typing `docker build -t <username>/<file-name>:latest .` into the terminal

3. Push the docker image by typing `docker push <username>/<file-name>:latest` into the terminal.

Pull a Working Container from Docker
------------------------------------
1. Pull a working container by typing `docker pull <username>/<file-name>:latest` into the terminal.

Instructions to Interact With All Routes Using curl
---------------------------------------------------
1. Type `curl localhost:5016/interact` to see a list of routes to interact with the application.

2. Type `curl localhost:5016/load_data -X POST` to load the positional and sighting data. This must be done before you can interact with any of the other routes.

3. Type `curl localhost:5016/epoch` to return a string of all epochs. Each line that is returned is the name of an epoch.

4. Type `curl localhost:5016/epoch/<epoch-name>` to return a dictionary of the information about a specific epoch. The dictionary has keys that represent the type of information, where the value is the value of that specific piece of information. For example, `curl localhost:5016/epoch/2022-057T12:00:00.000Z` returns:

{
  "X": {
    "#text": "6626.5027288478996",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-0.48760287876274999",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-824.23928357807699",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "4.9312583060242199",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-1255.3633426653601",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-5.8454326130222896",
    "@units": "km/s"
  }
}

where the "#text" is the value and "@units" is the units. In this case, the X coordinate is at about 6626.5 km.

5. Type `curl localhost:5016/countries` returns a dictionary of all countries and how many sightings occurred in that city.

6. Type `curl localhost:5016/countries/<specific-country>` returns a dictionary of all sightings in that specific country.

7. Type `curl localhost:5016/countries/<specific-country>/regions` returns a dictionary containing all regions and how many sightings occurred in that city.

8. Type `curl localhost:5016/countries/<specific-country>/regions/<specific-region>` returns a dictionary of all sightings in that specific country and region.

9. Type `curl localhost:5016/countries/<specific-country>/regions/<specific-region>/cities` returns a dictionary of all cities and how many sightings occurred in that city.

10. Type `curl localhost:5016/countries/<specific-country>/regions/<specific-region>/cities/<specific-city>` returns a dictionary of all sightings in that specific country, region, and city. For example, `curl localhost:5016/countries/United_States/regions/Wyoming/cities/Basin`

{
  "United_States, Wyoming, Basin": [
    {
      "city": "Basin",
      "country": "United_States",
      "duration_minutes": "5",
      "enters": "10 above S",
      "exits": "10 above E",
      "max_elevation": "22",
      "region": "Wyoming",
      "sighting_date": "Fri Feb 18/06:00 AM",
      "spacecraft": "ISS",
      "utc_date": "Feb 18, 2022",
      "utc_offset": "-7.0",
      "utc_time": "13:00"
    },
    {
      "city": "Basin",
      "country": "United_States",
      "duration_minutes": "3",
      "enters": "10 above SSE",
      "exits": "10 above ESE",
      "max_elevation": "13",
      "region": "Wyoming",
      "sighting_date": "Sat Feb 19/05:13 AM",
      "spacecraft": "ISS",
      "utc_date": "Feb 19, 2022",
      "utc_offset": "-7.0",
      "utc_time": "12:13"
    },

This snip shows the first two sightings. The key is the location (United States, Wyoming, Basin) and the value is all the sightings that occurred in Basin and the data for each sighting.

Alternate Instructions Using Makefile
-------------------------------------
Another way to run Flask using the container is to use the existing Makefile in the repository.


