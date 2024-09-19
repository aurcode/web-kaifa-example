-- Create the 'scores' table if it does not already exist
CREATE TABLE IF NOT EXISTS scores (
    -- 'id' column: Integer type, auto-incrementing, serves as the primary key
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- 'username' column: Variable character string of up to 50 characters, cannot be null
    username VARCHAR(50) NOT NULL,

    -- 'score' column: Floating point number, cannot be null
    score FLOAT NOT NULL
);
