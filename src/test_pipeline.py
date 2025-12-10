"""
Tests for pipeline module
"""
import pytest
import pandas as pd
import tempfile
import os
import sys
 
from pipeline import SentimentPipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance for tests"""
    return SentimentPipeline()


@pytest.fixture
def sample_csv():
    """Create temporary CSV for testing"""
    df = pd.DataFrame({
        'review': [
            'Excellent product!',
            'Terrible quality',
            'Its okay'
        ],
        'rating': [5, 1, 3]
    })
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        df.to_csv(f.name, index=False)
        filepath = f.name
    
    yield filepath
    
    if os.path.exists(filepath):
        os.remove(filepath)


class TestSentimentPipeline:
    
    def test_run_csv_pipeline(self, pipeline, sample_csv):
        """Test complete CSV pipeline"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name
        
        try:
            result_df = pipeline.run_csv_pipeline(
                input_csv=sample_csv,
                output_csv=output_path,
                text_column='review',
                save_summary=False
            )
            
            # Verify results
            assert len(result_df) == 3
            assert 'sentiment' in result_df.columns
            assert 'polarity' in result_df.columns
            assert 'subjectivity' in result_df.columns
            assert 'processed_at' in result_df.columns
            
            # Verify output file was created
            assert os.path.exists(output_path)
            
            # Verify sentiments are correct
            assert result_df['sentiment'].iloc[0] == 'positive'
            assert result_df['sentiment'].iloc[1] == 'negative'
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_process_dataframe_with_empty_text(self, pipeline):
        """Test handling of empty or null text"""
        df = pd.DataFrame({
            'text': ['Good text', '', None, 'Another good text'],
        })
        
        result = pipeline._process_dataframe(df, 'text')
        
        assert len(result) == 4
        assert result['sentiment'].iloc[1] == 'unknown'
        assert result['sentiment'].iloc[2] == 'unknown'
        assert result['polarity'].iloc[1] == 0.0
        assert result['polarity'].iloc[2] == 0.0
    
    def test_custom_pipeline(self, pipeline):
        """Test custom pipeline with DataFrame input"""
        df = pd.DataFrame({
            'feedback': ['Great!', 'Bad', 'Okay'],
            'user_id': [1, 2, 3]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name
        
        try:
            result_df = pipeline.run_custom_pipeline(
                df=df,
                text_column='feedback',
                output_path=output_path,
                output_format='csv',
                save_summary=False
            )
            
            assert len(result_df) == 3
            assert 'sentiment' in result_df.columns
            assert 'user_id' in result_df.columns
            assert os.path.exists(output_path)
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
