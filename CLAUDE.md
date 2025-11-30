# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a static website with Python analysis tools for exploring WPA Federal Writers' Project slave narratives from the 1930s. The project consists of:

1. **Analysis Pipeline**: Python scripts that parse historical text files and extract themes, folklore, and statistical data
2. **Static Website**: HTML/CSS/JavaScript interface for browsing narratives and viewing comparative analysis (no server required)
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

### Static Website (HTML files in root)

Three standalone HTML pages that can be opened directly in a browser:

- **index.html** - Overview with summary statistics for each state
- **browse.html** - Interactive narrative browser with filtering by state/name and sorting options
- **compare.html** - Comparative visualizations using Plotly.js:
  - Theme distribution bar charts
  - Folklore category comparisons
  - Statistical comparisons (narrative counts, avg lengths)
  - Top word frequencies by state

All pages load pre-generated JSON files from data/ using JavaScript fetch API. No server required for local viewing (files can be opened directly), though a simple HTTP server is recommended for full functionality.

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

### Viewing the Website

**Option 1: Direct file opening (quick preview)**
- Simply open `index.html` in your web browser
- Note: Some browsers may block fetch() requests for local files due to CORS policy

**Option 2: Simple HTTP server (recommended)**
```bash
# Using Python (recommended)
python -m http.server 8000

# Or using PHP
php -S localhost:8000

# Or using Node.js (if installed)
npx http-server -p 8000
```

Then access at http://localhost:8000

**Option 3: Deploy to static hosting**
- Upload all files to GitHub Pages, Netlify, Vercel, or any static host
- No build step required, just upload the directory

## Development Notes

### Adding New Analysis Features

To add new themes or folklore categories:

1. Edit `src/analysis.py`
2. Add keywords to `THEME_KEYWORDS` or `FOLKLORE_PATTERNS` dictionaries
3. Re-run `python src/analyze_narratives.py` to regenerate data files
4. Update templates if new visualizations are needed

### Modifying Narrative Parsing

The parser uses state-specific regex patterns to extract narratives from each state's unique text format:

- **Georgia**: "NAME, Age XX" format (currently extracts 5 narratives)
- **Florida**: "NAME" in all-caps standalone (currently extracts 27 narratives)
- **Missouri**: "Name\n*Interview with Name*" format (currently extracts 37 narratives)
- **Texas**: "Name\n\n\n*Description*" format (currently extracts 23 narratives)
- **South Carolina**: "=NAME=\n=_EX-SLAVE XX YEARS OLD_=" format (currently extracts 7 narratives)

**Current status**: Parser successfully extracts **99 narratives** from all 5 states (total 200,013 words).

To modify or improve parsing:

1. Examine the text structure in `narratives/[state-file].txt`
2. Update state-specific regex patterns in `src/parser.py` (lines 32-198)
3. For South Carolina, note the Windows line ending normalization (line 172)
4. Test by running `python src/analyze_narratives.py` and verifying output counts
5. Update `get_all_narratives()` file mapping if adding new narrative files

### Deployment

**For static hosting (GitHub Pages, Netlify, Vercel):**

1. **Build step**: Run `python src/analyze_narratives.py` to generate data/
2. **Commit data files**: Remove `data/` from .gitignore or manually upload data/ folder
3. **Deploy**: Push to your static hosting service (no build command needed)

**For GitHub Pages:**
- Go to repository Settings → Pages
- Select branch (e.g., main)
- Set root directory as source
- Site will be live at `https://username.github.io/repository-name/`

No server-side code - everything runs in the browser!

## File Organization

```
narratives/          - Original .txt files (read-only historical documents)
src/                 - Analysis Python modules (parser, analysis, main script)
webapp/              - Flask application (legacy - not used in static version)
index.html           - Home page (static)
browse.html          - Browse narratives page (static)
compare.html         - Comparison visualizations page (static)
data/                - Generated JSON files (gitignored by default, created by analysis script)
```

**Note**: The webapp/ directory contains the original Flask version but is no longer used. The static HTML files in the root directory provide the same functionality without requiring a server.

## Key Design Decisions

1. **Static website**: Pure HTML/CSS/JavaScript - no server required, works anywhere
2. **Pre-computation**: Analysis runs once to generate JSON files rather than on-demand processing
3. **No database**: Uses JSON files for simplicity and portability
4. **CDN dependencies**: Bootstrap and Plotly loaded from CDN (no local static files needed)
5. **No build process**: HTML files work as-is, no webpack/bundling required
6. **No testing framework**: This is a data analysis tool, not production software
7. **Simple theme detection**: Keyword-based matching rather than NLP/ML for transparency and interpretability

## Historical Context

These are sensitive historical documents containing:
- First-person accounts of slavery
- Period-specific language and dialect transcriptions
- References to violence, family separation, and trauma

Handle with awareness of their cultural and historical significance.
