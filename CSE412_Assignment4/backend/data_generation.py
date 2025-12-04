import psycopg2
import random, datetime
from faker import Faker
from datetime import timedelta

fake = Faker()

NUM_GAMES = 10000
NUM_ORDERS = 10000

dbConnection = "dbname=assignment4 user=postgres password=JarrettusKennedy host=localhost port=5432"

conn = psycopg2.connect(dbConnection)
cursor = conn.cursor()

genres = ['Action', 'Adventure', 'RPG', 'Strategy', 'Simulation', 'Sports', 'Puzzle']
platforms = ['PC', 'Xbox', 'PlayStation', 'Switch', 'Mobile']
esrb_ratings = ['E', 'E10+', 'T', 'M', 'AO']

print("Generating games...")
for _ in range(NUM_GAMES):
    title = fake.sentence(nb_words=3).replace('.', '')
    description = fake.text(max_nb_chars=200)
    publisher = fake.company()
    genre = random.choice(genres)
    player_count = random.randint(1, 100)
    price = round(random.uniform(10, 100), 2)
    release_year = random.randint(2000, 2025)
    esrb = random.choice(esrb_ratings)
    platform = random.choice(platforms)
    
    cursor.execute("""
        INSERT INTO games (title, description, publisher, genre, player_count, price, releaseYear, esrbRating, platform)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (title, description, publisher, genre, player_count, price, release_year, esrb, platform)
    )

conn.commit()
print("Games inserted.")

cursor.execute("SELECT gameID FROM games")
game_ids = [row[0] for row in cursor.fetchall()]

order_statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']

print("Generating orders...")
for _ in range(NUM_ORDERS):
    game_id = random.choice(game_ids)
    quantity = random.randint(1, 5)
    customer_name = fake.name()
    order_date = fake.date_between(start_date='-2y', end_date='today')
    shipping_date = order_date + timedelta(days=random.randint(1, 14))
    shipping_cost = round(random.uniform(5, 20), 2)
    shipping_address = fake.address().replace("\n", ", ")
    tracking_number = fake.bothify(text='??##########')
    order_status = random.choice(order_statuses)
    
    cursor.execute("""
        INSERT INTO orders (gameID, quantity, customerName, orderDate, shippingDate, shippingCost, shippingAddress, trackingNumber, orderStatus)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (game_id, quantity, customer_name, order_date, shipping_date, shipping_cost, shipping_address, tracking_number, order_status)
    )

conn.commit()
print("Orders inserted.")

cursor.close()
conn.close()