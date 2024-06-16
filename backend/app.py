from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import pymysql.cursors
from dotenv import load_dotenv
from os import getenv


# Create an instance of the application Flask
app = Flask(__name__)
CORS(app)  # Allow http requests

# Constants
# Load the variables from the .env file.
load_dotenv()

DATABASE_HOST = getenv("DATABASE_HOST")
DATABASE_NAME = getenv("DATABASE_NAME")
DATABASE_USER = getenv("DATABASE_USER")
DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")


def fix_region_name(region):
    if region == "":
        return "WORLD"
    country = region.upper()

    if country.startswith('E'):
        country = "EUR"
    elif country.startswith('J'):
        country = "JPN"
    elif country.startswith('U'):
        country = "USA"
    elif country.startswith('S'):
        country = "ESP"
    return country

# Defines an url or endpoint (it can be whatever you want) and the function name (Search, insert, delete...). This endpoint will recieve the input JSON, that's why it's a POST. POST method can only recieve


@app.route('/search', methods=['POST'])
# @cross_origin() # If you want CORS in this endpoint only
def search():
    # Input JSON
    # {
    # 	"game_name": "",
    # 	"game_platform": ""
    # }

    # Output JSON
    # [
    # 	{
    # 		"game_code": 0,
    # 		"game_language": "",
    # 		"game_name": "",
    # 		"game_platform": "",
    # 		"game_region": ""
    # 	}
    # ]

    # Get the JSON data recieved from the website
    data = request.get_json()

    # Access to the fields: 'game_name' and 'game_platform'
    game_name = data['game_name']
    game_platform = data['game_platform']

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    if game_name != "" and game_platform != "":
        # Query when the user enters the game title and the game platform
        query = f"select game.*, platform.name as 'platform' from game inner join has using (game_code) inner join platform on has.platform_name = platform.name where (game.name LIKE '{game_name}%' or game.name LIKE '%{game_name}%' or game.name = '{game_name}') and platform.name = '{game_platform}'"
        # Run the query
        cursor.execute(query)
        # Obtaining the data from the table
        game_data = cursor.fetchall()

    elif game_name != "" and game_platform == "":
        # Query when the user enters the game title but not the game platform
        query = f"select game.*, platform.name as 'platform' from game inner join has using (game_code) inner join platform on platform.name = has.platform_name where game.name LIKE '{game_name}%' OR game.name LIKE '%{game_name}%' OR game.name = '{game_name}'"
        cursor.execute(query)
        # Obtaining the data from the table
        game_data = cursor.fetchall()

    elif game_name == "" and game_platform != "":
        # Query when the user enters the game platform but not the game title
        query = f"select game.*, platform.name as 'platform' from game inner join has using (game_code) inner join platform on platform.name = has.platform_name where platform.name = '{game_platform}'"
        cursor.execute(query)
        # Obtaining the data from the table
        game_data = cursor.fetchall()

    # Query when nor the game title nor the game platform is entered
    elif game_name == "" and game_platform == "":
        game_data = "No game or platform found"

    # Close the connection
    cursor.close()
    connection.close()

    # Add the game_ prefix to each field but game_code
    renamed_list = [{'game_' + key if key != 'game_code' else key: value for key,
                     value in item.items()} for item in game_data]

    # Returns an answer
    return jsonify(renamed_list)


@app.route('/insert', methods=['POST'])
def insert():
    # Input JSON
    # {
    # 	"game_name": "",
    # 	"game_region": "",
    # 	"game_language": "",
    # 	"game_platform": ""
    # }

    # Get the JSON data recieved from the website
    data = request.get_json()

    # Access to the fields: 'game_name', 'game_region', and 'game_language'
    game_name = data['game_name'].replace("'", "\\'")
    # Fix the region name of the game file, before check it on the database
    game_region = fix_region_name(data['game_region'])
    game_language = data['game_language']
    if game_language == "":
        game_language = "None"
    game_platform = data['game_platform']

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query that returns the game and its info stored to check if it exists already in the database
    query = f"select * from game where name LIKE '%{game_name}%' and region = '{game_region}' and language = '{game_language}'"
    cursor.execute(query)
    game_db_result = cursor.fetchone()
    # Turn the result into a Boolean
    game_db_exists = bool(game_db_result)

    # If exists in the database (using its code to run the query), return the platform
    if game_db_exists and game_db_result['game_code']:
        # Query that returns the game platform
        query = f"select platform.name from platform inner join has on platform.name = has.platform_name inner join game on game.game_code = has.game_code where game.game_code = '{game_db_result['game_code']}'"
        cursor.execute(query)
        game_db_result['platform'] = cursor.fetchone().get(
            'name')  # Save the platform name

    insert = False
    if not game_db_exists:
        insert = True
    elif game_db_exists and game_region != game_db_result['region']:
        insert = True
    elif game_db_exists and game_platform != game_db_result['platform']:
        insert = True

    if insert:
        # SQL insert query into the GAME table using the procedure
        sql_insert_query_game = f"insert into game (name, region, language) values ('{game_name}', '{game_region}', '{game_language}')"
        cursor.execute(sql_insert_query_game)

        # Query to get the game code from the database and add it to the table "HAS" along with the platform
        query = f"select game_code from game where name = '{game_name}' and region = '{game_region}' and language = '{game_language}'"
        cursor.execute(query)
        game_code = int(cursor.fetchone().get('game_code'))

        # SQL insert query into the HAS table using the procedure
        sql_insert_query_has = f"insert into has (game_code, platform_name) values ('{game_code}', '{game_platform}')"
        cursor.execute(sql_insert_query_has)

    # Connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Returns an answer
    return jsonify("OK.")


