"""
Unit tests for sentiment analyzer
"""
import pytest
import sys
sys.path.insert(0, '/home/claude/nlp-project/src')
from sentiment_analyzer import SentimentAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance for tests"""
    return SentimentAnalyzer()


class TestSentimentAnalyzer:
    
    def test_positive_sentiment(self, analyzer):
        """Test positive sentiment detection"""
        text = "I love this! It's wonderful and amazing!"
        result = analyzer.analyze_sentiment(text)
        assert result['label'] == 'positive'
        assert result['polarity'] > 0
    
    def test_negative_sentiment(self, analyzer):
        """Test negative sentiment detection"""
        text = "This is terrible and awful. I hate it."
        result = analyzer.analyze_sentiment(text)
        assert result['label'] == 'negative'
        assert result['polarity'] < 0
    
    def test_neutral_sentiment(self, analyzer):
        """Test neutral sentiment detection"""
        text = "This is a sentence."
        result = analyzer.analyze_sentiment(text)
        assert result['label'] == 'neutral'
        assert -0.1 <= result['polarity'] <= 0.1
    
    def test_preprocess_text(self, analyzer):
        """Test text preprocessing"""
        text = "Check out https://example.com! #amazing @user"
        cleaned = analyzer.preprocess_text(text)
        assert 'https' not in cleaned
        assert cleaned.islower()
    
    def test_batch_analyze(self, analyzer):
        """Test batch processing"""
        texts = [
            "Great product!",
            "Terrible experience.",
            "It's okay."
        ]
        results = analyzer.batch_analyze(texts)
        assert len(results) == 3
        assert all('polarity' in r for r in results)
        assert all('label' in r for r in results)
    
    def test_return_structure(self, analyzer):
        """Test that return structure is correct"""
        result = analyzer.analyze_sentiment("Test text")
        assert 'polarity' in result
        assert 'subjectivity' in result
        assert 'label' in result
        assert isinstance(result['polarity'], float)
        assert isinstance(result['subjectivity'], float)
        assert isinstance(result['label'], str)
