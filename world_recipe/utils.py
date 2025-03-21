COUNTRIES = {
    1: 'Argentina',
    2: 'Australia',
    3: 'Belgium',
    4: 'Brazil',
    5: 'Canada',
    6: 'China',
    7: 'Colombia',
    8: 'Denmark',
    9: 'Egypt',
    10: 'Finland',
    11: 'France',
    12: 'Germany',
    13: 'Somalia',
    14: 'Algeria',
}

def get_country_name(country_id):
    return COUNTRIES.get(country_id)

def get_country_id(country_name):
    for country_id, name in COUNTRIES.items():
        if name.lower() == country_name.lower():
            return country_id
    return None