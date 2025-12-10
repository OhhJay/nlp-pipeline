# System Architecture

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
├─────────────────────────────────────────────────────────────────┤
│  CSV Files  │  JSON Files  │  PostgreSQL  │  MySQL  │  Python   │
└──────┬──────┴──────┬───────┴──────┬───────┴────┬────┴─────┬─────┘
       │             │              │            │          │
       └─────────────┴──────────────┴────────────┴──────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   DataLoader    │
                    │   (Handler)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Pipeline     │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Sentiment     │
                    │    Analyzer     │
                    │  (NLTK/TextBlob)│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   DataSaver     │
                    │   (Handler)     │
                    └────────┬────────┘
                             │
       ┌─────────────────────┴──────────────────────┐
       │             │              │                │
       ▼             ▼              ▼                ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌──────────┐
│   CSV    │  │   JSON   │  │  Database   │  │ Summary  │
│  Output  │  │  Output  │  │   Tables    │  │  Stats   │
└──────────┘  └──────────┘  └─────────────┘  └──────────┘
```

## 🔧 Component Details

### 1. Data Layer (data_handler.py)

#### DataLoader
- Loads data from multiple sources
- Validates column/field existence
- Handles errors gracefully
- Returns pandas DataFrame

**Supported Sources:**
- CSV files
- JSON files  
- PostgreSQL databases
- MySQL databases
- Python lists

#### DataSaver
- Saves processed data to multiple destinations
- Generates summary statistics
- Creates output directories automatically

**Supported Outputs:**
- CSV files
- JSON files
- Database tables
- Summary text files

### 2. Processing Layer (sentiment_analyzer.py)

#### SentimentAnalyzer
- Text preprocessing (cleaning, normalization)
- Sentiment scoring using TextBlob
- Batch processing support

**Features:**
- Polarity: -1 (negative) to +1 (positive)
- Subjectivity: 0 (objective) to 1 (subjective)
- Label classification: positive/negative/neutral

### 3. Orchestration Layer (pipeline.py)

#### SentimentPipeline
- Coordinates data flow
- Manages end-to-end processing
- Logging and error handling
- Progress tracking

**Pipeline Types:**
- CSV → Processing → CSV
- JSON → Processing → JSON
- Database → Processing → Database
- Custom DataFrame → Processing → Any output

### 4. Interface Layer (run_pipeline.py)

#### CLI Interface
- Command-line argument parsing
- Configuration management
- User-friendly error messages

## 🔄 Data Flow

### CSV Processing Flow
```
1. User executes: run_pipeline.py --source-type csv ...
2. CLI parses arguments
3. Pipeline initialized
4. DataLoader reads CSV → pandas DataFrame
5. Pipeline adds timestamp column
6. For each row:
   - Extract text from specified column
   - Preprocess text (clean, normalize)
   - Analyze sentiment (polarity, subjectivity)
   - Classify label (positive/negative/neutral)
7. Append results to DataFrame
8. DataSaver writes to CSV output
9. Optional: Generate summary statistics
10. Return processed DataFrame
```

### Database Processing Flow
```
1. User executes: run_pipeline.py --source-type postgres ...
2. DataLoader connects to source database
3. Execute SQL query → pandas DataFrame
4. Process data (same as above)
5. DataSaver connects to destination database
6. Write results to table (append/replace/fail)
7. Close connections
```

## 🐳 Docker Architecture

### Container Structure
```
┌────────────────────────────────────────┐
│     nlp-sentiment-app Container        │
│  ┌──────────────────────────────────┐  │
│  │  Python 3.9                      │  │
│  │  + NLTK, TextBlob, pandas        │  │
│  │  + SQLAlchemy, psycopg2          │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Application Code                │  │
│  │  - src/                          │  │
│  │  - data/                         │  │
│  │  - run_pipeline.py               │  │
│  └──────────────────────────────────┘  │
└────────────────┬───────────────────────┘
                 │
                 │ Network: nlp-network
                 │
┌────────────────┴───────────────────────┐
│     postgres Container                  │
│  ┌──────────────────────────────────┐  │
│  │  PostgreSQL 15                   │  │
│  │  Database: nlpdb                 │  │
│  │  Tables: reviews, sentiment_results│
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Persistent Volume                │  │
│  │  postgres_data                    │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

