#!/usr/bin/env python3
"""
Main script to analyze slave narratives and generate JSON data for web interface.
"""

import json
import os
from parser import get_all_narratives
from analysis import NarrativeAnalyzer


def main():
    """Main execution function."""
    print("=" * 60)
    print("Slave Narratives Comparative Analysis")
    print("=" * 60)
    print()

    # Step 1: Parse all narrative files
    print("Step 1: Parsing narrative files...")
    narratives_data = get_all_narratives()
    print(f"✓ Parsed narratives from {len(narratives_data)} states")
    print()

    # Step 2: Initialize analyzer
    print("Step 2: Initializing analyzer...")
    analyzer = NarrativeAnalyzer(narratives_data)
    print("✓ Analyzer initialized")
    print()

    # Step 3: Analyze themes
    print("Step 3: Analyzing themes across states...")
    theme_analysis = analyzer.analyze_themes()
    print("✓ Theme analysis complete")
    print()

    # Step 4: Extract folklore
    print("Step 4: Extracting folklore and folk tales...")
    folklore_analysis = analyzer.extract_folklore()
    print("✓ Folklore extraction complete")
    print()

    # Step 5: Get word frequencies
    print("Step 5: Calculating word frequencies...")
    word_frequencies = analyzer.get_word_frequencies(top_n=50)
    print("✓ Word frequency analysis complete")
    print()

    # Step 6: Get comparative statistics
    print("Step 6: Generating comparative statistics...")
    comparative_stats = analyzer.get_comparative_stats()
    print("✓ Comparative statistics generated")
    print()

    # Step 7: Save all data to JSON files
    print("Step 7: Saving results to data/ directory...")

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Save narratives (without full text to reduce size)
    narratives_summary = {}
    for state, data in narratives_data.items():
        narratives_summary[state] = {
            'narrative_count': data['narrative_count'],
            'narratives': [
                {
                    'name': n['name'],
                    'age': n['age'],
                    'address': n['address'],
                    'word_count': n['word_count'],
                    'text_preview': n['text'][:500] + '...' if len(n['text']) > 500 else n['text']
                }
                for n in data['narratives']
            ]
        }

    with open('data/narratives.json', 'w', encoding='utf-8') as f:
        json.dump(narratives_summary, f, indent=2)
    print("  ✓ narratives.json")

    # Save full narratives for detailed view
    with open('data/narratives_full.json', 'w', encoding='utf-8') as f:
        json.dump(narratives_data, f, indent=2)
    print("  ✓ narratives_full.json")

    # Save theme analysis
    with open('data/themes.json', 'w', encoding='utf-8') as f:
        json.dump(theme_analysis, f, indent=2)
    print("  ✓ themes.json")

    # Save folklore analysis
    with open('data/folklore.json', 'w', encoding='utf-8') as f:
        json.dump(folklore_analysis, f, indent=2)
    print("  ✓ folklore.json")

    # Save word frequencies
    with open('data/word_frequencies.json', 'w', encoding='utf-8') as f:
        json.dump(word_frequencies, f, indent=2)
    print("  ✓ word_frequencies.json")

    # Save comparative stats
    with open('data/comparative_stats.json', 'w', encoding='utf-8') as f:
        json.dump(comparative_stats, f, indent=2)
    print("  ✓ comparative_stats.json")

    print()
    print("=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print()
    print("Summary:")
    for state, stats in comparative_stats.items():
        print(f"  {state}: {stats['narrative_count']} narratives, "
              f"{stats['total_words']:,} total words")
    print()
    print("All data files saved to data/ directory")
    print("You can now run the web application with: python webapp/app.py")
    print()


if __name__ == '__main__':
    main()
