# Usage Examples

## 📋 Table of Contents
1. [CSV Processing](#csv-processing)
2. [JSON Processing](#json-processing)
3. [Database Processing](#database-processing)
4. [Python API](#python-api)
5. [Docker Examples](#docker-examples)
6. [Real-World Scenarios](#real-world-scenarios)

## CSV Processing

### Basic CSV Pipeline
```bash
python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/analyzed_reviews.csv
```

### CSV Without Summary
```bash
python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/results.csv \
  --no-summary
```

### Large CSV File
```bash
# For large files, check progress in logs
python run_pipeline.py \
  --source-type csv \
  --source data/large_reviews.csv \
  --text-column feedback_text \
  --output data/output/large_results.csv 2>&1 | tee pipeline.log
```

## JSON Processing

### Basic JSON Pipeline
```bash
python run_pipeline.py \
  --source-type json \
  --source data/sample_feedback.json \
  --text-column text \
  --output data/output/feedback_analysis.json
```

### Nested JSON Field
```bash
# If your JSON has nested structure like: {"data": {"comment": "text here"}}
# First flatten your JSON, then process the comment field
python run_pipeline.py \
  --source-type json \
  --source data/nested_feedback.json \
  --text-column comment \
  --output data/output/results.json
```

## Database Processing

### PostgreSQL to PostgreSQL
```bash
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://user:password@localhost:5432/source_db" \
  --query "SELECT id, review_text as text FROM customer_reviews WHERE created_at > '2024-01-01'" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://user:password@localhost:5432/target_db" \
  --table sentiment_analysis \
  --if-exists append
```

### PostgreSQL with Complex Query
```bash
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://user:password@localhost:5432/mydb" \
  --query "
    SELECT 
      r.id,
      r.review_text as text,
      r.product_id,
      p.product_name
    FROM reviews r
    JOIN products p ON r.product_id = p.id
    WHERE r.rating IS NOT NULL
    AND r.created_at >= CURRENT_DATE - INTERVAL '30 days'
  " \
  --text-column text \
  --output-type postgres \
  --output "postgresql://user:password@localhost:5432/mydb" \
  --table recent_sentiment
```

### MySQL Example
```bash
python run_pipeline.py \
  --source-type mysql \
  --source "mysql+pymysql://user:password@localhost:3306/reviews_db" \
  --query "SELECT review_id, comment_text as text FROM comments" \
  --text-column text \
  --output-type mysql \
  --output "mysql+pymysql://user:password@localhost:3306/analytics_db" \
  --table comment_sentiment
```

### Replace Existing Table
```bash
# Use --if-exists replace to overwrite table
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://user:password@localhost:5432/db" \
  --query "SELECT * FROM reviews" \
  --text-column review_text \
  --output-type postgres \
  --output "postgresql://user:password@localhost:5432/db" \
  --table sentiment_results \
  --if-exists replace
```

## Python API

### Simple Script
```python
from src.pipeline import SentimentPipeline

# Initialize pipeline
pipeline = SentimentPipeline()

# Process CSV
results = pipeline.run_csv_pipeline(
    input_csv='reviews.csv',
    output_csv='analyzed_reviews.csv',
    text_column='review_text'
)

# Print summary
print(f"Processed {len(results)} reviews")
print(results['sentiment'].value_counts())
```

### Process DataFrame
```python
import pandas as pd
from src.pipeline import SentimentPipeline

# Load your data
df = pd.read_csv('my_data.csv')

# Initialize and run
pipeline = SentimentPipeline()
results = pipeline.run_custom_pipeline(
    df=df,
    text_column='comments',
    output_path='sentiment_results.csv',
    output_format='csv',
    save_summary=True
)

# Analyze results
positive_pct = (results['sentiment'] == 'positive').mean() * 100
print(f"Positive sentiment: {positive_pct:.1f}%")
```

### Direct Sentiment Analysis
```python
from src.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Single analysis
text = "This is an amazing product!"
result = analyzer.analyze_sentiment(text)
print(f"Sentiment: {result['label']}")
print(f"Polarity: {result['polarity']:.3f}")

# Batch analysis
texts = [
    "Great service!",
    "Terrible experience",
    "It's okay"
]
results = analyzer.batch_analyze(texts)

for text, result in zip(texts, results):
    print(f"{text}: {result['label']}")
```

### Database Pipeline with Error Handling
```python
from src.pipeline import SentimentPipeline
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

pipeline = SentimentPipeline()

try:
    results = pipeline.run_database_pipeline(
        source_connection='postgresql://user:pass@localhost/db',
        source_query='SELECT id, text FROM reviews',
        dest_connection='postgresql://user:pass@localhost/db',
        dest_table='sentiment_results',
        text_column='text',
        if_exists='append'
    )
    print(f"✓ Success! Processed {len(results)} records")
    
except Exception as e:
    print(f"✗ Error: {e}")
    logging.exception("Pipeline failed")
```

## Docker Examples

### Basic Docker Run
```bash
# Build image
docker build -t nlp-analyzer .

# Run with volume mount
docker run -v $(pwd)/data:/app/data nlp-analyzer \
  python run_pipeline.py \
  --source-type csv \
  --source data/reviews.csv \
  --text-column review \
  --output data/output/results.csv
```

### Docker Compose - Full Stack
```bash
# Start all services
docker-compose up -d

# Wait for database initialization
sleep 10

# Process data from database
docker-compose exec nlp-app python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --query "SELECT id, review_text as text FROM reviews" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --table sentiment_results

# View results in database
docker-compose exec postgres psql -U nlpuser -d nlpdb \
  -c "SELECT review_text, sentiment, polarity FROM sentiment_results LIMIT 10;"

# Export results to CSV
docker-compose exec postgres psql -U nlpuser -d nlpdb \
  -c "COPY sentiment_results TO STDOUT CSV HEADER" > results.csv

# Stop services
docker-compose down
```

### Interactive Docker Session
```bash
# Start container with bash
docker run -it -v $(pwd)/data:/app/data nlp-analyzer bash

# Inside container:
# 1. Process CSV
python run_pipeline.py --source-type csv --source data/reviews.csv --text-column review --output data/results.csv

# 2. Check Python interactively
python
>>> from src.sentiment_analyzer import SentimentAnalyzer
>>> analyzer = SentimentAnalyzer()
>>> analyzer.analyze_sentiment("Great product!")
>>> exit()

# 3. Exit container
exit
```

## Real-World Scenarios

### 1. Daily Customer Review Analysis
```bash
#!/bin/bash
# daily_review_analysis.sh

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="data/output/${DATE}"
mkdir -p "${OUTPUT_DIR}"

# Process today's reviews
python run_pipeline.py \
  --source-type postgres \
  --source "${DATABASE_URL}" \
  --query "SELECT * FROM reviews WHERE DATE(created_at) = '${DATE}'" \
  --text-column review_text \
  --output-type postgres \
  --output "${DATABASE_URL}" \
  --table daily_sentiment

# Generate report
echo "Daily Sentiment Report - ${DATE}" > "${OUTPUT_DIR}/report.txt"
cat "data/output/sentiment_summary.txt" >> "${OUTPUT_DIR}/report.txt"
```

### 2. Social Media Monitoring
```python
# monitor_social_media.py
import pandas as pd
from src.pipeline import SentimentPipeline
from datetime import datetime

# Fetch tweets (pseudo-code)
tweets = fetch_recent_tweets(hashtag="#MyBrand")

# Convert to DataFrame
df = pd.DataFrame(tweets)

# Analyze sentiment
pipeline = SentimentPipeline()
results = pipeline.run_custom_pipeline(
    df=df,
    text_column='tweet_text',
    output_path=f'social_sentiment_{datetime.now():%Y%m%d}.csv',
    output_format='csv'
)

# Alert on negative spike
negative_pct = (results['sentiment'] == 'negative').mean()
if negative_pct > 0.3:
    send_alert(f"High negative sentiment: {negative_pct:.0%}")
```

### 3. Product Feedback Dashboard
```python
# product_feedback_pipeline.py
from src.pipeline import SentimentPipeline
import pandas as pd

pipeline = SentimentPipeline()

# Process feedback from database
results = pipeline.run_database_pipeline(
    source_connection='postgresql://user:pass@localhost/db',
    source_query="""
        SELECT 
            p.product_name,
            r.review_text as text,
            r.rating
        FROM reviews r
        JOIN products p ON r.product_id = p.id
        WHERE r.created_at >= CURRENT_DATE - INTERVAL '7 days'
    """,
    dest_connection='postgresql://user:pass@localhost/db',
    dest_table='weekly_product_sentiment',
    text_column='text',
    if_exists='replace'
)

# Generate insights by product
insights = results.groupby('product_name').agg({
    'sentiment': lambda x: (x == 'positive').mean(),
    'polarity': 'mean',
    'rating': 'mean'
}).round(3)

print("\nWeekly Product Insights:")
print(insights)
```

### 4. Multi-Source Analysis
```bash
#!/bin/bash
# analyze_all_sources.sh

echo "Starting multi-source sentiment analysis..."

# 1. Process CSV reviews
python run_pipeline.py \
  --source-type csv \
  --source data/csv_reviews.csv \
  --text-column review \
  --output data/output/csv_results.csv

# 2. Process JSON feedback
python run_pipeline.py \
  --source-type json \
  --source data/json_feedback.json \
  --text-column comment \
  --output data/output/json_results.json

# 3. Process database records
python run_pipeline.py \
  --source-type postgres \
  --source "${DB_CONNECTION}" \
  --query "SELECT text FROM user_feedback" \
  --text-column text \
  --output-type postgres \
  --output "${DB_CONNECTION}" \
  --table consolidated_sentiment

echo "Multi-source analysis complete!"
```

### 5. Scheduled Batch Processing
```python
# scheduled_analysis.py
from apscheduler.schedulers.blocking import BlockingScheduler
from src.pipeline import SentimentPipeline
import logging

logging.basicConfig(level=logging.INFO)
pipeline = SentimentPipeline()

def hourly_analysis():
    """Run every hour"""
    try:
        results = pipeline.run_database_pipeline(
            source_connection=DB_CONNECTION,
            source_query="SELECT * FROM recent_reviews",
            dest_connection=DB_CONNECTION,
            dest_table='hourly_sentiment',
            text_column='review_text'
        )
        logging.info(f"Processed {len(results)} records")
    except Exception as e:
        logging.error(f"Analysis failed: {e}")

scheduler = BlockingScheduler()
scheduler.add_job(hourly_analysis, 'interval', hours=1)
scheduler.start()
```

## Tips & Best Practices

### Performance Optimization
```python
# Process in chunks for large datasets
import pandas as pd
from src.pipeline import SentimentPipeline

pipeline = SentimentPipeline()
chunksize = 1000

for chunk in pd.read_csv('large_file.csv', chunksize=chunksize):
    results = pipeline.run_custom_pipeline(
        df=chunk,
        text_column='text',
        output_path='results.csv',
        output_format='csv',
        save_summary=False
    )
```

### Error Handling
```python
# Robust pipeline with retries
from src.pipeline import SentimentPipeline
import time

def run_with_retry(max_retries=3):
    pipeline = SentimentPipeline()
    
    for attempt in range(max_retries):
        try:
            results = pipeline.run_csv_pipeline(
                input_csv='data.csv',
                output_csv='results.csv',
                text_column='text'
            )
            return results
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise
```

### Custom Filtering
```python
# Filter and process specific sentiments
from src.pipeline import SentimentPipeline

pipeline = SentimentPipeline()
results = pipeline.run_csv_pipeline(
    input_csv='reviews.csv',
    output_csv='all_results.csv',
    text_column='review'
)

# Export only negative reviews for investigation
negative_reviews = results[results['sentiment'] == 'negative']
negative_reviews.to_csv('negative_reviews_for_review.csv', index=False)

print(f"Found {len(negative_reviews)} negative reviews for follow-up")
```
