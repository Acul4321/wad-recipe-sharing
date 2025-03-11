COUNTRIES = {
    1: 'Afghanistan', 2: 'Albania', 3: 'Algeria', 4: 'Argentina',
    5: 'Australia', 6: 'Austria', 7: 'Belgium', 8: 'Brazil',
    9: 'Canada', 10: 'China', 11: 'Colombia', 12: 'Denmark',
    13: 'Egypt', 14: 'Finland', 15: 'France', 16: 'Germany',
    17: 'Greece', 18: 'India', 19: 'Indonesia', 20: 'Ireland',
    21: 'Italy', 22: 'Japan', 23: 'Mexico', 24: 'Netherlands',
    25: 'New Zealand', 26: 'Norway', 27: 'Pakistan', 28: 'Poland',
    29: 'Portugal', 30: 'Russia', 31: 'Saudi Arabia', 32: 'Singapore',
    33: 'South Africa', 34: 'Spain', 35: 'Sweden', 36: 'Switzerland',
    37: 'Thailand', 38: 'Turkey', 39: 'United Kingdom', 40: 'United States'
}

def get_country_name(country_id):
    return COUNTRIES.get(country_id)

def get_country_id(country_name):
    for country_id, name in COUNTRIES.items():
        if name.lower() == country_name.lower():
            return country_id
    return None