"""
Tests for data handling module
"""
import pytest
import pandas as pd
import json
import tempfile
import os
import sys

sys.path.insert(0, '/home/claude/nlp-project/src')
from data_handler import DataLoader, DataSaver


@pytest.fixture
def sample_csv_file():
    """Create temporary CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("id,text,rating\n")
        f.write("1,Great product!,5\n")
        f.write("2,Terrible experience,1\n")
        f.write("3,It's okay,3\n")
        filepath = f.name
    
    yield filepath
    
    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def sample_json_file():
    """Create temporary JSON file for testing"""
    data = [
        {"id": 1, "text": "Amazing!", "score": 5},
        {"id": 2, "text": "Not good", "score": 2}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(data, f)
        filepath = f.name
    
    yield filepath
    
    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame for testing"""
    return pd.DataFrame({
        'text': ['Excellent', 'Poor', 'Average'],
        'sentiment': ['positive', 'negative', 'neutral'],
        'polarity': [0.8, -0.7, 0.1],
        'subjectivity': [0.9, 0.8, 0.5]
    })


class TestDataLoader:
    
    def test_load_from_csv(self, sample_csv_file):
        """Test loading data from CSV"""
        loader = DataLoader()
        df = loader.load_from_csv(sample_csv_file, 'text')
        
        assert len(df) == 3
        assert 'text' in df.columns
        assert df['text'].iloc[0] == 'Great product!'
    
    def test_load_from_csv_missing_column(self, sample_csv_file):
        """Test error when column doesn't exist"""
        loader = DataLoader()
        
        with pytest.raises(ValueError, match="Column .* not found"):
            loader.load_from_csv(sample_csv_file, 'nonexistent')
    
    def test_load_from_csv_missing_file(self):
        """Test error when file doesn't exist"""
        loader = DataLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_from_csv('nonexistent.csv', 'text')
    
    def test_load_from_json(self, sample_json_file):
        """Test loading data from JSON"""
        loader = DataLoader()
        df = loader.load_from_json(sample_json_file, 'text')
        
        assert len(df) == 2
        assert 'text' in df.columns
        assert df['text'].iloc[0] == 'Amazing!'
    
    def test_load_from_json_missing_field(self, sample_json_file):
        """Test error when field doesn't exist"""
        loader = DataLoader()
        
        with pytest.raises(ValueError, match="Field .* not found"):
            loader.load_from_json(sample_json_file, 'nonexistent')
    
    def test_load_from_list(self):
        """Test loading data from list"""
        loader = DataLoader()
        texts = ["Text 1", "Text 2", "Text 3"]
        df = loader.load_from_list(texts)
        
        assert len(df) == 3
        assert 'text' in df.columns
        assert df['text'].tolist() == texts


class TestDataSaver:
    
    def test_save_to_csv(self, sample_dataframe):
        """Test saving DataFrame to CSV"""
        saver = DataSaver()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name
        
        try:
            saver.save_to_csv(sample_dataframe, output_path)
            
            # Verify file was created and contains data
            assert os.path.exists(output_path)
            df_loaded = pd.read_csv(output_path)
            assert len(df_loaded) == len(sample_dataframe)
            assert 'text' in df_loaded.columns
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_save_to_json(self, sample_dataframe):
        """Test saving DataFrame to JSON"""
        saver = DataSaver()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_path = f.name
        
        try:
            saver.save_to_json(sample_dataframe, output_path)
            
            # Verify file was created and contains data
            assert os.path.exists(output_path)
            with open(output_path, 'r') as f:
                data = json.load(f)
            assert len(data) == len(sample_dataframe)
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_save_summary_stats(self, sample_dataframe):
        """Test saving summary statistics"""
        saver = DataSaver()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            output_path = f.name
        
        try:
            saver.save_summary_stats(sample_dataframe, output_path)
            
            # Verify file was created and contains expected content
            assert os.path.exists(output_path)
            with open(output_path, 'r') as f:
                content = f.read()
            
            assert 'Sentiment Analysis Summary' in content
            assert 'Polarity Statistics' in content
            assert 'Total Records Processed' in content
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
