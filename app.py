from flask import Flask
import logging
import xmltodict

app = Flask(__name__)

positional_data = {}
sighting_data = {}

@app.route('/load_data', methods=['POST'])
def load_data():
    """
    Loads information on ISS position and sightings.

    Returns:
        string that states that the data has been loaded.
    """
    logging.info('Reading in ISS data')

    global positional_data
    global sighting_data

    with open('ISS.OEM_J2K_EPH.xml', 'r') as f:
        positional_data = xmltodict.parse(f.read())

    with open('XMLsightingData_citiesUSA11.xml', 'r') as f:
        sighting_data = xmltodict.parse(f.read())

    return f'Data loaded from file to dictionary.\n'



@app.route('/interact', methods=['GET'])
def interact():
    """
    Outputs information on how to interact with the application.

    Returns:
        ret (str): how to interact with the application
    """
    logging.info('How to interact with the application')
    ret = "How to interact with the application:\n"
    ret += "curl localhost:<port number>/interact                                             (GET) prints this information\n"
    ret += "curl localhost:<port number>/load_data -X POST                                    (POST) reads in the ISS data from files for position and sighting\n"
    ret += "curl localhost:<port number>/epoch                                                (GET) returns all Epochs in the positional data\n"
    ret += "curl localhost:<port number>/epoch/<epoch>                                        (GET) returns information about a specific Epoch in the positional data\n"
    ret += "curl localhost:<port number>/countries                                            (GET) returns all Countries in the sighting data\n"
    ret += "curl localhost:<port number>/countries/<country>                                  (GET) returns information about a specific Country in the sighting data\n"
    ret += "curl localhost:<port number>/countries/<country>/regions                          (GET) returns all Regions in a specific Country in the sighting data\n"
    ret += "curl localhost:<port number>/countries/<country>/regions/<region>                 (GET) returns information about a specific Region in a specific Country in the sighting data\n"
    ret += "curl localhost:<port number>/countries/<country>/regions/<region>/cities          (GET) returns all Cities in a specific Region in a specific Country in the sighting data\n"
    ret += "curl localhost:<port number>/countries/<country>/regions/<region>/cities/<city>   (GET) returns information about a specific City in a specific Region in a specific Country in the sighting data"
    return ret



