# NLP Sentiment Analysis Project

A production-ready sentiment analysis pipeline that loads data from various sources (CSV, JSON, databases), processes it with NLP, and saves results. Includes CI/CD with CircleCI, Docker containerization, and Google Colab notebooks.

## 🚀 Features

- **Multi-source data loading**: CSV, JSON, PostgreSQL, MySQL
- **Sentiment analysis**: Using NLTK and TextBlob
- **Batch processing**: Handle large datasets efficiently
- **Multiple output formats**: CSV, JSON, database tables
- **Summary statistics**: Automatic generation of analysis summaries
- **CLI interface**: Easy command-line pipeline execution
- **Automated testing**: pytest with coverage reporting
- **CI/CD pipeline**: CircleCI integration
- **Docker support**: Full containerization with docker-compose
- **Interactive notebooks**: Google Colab for experimentation

## 📁 Project Structure

```
nlp-project/
├── src/
│   ├── sentiment_analyzer.py    # Core sentiment analysis
│   ├── data_handler.py          # Data loading and saving
│   ├── pipeline.py              # Pipeline orchestration
│   └── __init__.py
├── tests/
│   ├── test_sentiment_analyzer.py
│   ├── test_data_handler.py
│   └── test_pipeline.py
├── data/
│   ├── sample_reviews.csv       # Sample CSV data
│   └── sample_feedback.json     # Sample JSON data
├── notebooks/
│   └── sentiment_analysis.ipynb # Colab notebook
├── .circleci/
│   └── config.yml               # CI/CD configuration
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container setup
├── init_db.sql                  # Database initialization
├── run_pipeline.py              # CLI interface
├── requirements.txt             # Dependencies
└── README.md
```

## 🛠️ Setup

### Local Development

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd nlp-project
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m nltk.downloader punkt
```

4. **Run the analyzer:**
```bash
python src/sentiment_analyzer.py
```

### Using Docker

#### Build and run with Docker:
```bash
# Build the image
docker build -t nlp-sentiment-analyzer .

# Run with local data
docker run -v $(pwd)/data:/app/data nlp-sentiment-analyzer \
  python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/results.csv
```

#### Using Docker Compose (recommended):
```bash
# Start all services (app + PostgreSQL)
docker-compose up -d

# Check logs
docker-compose logs -f

# Access the application container
docker-compose exec nlp-app bash

# Inside container, run pipeline
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --query "SELECT id, review_text as text FROM reviews" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://nlpuser:nlppass@postgres:5432/nlpdb" \
  --table sentiment_results

# Stop services
docker-compose down
```

### Google Colab

1. Open the notebook: `notebooks/sentiment_analysis.ipynb`
2. Upload to Google Colab
3. Run all cells to experiment with the sentiment analyzer

Alternatively, you can open directly from GitHub:
- Go to [Google Colab](https://colab.research.google.com)
- File → Open notebook → GitHub
- Enter your repository URL

## 🧪 Testing

### Run tests locally:
```bash
pytest tests/ -v
```

### Run tests with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## 🔄 CI/CD Pipeline (CircleCI)

The project includes a complete CircleCI pipeline that:

1. **Test Job:**
   - Installs dependencies
   - Downloads NLTK data
   - Runs unit tests with coverage
   - Stores test results

2. **Build-Docker Job:**
   - Builds Docker image
   - Tags with commit SHA and latest
   - Tests the Docker image

### Setting up CircleCI

1. Create account at [CircleCI](https://circleci.com)
2. Connect your GitHub/Bitbucket repository
3. The pipeline will automatically run on every commit

## 📊 Usage Examples

### Command-Line Interface (CLI)

The easiest way to run the pipeline is using the CLI:

#### Process CSV file:
```bash
python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/results.csv
```

#### Process JSON file:
```bash
python run_pipeline.py \
  --source-type json \
  --source data/sample_feedback.json \
  --text-column text \
  --output data/output/results.json
```

#### Process from database:
```bash
python run_pipeline.py \
  --source-type postgres \
  --source "postgresql://user:pass@localhost:5432/dbname" \
  --query "SELECT id, review_text as text FROM reviews WHERE rating IS NOT NULL" \
  --text-column text \
  --output-type postgres \
  --output "postgresql://user:pass@localhost:5432/dbname" \
  --table sentiment_results
```

### Python API

```python
from src.pipeline import SentimentPipeline

