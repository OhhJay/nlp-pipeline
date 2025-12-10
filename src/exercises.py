"""
🎓 HANDS-ON EXERCISES: Student Feedback Analysis
================================================

Complete these exercises to practice sentiment analysis!
Each exercise builds on the previous one.

Run this file and follow the instructions.
"""

import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("="*60)
print("🎓 STUDENT FEEDBACK ANALYSIS - HANDS-ON EXERCISES")
print("="*60)
print()

# Check if analyzed data exists
if not os.path.exists('analyzed_feedback.csv'):
    print("⚠️  First, run the sentiment analysis pipeline:")
    print()
    print("   python ../run_pipeline.py \\")
    print("     --source-type csv \\")
    print("     --source student_feedback.csv \\")
    print("     --text-column feedback \\")
    print("     --output analyzed_feedback.csv")
    print()
    print("Then run this file again!")
    sys.exit(1)

# Load the data
df = pd.read_csv('analyzed_feedback.csv')

print(f"✓ Loaded {len(df)} student feedback responses")
print()

# ============================================================================
# EXERCISE 1: Basic Statistics
# ============================================================================
print("="*60)
print("EXERCISE 1: Understanding the Data")
print("="*60)
print()
print("Let's explore what we have:")
print()

# Show basic info
print("1️⃣  Dataset Overview:")
print(f"   - Total feedback: {len(df)}")
print(f"   - Number of courses: {df['course_name'].nunique()}")
print(f"   - Courses: {', '.join(df['course_name'].unique())}")
print()

