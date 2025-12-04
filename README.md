# Jarrett Mitchell - Assignment 4 Setup Instructions --- Games and Orders: Database Search Performance

### Steps for Setup ###

# Step 1: Create a virtual environment
#
#       Type into terminal:     python -m venv venv

# Step 2: Activate the venv
#
#       Type into terminal:     .\venv\Scripts\activate

# Step 3: Install Python dependencies
#
#       Type into terminal:     pip install flask psycopg2-binary faker

# Step 4: Setup pgAdmin database with the schema in schema.sql
#
#       Create a database in pgAdmin with any name and keep the database running.

# Step 5: Open up data_generation.py AND app.py

# Step 6: For BOTH files, edit the 'dbConnection' variable to have your name you picked for the database you created, as well as your   username and password for your server.
#
#       dbConnection = "dbname=<Your database name> user=<Your username (usually 'postgres')> 
#       password=<Your password> host=localhost port=5432"

# Step 7: Run data_generation.py to generate data to your database for 'games' and 'orders' tables.
#
#       Type into terminal:     python data_generation.py

# Step 8: Run app.py to deploy the site on localhost:5000
#
#       Type into terminal:     python app.py

# Step 9: Open the web application in browser
#
#       In browser, add to the address bar:     http://127.0.0.1:5000/

# Step 10: AFTER FINISHING - Deactivate venv
#
#	Type into terminal:	deactivate


### Usage ###

# Enter search text in the box relating to a game title from the 'games' table.

# Execution times will appear for:

#       Single table without index
#       Join table without index
#       Single table with index
#       Join table with index

# These appear in color coded boxes depending on if the query is related to 'without index' (blue) or 'with index' (green).

# Results table: 5 'games' search results will appear below the execution times with all ten columns pertaining to a game from the 'games' table.