from flask_restful import Resource, reqparse
import sqlite3


def normalize_path(value_min=0.0,
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


def get_data_coins():
    args = reqparse.RequestParser()
    args.add_argument("value_min", type=float, default=0, location="args")
    args.add_argument("value_max", type=float, default=1000, location="args")
    args.add_argument("conservation_state", type=str, default=None, location="args")
    args.add_argument("country", type=str, default=None, location="args")
    args.add_argument("year_min", type=int, default=0, location="args")
    args.add_argument("year_max", type=int, default=2022, location="args")
    args.add_argument("limit", type=float, default=50, location="args")
    args.add_argument("offset", type=float, default=0, location="args")

    return args.parse_args()


def get_query(params):
    if params.get('conservation_state') and params.get('country'):
        return "SELECT * FROM coins WHERE (value >= ? and value <= ?) and conservation_state ? and country ? "\
                "and (year >= ? and year <= ?) LIMIT ? OFFSET ? "
    elif params.get('conservation_state'):
        return "SELECT * FROM coins WHERE (value >= ? and value <= ?) and conservation_state ? and (year >= ? and " \
                "year <= ?) LIMIT ? OFFSET ? "
    elif params.get('country'):
        return "SELECT * FROM coins WHERE (value >= ? and value <= ?) and country ? and (year >= ? and year <= ?) " \
                "LIMIT ? OFFSET ? "
    else:
        return "SELECT * FROM coins WHERE (value >= ? and value <= ?) and (year >= ? and year <= ?) LIMIT ? OFFSET ? "


def result_to_json(result):
    coins = []
    for linha in result:
        coins.append({
            'coin_id': linha[0],
            'description': linha[1],
            'value': linha[2],
            'conservation_state': linha[3],
            'country': linha[4],
            'year': linha[5]
        })

    return {'coins': coins}


class Coins(Resource):
    @classmethod
    def get(cls):
        connection = sqlite3.connect('coin_database.db')
        cursor = connection.cursor()

        data = get_data_coins()
        # get only data valide
        data_valide = {key: data[key] for key in data if data[key] is not None}
        params = normalize_path(**data_valide)
        query = get_query(params)
        tuple_params = tuple([params[key] for key in params])
        query_result = cursor.execute(query, tuple_params)
        result = result_to_json(result=query_result)

        return result