# Sentiment distribution
print("2️⃣  Overall Sentiment Distribution:")
sentiment_counts = df['sentiment'].value_counts()
for sentiment, count in sentiment_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   - {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
print()

# Average scores
print("3️⃣  Average Scores:")
print(f"   - Average Rating: {df['rating'].mean():.2f} / 5")
print(f"   - Average Polarity: {df['polarity'].mean():.3f}")
print(f"   - Average Subjectivity: {df['subjectivity'].mean():.3f}")
print()

input("Press Enter to continue to Exercise 2...")
print()

# ============================================================================
# EXERCISE 2: Course Comparison
# ============================================================================
print("="*60)
print("EXERCISE 2: Which Course Needs Help?")
print("="*60)
print()

print("Let's analyze each course separately:")
print()

for course in sorted(df['course_name'].unique()):
    course_data = df[df['course_name'] == course]
    
    # Calculate statistics
    total = len(course_data)
    positive = (course_data['sentiment'] == 'positive').sum()
    negative = (course_data['sentiment'] == 'negative').sum()
    neutral = (course_data['sentiment'] == 'neutral').sum()
    avg_polarity = course_data['polarity'].mean()
    avg_rating = course_data['rating'].mean()
    
    # Determine status
    negative_pct = (negative / total) * 100
    if negative_pct > 30:
        status = "🚨 NEEDS ATTENTION"
    elif negative_pct < 15 and avg_polarity > 0.3:
        status = "✅ EXCELLENT"
    else:
        status = "📊 GOOD"
    
    print(f"📚 {course}")
    print(f"   Status: {status}")
    print(f"   Responses: {total}")
    print(f"   Positive: {positive} ({positive/total*100:.1f}%)")
    print(f"   Negative: {negative} ({negative/total*100:.1f}%)")
    print(f"   Neutral: {neutral} ({neutral/total*100:.1f}%)")
    print(f"   Avg Rating: {avg_rating:.2f} / 5")
    print(f"   Avg Polarity: {avg_polarity:+.3f}")
    print()

input("Press Enter to continue to Exercise 3...")
print()

# ============================================================================
# EXERCISE 3: Finding Specific Issues
# ============================================================================
print("="*60)
print("EXERCISE 3: What Are Students Complaining About?")
print("="*60)
print()

# Get negative feedback
negative_feedback = df[df['sentiment'] == 'negative'].sort_values('polarity')

print("🔍 Most Negative Feedback (Top 5):")
print()
for idx, row in negative_feedback.head(5).iterrows():
    print(f"📝 {row['course_name']} (Student {row['student_id']})")
    print(f"   Rating: {row['rating']}/5 | Polarity: {row['polarity']:.3f}")
    print(f"   Feedback: {row['feedback'][:100]}...")
    print()

# Common keywords in negative feedback
print("🔍 Common words in negative feedback:")
from collections import Counter
import re

negative_text = ' '.join(negative_feedback['feedback'].str.lower())
words = re.findall(r'\b\w+\b', negative_text)

# Common complaint words
complaint_words = ['difficult', 'confusing', 'bad', 'terrible', 'poor', 'frustrating', 
                   'disappointing', 'unclear', 'outdated', 'buggy', 'slow', 'fast',
                   'boring', 'waste', 'hard']

found_complaints = [(word, negative_text.count(word)) for word in complaint_words if word in negative_text]
found_complaints.sort(key=lambda x: x[1], reverse=True)

for word, count in found_complaints[:10]:
    print(f"   - '{word}': mentioned {count} times")
print()

input("Press Enter to continue to Exercise 4...")
print()

# ============================================================================
# EXERCISE 4: Success Stories
# ============================================================================
print("="*60)
print("EXERCISE 4: What's Working Well?")
print("="*60)
print()

# Get highly positive feedback
positive_feedback = df[df['sentiment'] == 'positive'].sort_values('polarity', ascending=False)

print("⭐ Most Positive Feedback (Top 5):")
print()
for idx, row in positive_feedback.head(5).iterrows():
    print(f"📝 {row['course_name']} (Student {row['student_id']})")
    print(f"   Rating: {row['rating']}/5 | Polarity: {row['polarity']:.3f}")
    print(f"   Feedback: {row['feedback'][:100]}...")
    print()

# Success keywords
print("⭐ Common words in positive feedback:")
positive_text = ' '.join(positive_feedback['feedback'].str.lower())

success_words = ['excellent', 'amazing', 'fantastic', 'great', 'love', 'best',
                 'wonderful', 'perfect', 'brilliant', 'outstanding', 'clear',
                 'helpful', 'engaging', 'practical', 'learned']

found_success = [(word, positive_text.count(word)) for word in success_words if word in positive_text]
found_success.sort(key=lambda x: x[1], reverse=True)

for word, count in found_success[:10]:
    print(f"   - '{word}': mentioned {count} times")
print()

input("Press Enter to continue to Exercise 5...")
print()

# ============================================================================
# EXERCISE 5: Action Items
# ============================================================================
print("="*60)
print("EXERCISE 5: Creating an Action Plan")
print("="*60)
print()

print("Based on our analysis, here are recommended actions:")
print()

for course in sorted(df['course_name'].unique()):
    course_data = df[df['course_name'] == course]
    negative_pct = (course_data['sentiment'] == 'negative').mean() * 100
    avg_polarity = course_data['polarity'].mean()
    
    print(f"📚 {course}")
    print(f"   Negative Feedback: {negative_pct:.1f}%")
    print(f"   Average Sentiment: {avg_polarity:+.3f}")
    print()
    print("   📋 Recommended Actions:")
    
    if negative_pct > 30:
        print("   🚨 URGENT:")
        print("   1. Schedule meeting with instructor immediately")
        print("   2. Review course structure and pacing")
        print("   3. Survey students for specific concerns")
        print("   4. Implement mid-semester improvements")
    elif negative_pct > 20:
        print("   ⚠️  NEEDS ATTENTION:")
        print("   1. Analyze negative feedback themes")
        print("   2. Meet with instructor to discuss improvements")
        print("   3. Monitor next few weeks closely")
    else:
        print("   ✅ MAINTAIN QUALITY:")
        print("   1. Document what's working well")
        print("   2. Share best practices with other instructors")
        print("   3. Use positive feedback for testimonials")
    
    # Specific issues
    course_negative = course_data[course_data['sentiment'] == 'negative']
    if len(course_negative) > 0:
        print()
        print("   🔍 Specific Issues to Address:")
        for idx, row in course_negative.head(3).iterrows():
            # Extract key issue
            feedback_lower = row['feedback'].lower()
            if 'pace' in feedback_lower or 'fast' in feedback_lower or 'slow' in feedback_lower:
                print("   - Review course pacing")
            if 'confusing' in feedback_lower or 'unclear' in feedback_lower:
                print("   - Improve clarity of instructions")
            if 'difficult' in feedback_lower or 'hard' in feedback_lower:
                print("   - Provide additional support/resources")
            if 'outdated' in feedback_lower or 'buggy' in feedback_lower:
                print("   - Update course materials/platform")
    
    print()

print()
print("="*60)
print("🎉 EXERCISES COMPLETE!")
print("="*60)
print()
print("What you've learned:")
print("✓ How to load and analyze sentiment data")
print("✓ How to compare courses using metrics")
print("✓ How to identify specific issues from feedback")
print("✓ How to find success patterns")
print("✓ How to create actionable plans from data")
print()
print("Next Steps:")
print("1. Try analyzing your own feedback data")
print("2. Create visualizations with matplotlib")
print("3. Build an automated reporting system")
print("4. Experiment with different sentiment thresholds")
print()
print("Happy analyzing! 📊")
