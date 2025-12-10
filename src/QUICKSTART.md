# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd nlp-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m nltk.downloader punkt
```

### 2. Run Your First Pipeline

#### Option A: CSV Processing
```bash
python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/results.csv
```

Check your results:
- `data/output/results.csv` - Full results with sentiment scores
- `data/output/results_summary.txt` - Summary statistics

#### Option B: JSON Processing
```bash
python run_pipeline.py \
  --source-type json \
  --source data/sample_feedback.json \
  --text-column text \
  --output data/output/feedback_results.json
```

### 3. Try with Docker Compose
```bash
# Start services
docker-compose up -d

# Wait 10 seconds for PostgreSQL to initialize
sleep 10

# Run pipeline on database
docker-compose exec nlp-app python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --query "SELECT id, review_text as text, rating FROM reviews" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --table sentiment_results

# View results
docker-compose exec postgres psql -U nlpuser -d nlpdb -c "SELECT review_text, sentiment, polarity FROM sentiment_results LIMIT 5;"

# Cleanup
docker-compose down
```

### 4. Run Tests
```bash
pytest tests/ -v --cov=src
```

### 5. Try the Colab Notebook
1. Upload `notebooks/sentiment_analysis.ipynb` to Google Colab
2. Run all cells
3. Experiment with your own text!

## 📊 Understanding the Output

### Sentiment Scores
- **Polarity**: -1 (very negative) to +1 (very positive)
- **Subjectivity**: 0 (objective) to 1 (subjective)
- **Label**: "positive", "negative", or "neutral"

### Example Output (CSV)
```csv
id,review,rating,sentiment,polarity,subjectivity,processed_at
1,"Great product!",5,positive,0.8,0.75,2024-01-15T10:30:00
2,"Terrible quality",1,negative,-0.65,0.85,2024-01-15T10:30:01
```

### Summary Statistics File
```
Sentiment Analysis Summary
==================================================

Sentiment Distribution:
  Positive: 4 (40.0%)
  Negative: 3 (30.0%)
  Neutral: 3 (30.0%)

Polarity Statistics:
  Mean: 0.1250
  Median: 0.1000
  ...
```

## 🎯 Common Use Cases

### 1. Analyze Customer Reviews
```bash
python run_pipeline.py \
  --source-type csv \
  --source customer_reviews.csv \
  --text-column review_text \
  --output analyzed_reviews.csv
```

### 2. Monitor Social Media Sentiment
```bash
python run_pipeline.py \
  --source-type json \
  --source tweets.json \
  --text-column tweet_text \
  --output sentiment_analysis.json
```

### 3. Process Support Tickets
```bash
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://user:pass@localhost/support" \
  --query "SELECT ticket_id, description as text FROM tickets WHERE status='open'" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://user:pass@localhost/support" \
  --table ticket_sentiment
```

## 🔧 Customization

### Add Your Own Data
1. Place your CSV/JSON file in the `data/` directory
2. Update the column/field names in the command
3. Run the pipeline!

### Connect Your Database
1. Copy `.env.example` to `.env`
2. Update connection strings
3. Run with your credentials

## ❓ Troubleshooting

### Issue: "Column not found"
- Check your CSV/JSON column names
- Use `--text-column` to specify the correct column

### Issue: "Database connection failed"
- Verify your connection string
- Check if database is running: `docker-compose ps`

### Issue: "Import errors"
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Next Steps

1. Read the full README.md for detailed documentation
2. Check out the Colab notebook for interactive examples
3. Explore the test files for more usage patterns
4. Set up CircleCI for your repository
5. Customize the analyzer for your specific needs

## 💡 Tips

- Start with small datasets to test
- Check the summary file for quick insights
- Use `--no-summary` flag to skip summary generation
- Enable CircleCI by connecting your GitHub repo
- Use docker-compose for local database testing

Happy analyzing! 🎉
