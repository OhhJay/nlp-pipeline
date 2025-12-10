#!/usr/bin/env python3
"""
Command-line interface for sentiment analysis pipeline
"""
import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pipeline import SentimentPipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description='Run sentiment analysis pipeline on data from various sources'
    )
    
    parser.add_argument(
        '--source-type',
        choices=['csv', 'json', 'postgres', 'mysql'],
        required=True,
        help='Type of data source'
    )
    
    parser.add_argument(
        '--source',
        required=True,
        help='Source path or connection string'
    )
    
    parser.add_argument(
        '--text-column',
        default='text',
        help='Name of column/field containing text to analyze (default: text)'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output path or table name'
    )
    
    parser.add_argument(
        '--output-type',
        choices=['csv', 'json', 'postgres', 'mysql'],
        help='Type of output destination (defaults to same as source-type)'
    )
    
    parser.add_argument(
        '--query',
        help='SQL query for database sources'
    )
    
    parser.add_argument(
        '--table',
        help='Table name for database output'
    )
    
    parser.add_argument(
        '--if-exists',
        choices=['fail', 'replace', 'append'],
        default='append',
        help='How to behave if output table exists (default: append)'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip generating summary statistics'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = SentimentPipeline()
    
    # Determine output type
    output_type = args.output_type or args.source_type
    
    try:
        # Run appropriate pipeline
        if args.source_type == 'csv':
            if output_type == 'csv':
                results = pipeline.run_csv_pipeline(
                    input_csv=args.source,
                    output_csv=args.output,
                    text_column=args.text_column,
                    save_summary=not args.no_summary
                )
            else:
                print("Error: CSV source currently only supports CSV output")
                sys.exit(1)
        
        elif args.source_type == 'json':
            if output_type == 'json':
                results = pipeline.run_json_pipeline(
                    input_json=args.source,
                    output_json=args.output,
                    text_field=args.text_column,
                    save_summary=not args.no_summary
                )
            else:
                print("Error: JSON source currently only supports JSON output")
                sys.exit(1)
        
        elif args.source_type in ['postgres', 'mysql']:
            if not args.query:
                print("Error: --query required for database sources")
                sys.exit(1)
            
            if output_type not in ['postgres', 'mysql']:
                print("Error: Database source requires database output")
                sys.exit(1)
            
            if not args.table:
                print("Error: --table required for database output")
                sys.exit(1)
            
            results = pipeline.run_database_pipeline(
                source_connection=args.source,
                source_query=args.query,
                dest_connection=args.output,
                dest_table=args.table,
                text_column=args.text_column,
                if_exists=args.if_exists
            )
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"Processed {len(results)} records")
        print(f"\nSentiment distribution:")
        print(results['sentiment'].value_counts())
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
