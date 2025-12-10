"""
Simple sentiment analysis using NLTK and TextBlob
"""
import nltk
from textblob import TextBlob
from typing import Dict, List
import re


class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        return text.strip()
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text
        
        Returns:
            Dictionary with polarity and subjectivity scores
        """
        cleaned_text = self.preprocess_text(text)
        blob = TextBlob(cleaned_text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 to 1
            'subjectivity': blob.sentiment.subjectivity,  # 0 to 1
            'label': self._get_sentiment_label(blob.sentiment.polarity)
        }
    
    def _get_sentiment_label(self, polarity: float) -> str:
        """Convert polarity score to label"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def batch_analyze(self, texts: List[str]) -> List[Dict[str, float]]:
        """Analyze sentiment for multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]


if __name__ == "__main__":
    # Example usage
    analyzer = SentimentAnalyzer()
    
    sample_texts = [
        "I absolutely love this product! It's amazing!",
        "This is terrible and disappointing.",
        "It's okay, nothing special."
    ]
    
    for text in sample_texts:
        result = analyzer.analyze_sentiment(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result['label']}")
        print(f"Polarity: {result['polarity']:.3f}")
        print(f"Subjectivity: {result['subjectivity']:.3f}")
