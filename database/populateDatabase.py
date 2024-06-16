# Necessary to have MySQL controller instaled using the command: pip install mysql-connector-python, check the version of Python that is installed, because instead of pip it can be pip3

import re
import os

import pymysql
import pymysql.cursors

from log import Log  # From log.py file give me the Log class

# The directory path with the files. The last element (the name of the platform) has to be changed when using the script with a different platform
directory_path = "/Volumes/games/roms/preserved/psp"
# directory_path = "/Users/sara/Downloads/test/roms/gamecube"
# Where the game data will be saved
files = []
# The variable that contains the name of the platform using the directory path. Returns the last element of the route, so the platform has always to be the last element
game_disk_platform = os.path.basename(os.path.normpath(directory_path))

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345678',
                             database='games',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# For each element in the directory path, if it is a file, then add it to the list "files"
# Version 1
# for item in os.listdir(directory_path):
#     item_path = os.path.join(directory_path, item)
#     if os.path.isfile(item_path) and not item.startswith('.'):
#         files.append(item)
# Version 2
for item in os.listdir(directory_path):
    if item.startswith('.') is True:
        continue

    file_name = ''
    item_path = os.path.join(directory_path, item)
    if os.path.isfile(item_path):
        file_name, _ = os.path.splitext(item)  # Remove extension on files
    else:
        file_name = item
    files.append(file_name)

# This variable contains the regular expression
# regex = r"^(.*?)\s*(?:\((.*?)\))?(?:\s*\((.*?)\))?\..*?$"
regex = r"^(.*?)\s*(?:\((.*?)\))?\s*(?:\((.*?)\))?$"


def fix_region_name(region):
    if region is None:
        return "WORLD"
    country = region.lower()

    if country.startswith('e'):
        country = "EUR"
    elif country.startswith('j'):
        country = "JPN"
    elif country.startswith('u'):
        country = "USA"
    elif country.startswith('s'):
        country = "ESP"
    return country


# Adding the files to the database
with connection:
    with connection.cursor() as cursor:
        # Create a new record. For each file in the list "files", if it matches the regular expression then add the name to the table "game"
        for file in files:
            match = re.search(regex, file)
            if match:
                game_disk_name = match.group(1).replace("'", "\\'")
                # Fix the region name of the game file, before check it on the database
                game_disk_region = fix_region_name(match.group(2))
                game_disk_language = match.group(3)
                if game_disk_language is None:
                    game_disk_language = "None"

                # Query that returns the game and its info stored to check if it exists already in the database
                query = f"select * from game where name = '{game_disk_name}' and region = '{game_disk_region}' and language = '{game_disk_language}'"
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
                elif game_db_exists and game_disk_region != game_db_result['region']:
                    insert = True
                elif game_db_exists and game_disk_platform != game_db_result['platform']:
                    insert = True

                if insert:
                    # SQL insert query into the GAME table using the procedure
                    sql_insert_query_game = f"call game_input ('{game_disk_name}', '{game_disk_region}', '{game_disk_language}')"
                    cursor.execute(sql_insert_query_game)

                    # Query to get the game code from the database and add it to the table "HAS" along with the platform
                    query = f"select game_code from game where name = '{game_disk_name}' and region = '{game_disk_region}' and language = '{game_disk_language}'"
                    cursor.execute(query)
                    game_code = int(cursor.fetchone().get('game_code'))

                    # SQL insert query into the HAS table using the procedure
                    sql_insert_query_has = f"CALL has_input('{game_disk_platform}', {game_code})"
                    cursor.execute(sql_insert_query_has)

                    # SQL query to get the total amount of games inserted
                    sql_message_total_games = f"select count(*) from game inner join has using (game_code) inner join platform on has.platform_name = platform.name where platform.name = '{game_disk_platform}'"
                    cursor.execute(sql_message_total_games)
                    result = cursor.fetchone()
                    total_games = int(result.get('count(*)'))

                    Log.info(
                        f"Total games inserted in {game_disk_platform}: {total_games}.")
                else:
                    Log.error(
                        f"The game {game_disk_name} ({game_disk_region}) ({game_disk_language}) has not been inserted: duplicated name and region.")

    # Connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