@app.route('/delete', methods=['POST'])
def delete():
    # Input JSON
    # {
    #   "game_code": 0,
    # 	"game_name": "",
    # 	"game_region": "",
    # 	"game_language": "",
    # 	"game_platform": ""
    # }

    # Get the JSON data recieved from the website
    data = request.get_json()

    # Access to the fields: 'game_code' , 'game_name', 'game_region', and 'game_language', and 'game_platform'
    game_code = data['game_code']

    """ game_name = data['game_name']
    game_region = data['game_region']
    game_language = data['game_language']
    game_platform = data['game_platform'] """

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query that deletes the game
    query = f"delete from game where game_code = '{data['game_code']}'"
    cursor.execute(query)

    # Connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Returns an answer
    return jsonify("OK.")


@app.route('/update', methods=['POST'])
def update():
    # Input JSON
    # {
    #   "game_code": 0,
    # 	"game_name": "",
    # 	"game_region": "",
    # 	"game_language": "",
    # 	"game_platform": ""
    # }

    # Get the JSON data recieved from the website
    data = request.get_json()

    # Access to the fields: 'game_code' , 'game_name', 'game_region', and 'game_language', and 'game_platform'
    game_code = data['game_code']
    game_name = data['game_name']
    game_region = data['game_region']
    game_language = data['game_language']
    game_platform = data['game_platform']

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query that updates the game if the user wants to change the name of the game
    if game_name != "":
        query = f"update game set name = '{game_name}' where game_code = '{data['game_code']}'"
        cursor.execute(query)

    # Query that updates the game if the user wants to change the region of the game
    if game_region != "":
        query = f"update game set region = '{game_region}' where game_code = '{data['game_code']}'"
        cursor.execute(query)

    # Query that updates the game if the user wants to change the language of the game
    if game_language != "":
        query = f"update game set language = '{game_language}' where game_code = '{data['game_code']}'"
        cursor.execute(query)

    # Query that updates the platform if the user wants to change the platform of the game
    if game_platform != "":
        query = f"update has set platform_name = '{game_platform}' where game_code = '{data['game_code']}'"
        cursor.execute(query)

    # Connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Returns an answer
    return jsonify("OK.")


# Get method does not need any json input
@app.route('/getGames', methods=['GET'])
def getGames():

    # Output JSON
    # [
    # 	{
    # 		"game_code": 0,
    # 		"game_language": "",
    # 		"game_name": "",
    # 		"game_platform": "",
    # 		"game_region": ""
    # 	}
    # ]

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query to get all the game data from the database
    query_get_all_game_data = "select game.*, platform.name as 'platform' from game inner join has using (game_code) inner join platform on has.platform_name = platform.name"
    # Run the query
    cursor.execute(query_get_all_game_data)
    # Obtaining all the data from the database
    game_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    # Add the game_ prefix to each field but game_code
    renamed_list = [{'game_' + key if key != 'game_code' else key: value for key,
                     value in item.items()} for item in game_data]

    # Returns an answer
    return jsonify(renamed_list)

# Get method does not need any json input


@app.route('/getRegions', methods=['GET'])
def getRegions():

    # Output JSON
    # [
    # 	{
    # 		"game_region": ""
    # 	}
    # ]

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query to get all the game data from the database
    query_get_all_game_data = "select distinct(region) from game"
    # Run the query
    cursor.execute(query_get_all_game_data)
    # Obtaining all the data from the database
    game_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    # Add the game_ prefix to each field but game_code
    renamed_list = [{'game_' + key if key != 'game_code' else key: value for key,
                     value in item.items()} for item in game_data]

    # Returns an answer
    return jsonify(renamed_list)


@app.route('/getPlatforms', methods=['GET'])
def getPlatforms():

    # Output JSON
    # [
    # 	{
    # 		"game_platform": ""
    # 	}
    # ]

    # Connect to the database
    connection = pymysql.connect(host=DATABASE_HOST,
                                 user=DATABASE_USER,
                                 password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # Query to get all the game data from the database
    query_get_all_game_data = "select name as 'platform' from platform"
    # Run the query
    cursor.execute(query_get_all_game_data)
    # Obtaining all the data from the database
    game_data = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    # Add the game_ prefix to each field but game_code
    renamed_list = [{'game_' + key if key != 'game_code' else key: value for key,
                     value in item.items()} for item in game_data]

    # Returns an answer
    return jsonify(renamed_list)


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
