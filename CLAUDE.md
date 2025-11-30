# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python-based web application for analyzing and comparing WPA Federal Writers' Project slave narratives from the 1930s. The project consists of:

1. **Analysis Pipeline**: Python scripts that parse historical text files and extract themes, folklore, and statistical data
2. **Web Application**: Flask-based interface for browsing narratives and viewing comparative analysis
3. **Historical Documents**: Five Project Gutenberg text files containing slave narratives from Georgia, Florida, Missouri, Texas, and South Carolina

## Project Architecture

### Analysis Pipeline (src/)

The analysis workflow follows this sequence:

1. **parser.py** - Parses Project Gutenberg text files to extract individual narratives with metadata (name, age, address, text)
2. **analysis.py** - NarrativeAnalyzer class performs:
   - Theme detection using keyword matching (10 major themes)
   - Folklore extraction (6 categories: ghost stories, conjure/magic, supernatural beliefs, folk medicine, songs/music, tales)
   - Word frequency analysis with stop word filtering
   - Comparative statistics across states
3. **analyze_narratives.py** - Main script that orchestrates the pipeline and outputs JSON files to data/

### Web Application (webapp/)

Flask application with three main routes:

- **/** (index.html) - Overview with summary statistics for each state
- **/browse** (browse.html) - Interactive narrative browser with filtering by state/name and sorting options
- **/compare** (compare.html) - Comparative visualizations using Plotly.js:
  - Theme distribution bar charts
  - Folklore category comparisons
  - Statistical comparisons (narrative counts, avg lengths)
  - Top word frequencies by state

The app loads pre-generated JSON files from data/ (no runtime analysis).

## Common Commands

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Analysis

```bash
# Parse narratives and generate analysis data
python src/analyze_narratives.py
```

This creates JSON files in data/:
- narratives.json (summaries with text previews)
- narratives_full.json (complete narrative texts)
- themes.json (theme frequency by state)
- folklore.json (folklore categories and examples)
- word_frequencies.json (top 50 words per state)
- comparative_stats.json (statistics for each state)

### Running Web Application

```bash
# Development server (local only)
python webapp/app.py

# Production server
gunicorn webapp.app:app
```

Access at http://localhost:5000

## Development Notes

### Adding New Analysis Features

To add new themes or folklore categories:

1. Edit `src/analysis.py`
2. Add keywords to `THEME_KEYWORDS` or `FOLKLORE_PATTERNS` dictionaries
3. Re-run `python src/analyze_narratives.py` to regenerate data files
4. Update templates if new visualizations are needed

### Modifying Narrative Parsing

If narrative file structure differs or new files are added:

1. Update `parse_narrative_file()` in `src/parser.py`
2. Adjust regex patterns for header matching
3. Update `get_all_narratives()` file mapping
4. Re-run analysis script

### Deployment

The application requires two steps for deployment:

1. **Build step**: Run `python src/analyze_narratives.py` to generate data/
2. **Runtime**: Start Flask app with `gunicorn webapp.app:app`

See README.md for platform-specific deployment instructions (Render, Heroku, PythonAnywhere).

## File Organization

```
narratives/          - Original .txt files (read-only historical documents)
src/                 - Analysis Python modules
webapp/              - Flask application
  app.py            - Routes and API endpoints
  templates/        - Jinja2 HTML templates
  static/           - Currently unused (using CDN for Bootstrap/Plotly)
data/               - Generated JSON files (gitignored, created by analysis script)
```

## Key Design Decisions

1. **Pre-computation**: Analysis runs once to generate JSON files rather than on-demand processing
2. **No database**: Uses JSON files for simplicity and portability
3. **CDN dependencies**: Bootstrap and Plotly loaded from CDN (no local static files)
4. **No testing framework**: This is a data analysis tool, not production software
5. **Simple theme detection**: Keyword-based matching rather than NLP/ML for transparency and interpretability

## Historical Context

These are sensitive historical documents containing:
- First-person accounts of slavery
- Period-specific language and dialect transcriptions
- References to violence, family separation, and trauma

Handle with awareness of their cultural and historical significance.