pipeline = SentimentPipeline()

# CSV Pipeline
results = pipeline.run_csv_pipeline(
    input_csv='data/sample_reviews.csv',
    output_csv='data/output/results.csv',
    text_column='review',
    save_summary=True
)

# JSON Pipeline
results = pipeline.run_json_pipeline(
    input_json='data/sample_feedback.json',
    output_json='data/output/results.json',
    text_field='text'
)

# Custom DataFrame Pipeline
import pandas as pd
df = pd.DataFrame({'feedback': ['Great!', 'Bad', 'Okay']})
results = pipeline.run_custom_pipeline(
    df=df,
    text_column='feedback',
    output_path='output.csv',
    output_format='csv'
)

# Database Pipeline
results = pipeline.run_database_pipeline(
    source_connection='postgresql://user:pass@localhost/db',
    source_query='SELECT * FROM reviews',
    dest_connection='postgresql://user:pass@localhost/db',
    dest_table='sentiment_results',
    text_column='review_text'
)
```

### Basic Sentiment Analysis

```python
from src.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Single text analysis
result = analyzer.analyze_sentiment("I love this product!")
print(result)
# Output: {'polarity': 0.5, 'subjectivity': 0.6, 'label': 'positive'}

# Batch analysis
texts = [
    "Great service!",
    "Terrible experience.",
    "It's okay."
]
results = analyzer.batch_analyze(texts)
```

### API Reference

#### `SentimentAnalyzer`

**Methods:**

- `analyze_sentiment(text: str) -> Dict[str, float]`
  - Analyzes sentiment of a single text
  - Returns dictionary with polarity, subjectivity, and label

- `batch_analyze(texts: List[str]) -> List[Dict[str, float]]`
  - Analyzes multiple texts
  - Returns list of sentiment dictionaries

- `preprocess_text(text: str) -> str`
  - Cleans and preprocesses text
  - Removes URLs, special characters, converts to lowercase

## 📈 Sentiment Scores

- **Polarity**: Range from -1 (negative) to 1 (positive)
- **Subjectivity**: Range from 0 (objective) to 1 (subjective)
- **Label**: "positive", "negative", or "neutral"

## 🔧 Configuration

### Docker Configuration

The Dockerfile uses Python 3.9-slim base image and includes:
- System dependencies
- Python packages from requirements.txt
- Pre-downloaded NLTK data

### CircleCI Configuration

Key features:
- Python 3.9 executor
- Dependency caching
- Test result storage
- Docker layer caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Testing Strategy

The project includes comprehensive tests:
- Positive sentiment detection
- Negative sentiment detection
- Neutral sentiment detection
- Text preprocessing
- Batch processing
- Return structure validation

## 🚀 Deployment Options

### Option 1: Docker Hub
```bash
docker tag nlp-sentiment-analyzer:latest yourusername/nlp-sentiment-analyzer:latest
docker push yourusername/nlp-sentiment-analyzer:latest
```

### Option 2: Cloud Run (Google Cloud)
```bash
gcloud run deploy sentiment-analyzer --source . --region us-central1
```

### Option 3: AWS ECR + ECS
```bash
# Push to ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
docker tag nlp-sentiment-analyzer:latest aws_account_id.dkr.ecr.region.amazonaws.com/nlp-sentiment-analyzer:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/nlp-sentiment-analyzer:latest
```

## 📚 Dependencies

### Core Dependencies
- **nltk**: Natural language processing toolkit
- **textblob**: Simplified text processing
- **pandas**: Data manipulation and analysis
- **sqlalchemy**: Database abstraction layer
- **psycopg2-binary**: PostgreSQL adapter
- **python-dotenv**: Environment variable management

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

## 🐛 Known Limitations

- Basic sentiment analysis (rule-based, not ML model)
- English language only
- May not capture sarcasm or complex sentiments
- Requires internet for initial NLTK data download

## 🔮 Future Enhancements

- [ ] Add support for multiple languages
- [ ] Integrate ML-based models (BERT, RoBERTa)
- [ ] Add API endpoint (Flask/FastAPI)
- [ ] Implement aspect-based sentiment analysis
- [ ] Add emotion detection
- [ ] Create web dashboard
- [ ] Add real-time streaming analysis

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👥 Authors

Your Name - Initial work

## 🙏 Acknowledgments

- NLTK and TextBlob teams
- CircleCI documentation
- Docker community
