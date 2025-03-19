COUNTRIES = {
    1: 'Afghanistan', 2: 'Albania', 3: 'Algeria', 4: 'Andorra', 
    5: 'Angola', 6: 'Argentina', 7: 'Armenia', 8: 'Australia', 
    9: 'Austria', 10: 'Azerbaijan', 11: 'Bahamas', 12: 'Bahrain', 
    13: 'Bangladesh', 14: 'Barbados', 15: 'Belarus', 16: 'Belgium', 
    17: 'Belize', 18: 'Benin', 19: 'Bhutan', 20: 'Bolivia', 
    21: 'Bosnia and Herzegovina', 22: 'Botswana', 23: 'Brazil', 24: 'Brunei',
    25: 'Bulgaria', 26: 'Burkina Faso', 27: 'Burundi', 28: 'Cambodia',
    29: 'Cameroon', 30: 'Canada', 31: 'Chad', 32: 'Chile',
    33: 'China', 34: 'Colombia', 35: 'Comoros', 36: 'Congo',
    37: 'Costa Rica', 38: 'Croatia', 39: 'Cuba', 40: 'Cyprus',
    41: 'Czech Republic', 42: 'Denmark', 43: 'Djibouti', 44: 'Dominica',
    45: 'Dominican Republic', 46: 'Ecuador', 47: 'Egypt', 48: 'El Salvador',
    49: 'Eritrea', 50: 'Estonia', 51: 'Ethiopia', 52: 'Fiji',
    53: 'Finland', 54: 'France', 55: 'Gabon', 56: 'Gambia',
    57: 'Georgia', 58: 'Germany', 59: 'Ghana', 60: 'Greece',
    61: 'Grenada', 62: 'Guatemala', 63: 'Guinea', 64: 'Guinea-Bissau',
    65: 'Guyana', 66: 'Haiti', 67: 'Honduras', 68: 'Hungary',
    69: 'Iceland', 70: 'India', 71: 'Indonesia', 72: 'Iran',
    73: 'Iraq', 74: 'Ireland', 75: 'Israel', 76: 'Italy',
    77: 'Jamaica', 78: 'Japan', 79: 'Jordan', 80: 'Kazakhstan',
    81: 'Kenya', 82: 'Kiribati', 83: 'Kuwait', 84: 'Kyrgyzstan',
    85: 'Laos', 86: 'Latvia', 87: 'Lebanon', 88: 'Lesotho',
    89: 'Liberia', 90: 'Libya', 91: 'Liechtenstein', 92: 'Lithuania',
    93: 'Luxembourg', 94: 'Madagascar', 95: 'Malawi', 96: 'Malaysia',
    97: 'Maldives', 98: 'Mali', 99: 'Malta', 100: 'Mauritania',
    101: 'Mauritius', 102: 'Mexico', 103: 'Moldova', 104: 'Monaco',
    105: 'Mongolia', 106: 'Montenegro', 107: 'Morocco', 108: 'Mozambique',
    109: 'Myanmar', 110: 'Namibia', 111: 'Nepal', 112: 'Netherlands',
    113: 'New Zealand', 114: 'Nicaragua', 115: 'Niger', 116: 'Nigeria',
    117: 'North Korea', 118: 'Norway', 119: 'Oman', 120: 'Pakistan',
    121: 'Panama', 122: 'Papua New Guinea', 123: 'Paraguay', 124: 'Peru',
    125: 'Philippines', 126: 'Poland', 127: 'Portugal', 128: 'Qatar',
    129: 'Romania', 130: 'Russia', 131: 'Rwanda', 132: 'Samoa',
    133: 'San Marino', 134: 'Saudi Arabia', 135: 'Senegal', 136: 'Serbia',
    137: 'Seychelles', 138: 'Sierra Leone', 139: 'Singapore', 140: 'Slovakia',
    141: 'Slovenia', 142: 'Solomon Islands', 143: 'Somalia', 144: 'South Africa',
    145: 'South Korea', 146: 'South Sudan', 147: 'Spain', 148: 'Sri Lanka',
    149: 'Sudan', 150: 'Suriname', 151: 'Sweden', 152: 'Switzerland',
    153: 'Syria', 154: 'Taiwan', 155: 'Tajikistan', 156: 'Tanzania',
    157: 'Thailand', 158: 'Togo', 159: 'Tonga', 160: 'Trinidad and Tobago',
    161: 'Tunisia', 162: 'Turkey', 163: 'Turkmenistan', 164: 'Tuvalu',
    165: 'Uganda', 166: 'Ukraine', 167: 'United Arab Emirates', 168: 'United Kingdom',
    169: 'United States', 170: 'Uruguay', 171: 'Uzbekistan', 172: 'Vanuatu',
    173: 'Vatican City', 174: 'Venezuela', 175: 'Vietnam', 176: 'Yemen',
    177: 'Zambia', 178: 'Zimbabwe'
}

# ...existing code...

def get_country_name(country_id):
    return COUNTRIES.get(country_id)

def get_country_id(country_name):
    for country_id, name in COUNTRIES.items():
        if name.lower() == country_name.lower():
            return country_id
    return None