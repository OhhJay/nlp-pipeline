"""
NLP Pipeline - Orchestrates data loading, processing, and saving
"""
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from sentiment_analyzer import SentimentAnalyzer
from data_handler import DataLoader, DataSaver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SentimentPipeline:
    """End-to-end sentiment analysis pipeline"""
    
    def __init__(self):
        """Initialize pipeline components"""
        self.analyzer = SentimentAnalyzer()
        self.loader = DataLoader()
        self.saver = DataSaver()
        logger.info("Pipeline initialized")
    
    def run_csv_pipeline(
        self,
        input_csv: str,
        output_csv: str,
        text_column: str,
        save_summary: bool = True
    ) -> pd.DataFrame:
        """
        Run complete pipeline for CSV input/output
        
        Args:
            input_csv: Path to input CSV file
            output_csv: Path to output CSV file
            text_column: Name of column containing text to analyze
            save_summary: Whether to save summary statistics
            
        Returns:
            DataFrame with sentiment analysis results
        """
        logger.info(f"Starting CSV pipeline: {input_csv} -> {output_csv}")
        
        # Load data
        df = self.loader.load_from_csv(input_csv, text_column)
        
        # Process data
        df = self._process_dataframe(df, text_column)
        
        # Save results
        self.saver.save_to_csv(df, output_csv)
        
        if save_summary:
            summary_path = output_csv.replace('.csv', '_summary.txt')
            self.saver.save_summary_stats(df, summary_path)
        
        logger.info("CSV pipeline completed successfully")
        return df
    
    def run_json_pipeline(
        self,
        input_json: str,
        output_json: str,
        text_field: str,
        save_summary: bool = True
    ) -> pd.DataFrame:
        """
        Run complete pipeline for JSON input/output
        
        Args:
            input_json: Path to input JSON file
            output_json: Path to output JSON file
            text_field: Name of field containing text to analyze
            save_summary: Whether to save summary statistics
            
        Returns:
            DataFrame with sentiment analysis results
        """
        logger.info(f"Starting JSON pipeline: {input_json} -> {output_json}")
        
        # Load data
        df = self.loader.load_from_json(input_json, text_field)
        
        # Process data
        df = self._process_dataframe(df, text_field)
        
        # Save results
        self.saver.save_to_json(df, output_json)
        
        if save_summary:
            summary_path = output_json.replace('.json', '_summary.txt')
            self.saver.save_summary_stats(df, summary_path)
        
        logger.info("JSON pipeline completed successfully")
        return df
    
    def run_database_pipeline(
        self,
        source_connection: str,
        source_query: str,
        dest_connection: str,
        dest_table: str,
        text_column: str,
        if_exists: str = 'append'
    ) -> pd.DataFrame:
        """
        Run complete pipeline for database input/output
        
        Args:
            source_connection: Source database connection string
            source_query: SQL query to load data
            dest_connection: Destination database connection string
            dest_table: Destination table name
            text_column: Name of column containing text to analyze
            if_exists: How to behave if table exists
            
        Returns:
            DataFrame with sentiment analysis results
        """
        logger.info(f"Starting database pipeline: {dest_table}")
        
        # Load data
        df = self.loader.load_from_database(source_connection, source_query, text_column)
        
        # Process data
        df = self._process_dataframe(df, text_column)
        
        # Save results
        self.saver.save_to_database(df, dest_connection, dest_table, if_exists)
        
        logger.info("Database pipeline completed successfully")
        return df
    
    def run_custom_pipeline(
        self,
        df: pd.DataFrame,
        text_column: str,
        output_path: str,
        output_format: str = 'csv',
        save_summary: bool = True
    ) -> pd.DataFrame:
        """
        Run pipeline with custom DataFrame input
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text to analyze
            output_path: Path to save output
            output_format: Output format ('csv' or 'json')
            save_summary: Whether to save summary statistics
            
        Returns:
            DataFrame with sentiment analysis results
        """
        logger.info(f"Starting custom pipeline with {len(df)} rows")
        
        # Process data
        df = self._process_dataframe(df, text_column)
        
        # Save results
        if output_format == 'csv':
            self.saver.save_to_csv(df, output_path)
        elif output_format == 'json':
            self.saver.save_to_json(df, output_path)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        if save_summary:
            summary_path = output_path.rsplit('.', 1)[0] + '_summary.txt'
            self.saver.save_summary_stats(df, summary_path)
        
        logger.info("Custom pipeline completed successfully")
        return df
    
    def _process_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Process DataFrame with sentiment analysis
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            
        Returns:
            DataFrame with added sentiment columns
        """
        logger.info(f"Processing {len(df)} texts...")
        
        # Add timestamp
        df['processed_at'] = datetime.now().isoformat()
        
        # Analyze sentiment for each row
        results = []
        for idx, text in enumerate(df[text_column], 1):
            if pd.isna(text) or text.strip() == '':
                results.append({
                    'sentiment': 'unknown',
                    'polarity': 0.0,
                    'subjectivity': 0.0
                })
                logger.warning(f"Row {idx}: Empty or null text")
            else:
                result = self.analyzer.analyze_sentiment(str(text))
                results.append({
                    'sentiment': result['label'],
                    'polarity': result['polarity'],
                    'subjectivity': result['subjectivity']
                })
            
            # Progress logging
            if idx % 100 == 0:
                logger.info(f"Processed {idx}/{len(df)} rows")
        
        # Add results to dataframe
        df['sentiment'] = [r['sentiment'] for r in results]
        df['polarity'] = [r['polarity'] for r in results]
        df['subjectivity'] = [r['subjectivity'] for r in results]
        
        logger.info(f"Processing complete. Sentiment distribution: {df['sentiment'].value_counts().to_dict()}")
        
        return df


def main():
    """Example usage of the pipeline"""
    pipeline = SentimentPipeline()
    
    # Example: Process CSV file
    print("\n" + "="*60)
    print("Example: CSV Pipeline")
    print("="*60)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'id': range(1, 6),
        'review': [
            "This product is absolutely amazing! Love it!",
            "Terrible quality, very disappointed.",
            "It's okay, nothing special.",
            "Great customer service and fast shipping!",
            "Not worth the money, would not recommend."
        ],
        'rating': [5, 1, 3, 5, 2]
    })
    
    sample_data.to_csv('/tmp/sample_reviews.csv', index=False)
    
    # Run pipeline
    results = pipeline.run_csv_pipeline(
        input_csv='/tmp/sample_reviews.csv',
        output_csv='/tmp/sentiment_results.csv',
        text_column='review',
        save_summary=True
    )
    
    print("\nResults Preview:")
    print(results[['review', 'sentiment', 'polarity']].head())


if __name__ == "__main__":
    main()
