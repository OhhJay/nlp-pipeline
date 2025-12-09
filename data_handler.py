"""
Data loader module for loading data from various sources
"""
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List, Dict, Optional
import json
import os
from pathlib import Path


class DataLoader:
    """Load data from various sources"""
    
    def __init__(self):
        """Initialize data loader"""
        self.supported_formats = ['csv', 'json', 'postgres', 'mysql']
    
    def load_from_csv(self, file_path: str, text_column: str) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file
            text_column: Name of column containing text to analyze
            
        Returns:
            DataFrame with text data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in CSV. Available: {df.columns.tolist()}")
        
        print(f"✓ Loaded {len(df)} rows from CSV: {file_path}")
        return df
    
    def load_from_json(self, file_path: str, text_field: str) -> pd.DataFrame:
        """
        Load data from JSON file
        
        Args:
            file_path: Path to JSON file
            text_field: Name of field containing text to analyze
            
        Returns:
            DataFrame with text data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Handle both array of objects and single object
        if isinstance(data, dict):
            data = [data]
        
        df = pd.DataFrame(data)
        
        if text_field not in df.columns:
            raise ValueError(f"Field '{text_field}' not found in JSON. Available: {df.columns.tolist()}")
        
        print(f"✓ Loaded {len(df)} rows from JSON: {file_path}")
        return df
    
    def load_from_database(
        self, 
        connection_string: str, 
        query: str,
        text_column: str
    ) -> pd.DataFrame:
        """
        Load data from database
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            text_column: Name of column containing text to analyze
            
        Returns:
            DataFrame with text data
        """
        engine = create_engine(connection_string)
        
        try:
            df = pd.read_sql_query(query, engine)
            
            if text_column not in df.columns:
                raise ValueError(f"Column '{text_column}' not found in query results. Available: {df.columns.tolist()}")
            
            print(f"✓ Loaded {len(df)} rows from database")
            return df
        
        finally:
            engine.dispose()
    
    def load_from_list(self, texts: List[str]) -> pd.DataFrame:
        """
        Load data from Python list
        
        Args:
            texts: List of text strings
            
        Returns:
            DataFrame with text data
        """
        df = pd.DataFrame({'text': texts})
        print(f"✓ Loaded {len(df)} rows from list")
        return df


class DataSaver:
    """Save processed data to various destinations"""
    
    def __init__(self):
        """Initialize data saver"""
        self.supported_formats = ['csv', 'json', 'postgres', 'mysql']
    
    def save_to_csv(
        self, 
        df: pd.DataFrame, 
        file_path: str,
        include_index: bool = False
    ) -> None:
        """
        Save DataFrame to CSV file
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            include_index: Whether to include index in output
        """
        output_dir = Path(file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(file_path, index=include_index)
        print(f"✓ Saved {len(df)} rows to CSV: {file_path}")
    
    def save_to_json(
        self, 
        df: pd.DataFrame, 
        file_path: str,
        orient: str = 'records',
        indent: int = 2
    ) -> None:
        """
        Save DataFrame to JSON file
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            orient: Format of JSON output
            indent: JSON indentation level
        """
        output_dir = Path(file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        df.to_json(file_path, orient=orient, indent=indent)
        print(f"✓ Saved {len(df)} rows to JSON: {file_path}")
    
    def save_to_database(
        self,
        df: pd.DataFrame,
        connection_string: str,
        table_name: str,
        if_exists: str = 'append'
    ) -> None:
        """
        Save DataFrame to database
        
        Args:
            df: DataFrame to save
            connection_string: Database connection string
            table_name: Target table name
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
        """
        engine = create_engine(connection_string)
        
        try:
            df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            print(f"✓ Saved {len(df)} rows to database table: {table_name}")
        
        finally:
            engine.dispose()
    
    def save_summary_stats(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Save summary statistics to text file
        
        Args:
            df: DataFrame with sentiment results
            file_path: Output file path
        """
        output_dir = Path(file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write("Sentiment Analysis Summary\n")
            f.write("=" * 50 + "\n\n")
            
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                f.write("Sentiment Distribution:\n")
                for sentiment, count in sentiment_counts.items():
                    percentage = (count / len(df)) * 100
                    f.write(f"  {sentiment.capitalize()}: {count} ({percentage:.1f}%)\n")
                f.write("\n")
            
            if 'polarity' in df.columns:
                f.write(f"Polarity Statistics:\n")
                f.write(f"  Mean: {df['polarity'].mean():.4f}\n")
                f.write(f"  Median: {df['polarity'].median():.4f}\n")
                f.write(f"  Std Dev: {df['polarity'].std():.4f}\n")
                f.write(f"  Min: {df['polarity'].min():.4f}\n")
                f.write(f"  Max: {df['polarity'].max():.4f}\n")
                f.write("\n")
            
            if 'subjectivity' in df.columns:
                f.write(f"Subjectivity Statistics:\n")
                f.write(f"  Mean: {df['subjectivity'].mean():.4f}\n")
                f.write(f"  Median: {df['subjectivity'].median():.4f}\n")
                f.write(f"  Std Dev: {df['subjectivity'].std():.4f}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"Total Records Processed: {len(df)}\n")
        
        print(f"✓ Saved summary statistics to: {file_path}")
