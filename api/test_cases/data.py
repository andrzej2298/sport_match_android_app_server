JOHNS_CREDENTIALS = {
    'username': 'John',
    'password': 'secret',
}

JOHN = {
    **JOHNS_CREDENTIALS,
    'email': 'john@example.com',
    'birth_date': '2020-02-06',
    'gender': 'M',
}

FOOTBALL = {
    'name': 'football'
}

JOHNS_FOOTBALL = {
    'level': 9,
    'user': 1,
    'sport': 1
}

MIM_COORDINATES = [
    52.211769,
    20.982064
]

MIM_WORKOUT = {
    'name': 'MIM',
    'location': {
        'type': 'Point',
        'coordinates': MIM_COORDINATES,
    },
    'level': 9,
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 1,
    'sport': 1
}

BITWY_WARSZAWSKIEJ_COORDINATES = [
    52.211858,
    20.977279
]

BITWY_WARSZAWSKIEJ_WORKOUT = {
    'name': 'Bitwy Warszawskiej',
    'location': {
        'type': 'Point',
        'coordinates': BITWY_WARSZAWSKIEJ_COORDINATES,
    },
    'level': 9,
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 1,
    'sport': 1
}

