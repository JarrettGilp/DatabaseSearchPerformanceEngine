DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS orders;

CREATE TABLE games (
    gameID SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(300) NOT NULL,
    publisher VARCHAR(50) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    player_count INT,
    price NUMERIC(8,2) NOT NULL,
    releaseYear INT,
    esrbRating VARCHAR(5) NOT NULL,
    platform VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    orderID SERIAL PRIMARY KEY,
    gameID INT REFERENCES games(gameID),
    quantity INT NOT NULL,
    customerName VARCHAR(100) NOT NULL,
    orderDate DATE NOT NULL,
    shippingDate DATE NOT NULL,
    shippingCost NUMERIC(6,2) NOT NULL,
    shippingAddress VARCHAR(200) NOT NULL,
    trackingNumber VARCHAR(50) NOT NULL,
    orderStatus VARCHAR(20) NOT NULL
);