def normalize_path_coins(value_min=0.0,
                   value_max=1000.0,
                   conservation_state=None,
                   country=None,
                   year_min=0,
                   year_max=2022,
                   limit=50,
                   offset=0,
                   **dados):

    normalized_result = {'value_min': value_min, 'value_max': value_max}

    if conservation_state and country:
        normalized_result['conservation_state'] = conservation_state
        normalized_result['country'] = country
    if conservation_state:
        normalized_result['conservation_state'] = conservation_state
    if country:
        normalized_result['country'] = country

    normalized_result['year_min'] = year_min
    normalized_result['year_max'] = year_max
    normalized_result['limit'] = limit
    normalized_result['offset'] = offset

    return normalized_result


def get_query(params):
    query = "SELECT * FROM coins WHERE (value >= ? and value <= ?) "
    if params.get('conservation_state'):
        query += "and (conservation_state = ?) "
    if params.get('country'):
        query += "and (country = ?) "
    query += "and (year >= ? and year <= ?) LIMIT ? OFFSET ?"

    return query

