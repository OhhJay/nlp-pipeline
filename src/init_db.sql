-- Initialize database schema for NLP sentiment analysis

-- Create source data table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    review_text TEXT NOT NULL,
    rating INTEGER,
    product_id VARCHAR(50),
    user_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sentiment results table
CREATE TABLE IF NOT EXISTS sentiment_results (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    review_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    polarity FLOAT NOT NULL,
    subjectivity FLOAT NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO reviews (review_text, rating, product_id, user_id) VALUES
    ('This product is absolutely amazing! Best purchase ever!', 5, 'PROD001', 'user123'),
    ('Terrible quality. Very disappointed with this purchase.', 1, 'PROD001', 'user456'),
    ('It''s okay. Nothing special but does the job.', 3, 'PROD002', 'user789'),
    ('Great value for money! Highly recommend.', 5, 'PROD002', 'user321'),
    ('Not as described. Poor customer service too.', 2, 'PROD003', 'user654'),
    ('Excellent product! Fast delivery as well.', 5, 'PROD003', 'user987'),
    ('Worst experience ever. Never buying from here again.', 1, 'PROD001', 'user135'),
    ('Good quality and reasonable price.', 4, 'PROD002', 'user246'),
    ('Average product. Could be better.', 3, 'PROD003', 'user357'),
    ('Love it! Exceeded my expectations completely.', 5, 'PROD001', 'user468');

-- Create indexes for better query performance
CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_created ON reviews(created_at);
CREATE INDEX idx_sentiment_sentiment ON sentiment_results(sentiment);
CREATE INDEX idx_sentiment_processed ON sentiment_results(processed_at);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nlpuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nlpuser;
