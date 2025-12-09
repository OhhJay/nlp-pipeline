# 🎯 START HERE - NLP Sentiment Analysis Project

Welcome! This is your complete NLP sentiment analysis pipeline.

## 🚀 Quick Navigation

### 📖 **New to the Project?**
Start with these files in order:

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ← Read this first!
   - High-level overview of what we built
   - Key features and capabilities
   - Technology stack

2. **[QUICKSTART.md](QUICKSTART.md)** ← Get running in 5 minutes!
   - Installation instructions
   - First pipeline run
   - Common commands

3. **[EXAMPLES.md](EXAMPLES.md)** ← See it in action!
   - Real-world usage examples
   - CSV, JSON, and database examples
   - Python API usage

### 📚 **Ready to Go Deeper?**

4. **[README.md](README.md)** ← Complete reference
   - Full documentation
   - API reference
   - Configuration options

5. **[ARCHITECTURE.md](ARCHITECTURE.md)** ← Understand the system
   - System design
   - Data flow diagrams
   - Component details

6. **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)** ← File organization
   - Directory layout
   - File descriptions
   - Usage patterns

### 💻 **Start Coding!**

Choose your path:

#### Path A: Command Line (Easiest)
```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m nltk.downloader punkt

# 2. Run your first pipeline
python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output results.csv

# 3. Check your results!
cat results.csv
```

#### Path B: Docker (Production-Ready)
```bash
# 1. Start everything
docker-compose up -d

# 2. Run pipeline in container
docker-compose exec nlp-app python run_pipeline.py \
  --source-type csv \
  --source data/sample_reviews.csv \
  --text-column review \
  --output data/output/results.csv

# 3. View results
docker-compose exec nlp-app cat data/output/results.csv
```

#### Path C: Python Code (Most Flexible)
```python
from src.pipeline import SentimentPipeline

# Create pipeline
pipeline = SentimentPipeline()

# Process data
results = pipeline.run_csv_pipeline(
    input_csv='data/sample_reviews.csv',
    output_csv='results.csv',
    text_column='review'
)

# Analyze results
print(results['sentiment'].value_counts())
```

#### Path D: Google Colab (Interactive)
1. Open `notebooks/sentiment_analysis.ipynb`
2. Upload to Google Colab
3. Run all cells and experiment!

## 🎯 What Can You Do?

### ✅ Immediate Things to Try

1. **Process the sample CSV**
   ```bash
   python run_pipeline.py --source-type csv --source data/sample_reviews.csv --text-column review --output results.csv
   ```

2. **Process the sample JSON**
   ```bash
   python run_pipeline.py --source-type json --source data/sample_feedback.json --text-column text --output results.json
   ```

3. **Run the tests**
   ```bash
   pytest tests/ -v
   ```

4. **Start the Docker environment**
   ```bash
   docker-compose up -d
   ```

### 🔧 Next Steps to Customize

1. **Use Your Own Data**
   - Replace `data/sample_reviews.csv` with your CSV
   - Update the `--text-column` parameter
   - Run the pipeline!

2. **Connect to Your Database**
   - Copy `.env.example` to `.env`
   - Add your database credentials
   - Use `--source-type postgres` or `mysql`

3. **Modify the Analysis**
   - Edit `src/sentiment_analyzer.py`
   - Adjust sentiment thresholds
   - Add custom preprocessing

## 📊 Expected Output

After running a pipeline, you'll get:

```
✓ Loaded 10 rows from CSV: data/sample_reviews.csv
Processing 10 texts...
Processed 10/10 rows
Processing complete. Sentiment distribution: {'positive': 5, 'negative': 3, 'neutral': 2}
✓ Saved 10 rows to CSV: results.csv
✓ Saved summary statistics to: results_summary.txt
```

Your files:
- `results.csv` - All data with sentiment scores
- `results_summary.txt` - Statistics and insights

## 🆘 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "NLTK data not found"
```bash
python -m nltk.downloader punkt
```

### Issue: "Permission denied" on run_pipeline.py
```bash
chmod +x run_pipeline.py
```

### Issue: Docker not starting
```bash
docker-compose down
docker-compose up -d
```

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `src/sentiment_analyzer.py` | Core NLP engine |
| `src/data_handler.py` | Load/save data |
| `src/pipeline.py` | Orchestration |
| `run_pipeline.py` | CLI interface |
| `tests/` | Test suite |
| `data/` | Sample data |
| `Dockerfile` | Container setup |
| `docker-compose.yml` | Multi-container |

## 🎓 Learning Path

**Beginner:**
1. Run QUICKSTART examples
2. Try with sample data
3. Explore Colab notebook

**Intermediate:**
1. Process your own CSV data
2. Try database integration
3. Modify sentiment thresholds

**Advanced:**
1. Add new data sources
2. Integrate ML models
3. Deploy to cloud
4. Set up CI/CD

## 🎉 Success Checklist

- [ ] Read PROJECT_SUMMARY.md
- [ ] Ran QUICKSTART example
- [ ] Processed sample CSV
- [ ] Viewed results file
- [ ] Ran tests successfully
- [ ] Tried Docker setup (optional)
- [ ] Read EXAMPLES.md
- [ ] Processed your own data

## 💡 Pro Tips

1. **Start small** - Use sample data first
2. **Check outputs** - Always verify the CSV/JSON results
3. **Read summaries** - The `_summary.txt` files have great insights
4. **Use Docker** - It handles all dependencies
5. **Run tests** - Ensures everything works

## 🚀 Ready to Build Something Amazing?

This pipeline can handle:
- Customer reviews
- Social media sentiment
- Survey responses  
- Support tickets
- Product feedback
- And much more!

Start with the sample data, then plug in your own sources.

## 📞 Need Help?

Check the documentation:
- **QUICKSTART.md** - Fast setup
- **EXAMPLES.md** - Code examples
- **ARCHITECTURE.md** - How it works
- **README.md** - Full reference

## 🎊 You're Ready!

Pick a path above and start building. The sample data is ready, the code is tested, and the documentation is comprehensive.

**Happy analyzing!** 📊✨

---

*Questions? Start with QUICKSTART.md or dive into the code!*
