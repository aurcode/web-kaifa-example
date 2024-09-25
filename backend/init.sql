CREATE TABLE IF NOT EXISTS markets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    rating FLOAT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    market_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    text TEXT,
    score INT CHECK (score >= 1 AND score <= 5),
    FOREIGN KEY (market_id) REFERENCES markets(id) ON DELETE CASCADE
);