## ⚙️ CI/CD Pipeline (CircleCI)

### Workflow
```
GitHub Push
    ↓
┌───────────────────┐
│   Checkout Code   │
└────────┬──────────┘
         ↓
┌───────────────────┐
│  Install Python   │
│  Dependencies     │
└────────┬──────────┘
         ↓
┌───────────────────┐
│  Download NLTK    │
│  Data             │
└────────┬──────────┘
         ↓
┌───────────────────┐
│   Run Tests       │
│   with Coverage   │
└────────┬──────────┘
         ↓
┌───────────────────┐
│  Store Test       │
│  Results          │
└────────┬──────────┘
         ↓
┌───────────────────┐
│  Build Docker     │
│  Image            │
└────────┬──────────┘
         ↓
┌───────────────────┐
│  Test Docker      │
│  Image            │
└────────┬──────────┘
         ↓
    Success! ✓
```

## 🔐 Security Considerations

1. **Environment Variables**: Use `.env` files for credentials
2. **SQL Injection**: Use parameterized queries (SQLAlchemy handles this)
3. **File Permissions**: Validate paths, use safe file operations
4. **Database Connections**: Always use connection pooling, dispose properly
5. **Input Validation**: Verify column/field existence before processing

## 📈 Scalability

### Current Limits
- Single-threaded processing
- In-memory DataFrame operations
- Best for < 1M records

### Future Scaling Options
1. **Batch Processing**: Process in chunks
2. **Parallel Processing**: Use multiprocessing/threading
3. **Distributed Processing**: Apache Spark, Dask
4. **Async I/O**: asyncio for database operations
5. **Message Queues**: RabbitMQ/Kafka for pipeline stages

## 🧪 Testing Strategy

```
Unit Tests (pytest)
    ├── test_sentiment_analyzer.py
    │   ├── Positive sentiment detection
    │   ├── Negative sentiment detection
    │   ├── Neutral sentiment detection
    │   ├── Text preprocessing
    │   └── Batch processing
    │
    ├── test_data_handler.py
    │   ├── CSV loading
    │   ├── JSON loading
    │   ├── Data saving
    │   └── Error handling
    │
    └── test_pipeline.py
        ├── End-to-end CSV pipeline
        ├── Custom DataFrame pipeline
        └── Empty text handling

Integration Tests (CircleCI)
    ├── Full pipeline execution
    ├── Docker image building
    └── Docker container testing
```

## 🔍 Monitoring & Logging

```python
Logging Levels:
    INFO  → Pipeline progress, records processed
    WARNING → Empty texts, missing data
    ERROR → File not found, connection failures
    
Example Log Output:
    2024-01-15 10:30:00 - pipeline - INFO - Pipeline initialized
    2024-01-15 10:30:01 - pipeline - INFO - ✓ Loaded 10 rows from CSV
    2024-01-15 10:30:02 - pipeline - INFO - Processing 10 texts...
    2024-01-15 10:30:03 - pipeline - INFO - Processed 10/10 rows
    2024-01-15 10:30:04 - pipeline - INFO - ✓ Saved 10 rows to CSV
```

## 💾 Database Schema

```sql
-- Source Data
reviews
    ├── id (SERIAL PRIMARY KEY)
    ├── review_text (TEXT)
    ├── rating (INTEGER)
    ├── product_id (VARCHAR)
    ├── user_id (VARCHAR)
    └── created_at (TIMESTAMP)

-- Processed Results
sentiment_results
    ├── id (SERIAL PRIMARY KEY)
    ├── review_id (INTEGER FK → reviews.id)
    ├── review_text (TEXT)
    ├── sentiment (VARCHAR: positive/negative/neutral)
    ├── polarity (FLOAT: -1 to 1)
    ├── subjectivity (FLOAT: 0 to 1)
    └── processed_at (TIMESTAMP)

Indexes:
    - reviews(product_id)
    - reviews(created_at)
    - sentiment_results(sentiment)
    - sentiment_results(processed_at)
```