@app.route('/epoch', methods=['GET'])
def all_epochs():
    """
    Outputs all Epochs in the positional data.

    Returns:
        ret (str): names of all epochs in the data
    """
    logging.info('Querying to return all Epochs.')
    ret = ""
    for i in range(len(positional_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        ret += positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return ret 



@app.route('/epoch/<epoch>', methods=['GET'])
def specific_epoch(epoch: str):
    """
    Outputs information about a specific Epoch in the positional data.
    
    Args:
        epoch (str): the name of the specific epoch
   
    Returns:
        ret_dict (dict): dictionary of information about a specific epoch
    """
    logging.info('Querying to return information about epoch ' + epoch)
    num = 0
    for i in range(len(positional_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        #return "This func\n"
        if epoch == positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            num = i
       # else:
       #     return 'This is not a valid Epoch.\n'
    ret_dict = {}
    ret_dict['X'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['X']
    ret_dict['Y'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['Y']
    ret_dict['Z'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['Z']
    ret_dict['X_DOT'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['X_DOT']
    ret_dict['Y_DOT'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['Y_DOT']
    ret_dict['Z_DOT'] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num]['Z_DOT']
    return ret_dict



@app.route('/countries', methods=['GET'])
def all_countries():
    """
    Outputs all Countries from the sighting data.

    Returns:
        ret_dict (dict): dictionary with all Countries and how many times they occur
    """
    logging.info('Querying to return all countries in sighting data')
    ret_dict = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        if sighting_data['visible_passes']['visible_pass'][i]['country'] in ret_dict:
            ret_dict[sighting_data['visible_passes']['visible_pass'][i]['country']] += 1    
        else:
            ret_dict[sighting_data['visible_passes']['visible_pass'][i]['country']] = 1
    return ret_dict
    


@app.route('/countries/<country>', methods=['GET'])
def specific_country(country: str):
    """
    Outputs information about a specific Country in the sighting data.
    
    Args:
        country (str): the name of the specific country

    Returns:
        ret_dict (dict): dictionary of information from a specific country
    """
    logging.info('Querying to return information about a specific Country: ' + country)
    ret_dict = {}
    list_dict = [] 
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        specific_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country == country:
            country_info_dict= {}
            country_info_dict['country']= sighting_data['visible_passes']['visible_pass'][i]['country']
            country_info_dict['region'] = sighting_data['visible_passes']['visible_pass'][i]['region']
            country_info_dict['city'] = sighting_data['visible_passes']['visible_pass'][i]['city']
            country_info_dict['spacecraft'] = sighting_data['visible_passes']['visible_pass'][i]['spacecraft']
            country_info_dict['sighting_date'] = sighting_data['visible_passes']['visible_pass'][i]['sighting_date']
            country_info_dict['duration_minutes'] = sighting_data['visible_passes']['visible_pass'][i]['duration_minutes']
            country_info_dict['max_elevation'] = sighting_data['visible_passes']['visible_pass'][i]['max_elevation']
            country_info_dict['enters'] = sighting_data['visible_passes']['visible_pass'][i]['enters']
            country_info_dict['exits'] = sighting_data['visible_passes']['visible_pass'][i]['exits']
            country_info_dict['utc_offset'] = sighting_data['visible_passes']['visible_pass'][i]['utc_offset']
            country_info_dict['utc_time'] = sighting_data['visible_passes']['visible_pass'][i]['utc_time']
            country_info_dict['utc_date'] = sighting_data['visible_passes']['visible_pass'][i]['utc_date']
            list_dict.append(country_info_dict)
    ret_dict[country] = list_dict
    return ret_dict


@app.route('/countries/<country>/regions', methods=['GET'])
def all_regions(country: str):
    """
    Outputs all Regions associated with a given Country in the sighting data.

    Args:
        country (str): the name of the specific country

    Returns:
        ret_dict (dict): dictionary of all the regions in the specific country with the value being the number of times they occur
    """
    logging.info('Querying to return all Regions in a certain Country.')
    ret_dict = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        specific_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country == country:
            specific_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if specific_region in ret_dict:
                ret_dict[specific_region] += 1
            else:
                ret_dict[specific_region] = 1
    return ret_dict



@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def specific_region(country: str, region: str):
    """
    Outputs information about a specific Region in the sighting data.

    Args:
        country (str): the name of the specific country
        region (str): the name of the specific region

    Returns:
        ret_dict (dict): dictionary with information about a specific region
    """
    logging.info('Querying to return information about a specific Region ' + region + ' and in a specific Country: ' + country)
    ret_dict = {}
    list_dict = [] 
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        specific_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country == country:
            specific_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if specific_region == region:
                region_info_dict= {}
                region_info_dict['country']= sighting_data['visible_passes']['visible_pass'][i]['country']              
                region_info_dict['region']= sighting_data['visible_passes']['visible_pass'][i]['region']
                region_info_dict['city'] = sighting_data['visible_passes']['visible_pass'][i]['city']
                region_info_dict['spacecraft'] = sighting_data['visible_passes']['visible_pass'][i]['spacecraft']
                region_info_dict['sighting_date'] = sighting_data['visible_passes']['visible_pass'][i]['sighting_date']
                region_info_dict['duration_minutes'] = sighting_data['visible_passes']['visible_pass'][i]['duration_minutes']
                region_info_dict['max_elevation'] = sighting_data['visible_passes']['visible_pass'][i]['max_elevation']
                region_info_dict['enters'] = sighting_data['visible_passes']['visible_pass'][i]['enters']
                region_info_dict['exits'] = sighting_data['visible_passes']['visible_pass'][i]['exits']
                region_info_dict['utc_offset'] = sighting_data['visible_passes']['visible_pass'][i]['utc_offset']
                region_info_dict['utc_time'] = sighting_data['visible_passes']['visible_pass'][i]['utc_time']
                region_info_dict['utc_date'] = sighting_data['visible_passes']['visible_pass'][i]['utc_date']
                list_dict.append(region_info_dict)
    ret_dict[country + ', ' + region] = list_dict
    return ret_dict



@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def all_cities(country: str, region: str):
    """
    Outputs all Cities associated with a given Country and Region in the sighting data.

    Args:
        country (str): the name of the specific country
        region (str): the name of the specific region

    Returns:
        ret_dict (dict): dictionary of all of the cities with the value being how many times they occur
    """
    logging.info('Querying to find all cities associated with a given Country and Region')
    ret_dict = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        specific_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country == country:
            specific_region = sighting_data['visible_passes']['visible_pass'][i]['region'] 
            if specific_region == region:
                specific_city = sighting_data['visible_passes']['visible_pass'][i]['city']
                if specific_city in ret_dict:
                    ret_dict[specific_city] += 1
                else:
                    ret_dict[specific_city] = 1
    return ret_dict



@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'])
def specific_city(country: str, region: str, city: str):
    """
    Outputs information about a specific City in the sighting data.
    
    Args:
        country (str): the name of the specific country
        region (str): the name of the specific region
        city (str): the name of the specific city

    Returns:
        ret_dict (dict): information about the specific City
    """
    logging.info('Querying to find information about City ' + city + ' in Region ' + region + ' in Country ' + country)
    ret_dict = {}
    list_dict = [] 
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        specific_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country == country:
            specific_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if specific_region == region:
                specific_city = sighting_data['visible_passes']['visible_pass'][i]['city']
                if specific_city == city:
                    city_info_dict= {}
                    city_info_dict['country']= sighting_data['visible_passes']['visible_pass'][i]['country']              
                    city_info_dict['region']= sighting_data['visible_passes']['visible_pass'][i]['region']
                    city_info_dict['city'] = sighting_data['visible_passes']['visible_pass'][i]['city']
                    city_info_dict['spacecraft'] = sighting_data['visible_passes']['visible_pass'][i]['spacecraft']
                    city_info_dict['sighting_date'] = sighting_data['visible_passes']['visible_pass'][i]['sighting_date']
                    city_info_dict['duration_minutes'] = sighting_data['visible_passes']['visible_pass'][i]['duration_minutes']
                    city_info_dict['max_elevation'] = sighting_data['visible_passes']['visible_pass'][i]['max_elevation']
                    city_info_dict['enters'] = sighting_data['visible_passes']['visible_pass'][i]['enters']
                    city_info_dict['exits'] = sighting_data['visible_passes']['visible_pass'][i]['exits']
                    city_info_dict['utc_offset'] = sighting_data['visible_passes']['visible_pass'][i]['utc_offset']
                    city_info_dict['utc_time'] = sighting_data['visible_passes']['visible_pass'][i]['utc_time']
                    city_info_dict['utc_date'] = sighting_data['visible_passes']['visible_pass'][i]['utc_date']
                    list_dict.append(city_info_dict)
    ret_dict[country + ', ' + region + ', ' + city] = list_dict
    return ret_dict






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
