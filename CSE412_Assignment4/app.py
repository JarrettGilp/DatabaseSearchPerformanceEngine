from flask import Flask, render_template, request
import psycopg2
import time
import os

app = Flask(__name__)

dbConnection = "dbname=example_database_name user=example_user_name password=example_password host=localhost port=5432"

# Database connection
def get_connection():
    return psycopg2.connect(dbConnection)

def run_query(cursor, query, params=None):
    start = time.time()
    cursor.execute(query, params)
    results = cursor.fetchall()
    end = time.time()
    exec_time = end - start
    colnames = [desc[0] for desc in cursor.description]
    return results, exec_time, colnames

def create_indexes(cursor):
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_games_title ON games(title);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customerName ON orders(customerName);")

def drop_indexes(cursor):
    cursor.execute("DROP INDEX IF EXISTS idx_games_title;")
    cursor.execute("DROP INDEX IF EXISTS idx_orders_customerName;")

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {
        'single_noidx': {'data': [], 'time': 0, 'cols': []},
        'join_noidx': {'data': [], 'time': 0, 'cols': []},
        'single_idx': {'data': [], 'time': 0, 'cols': []},
        'join_idx': {'data': [], 'time': 0, 'cols': []}
    }

    search_text = ""
    if request.method == 'POST':
        search_text = request.form.get('search_text', '')

        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Without Index
                drop_indexes(cursor)

                # Single table
                query = "SELECT * FROM games WHERE title ILIKE %s LIMIT 5"
                r, t, c = run_query(cursor, query, (f"%{search_text}%",))
                results['single_noidx'].update({'data': r, 'time': t, 'cols': c})

                # Join table
                query = """
                    SELECT g.title, g.publisher, o.customerName, o.orderDate, o.orderStatus
                    FROM games g
                    JOIN orders o ON g.gameID = o.gameID
                    WHERE g.title ILIKE %s OR o.customerName ILIKE %s
                    LIMIT 5
                """
                r, t, c = run_query(cursor, query, (f"%{search_text}%", f"%{search_text}%"))
                results['join_noidx'].update({'data': r, 'time': t, 'cols': c})

                # With Index
                create_indexes(cursor)

                # Single table
                query = "SELECT * FROM games WHERE title ILIKE %s LIMIT 5"
                r, t, c = run_query(cursor, query, (f"%{search_text}%",))
                results['single_idx'].update({'data': r, 'time': t, 'cols': c})

                # Join table
                query = """
                    SELECT g.title, g.publisher, o.customerName, o.orderDate, o.orderStatus
                    FROM games g
                    JOIN orders o ON g.gameID = o.gameID
                    WHERE g.title ILIKE %s OR o.customerName ILIKE %s
                    LIMIT 5
                """
                r, t, c = run_query(cursor, query, (f"%{search_text}%", f"%{search_text}%"))
                results['join_idx'].update({'data': r, 'time': t, 'cols': c})

    return render_template('index.html', results=results, search_text=search_text)

if __name__ == '__main__':
    app.run(debug=True)