# WPA Slave Narratives Comparative Analysis

A static website for analyzing and comparing historical slave narratives from the WPA Federal Writers' Project (1936-1938). This project provides comparative analysis of themes, folklore, and textual patterns across narratives from five states: Georgia, Florida, Missouri, Texas, and South Carolina.

**✨ No server required!** This is a pure HTML/CSS/JavaScript website that can be opened directly in your browser or hosted on any static web hosting service.

## Features

- **Browse Narratives**: Read individual narratives with filtering by state, name, and length
- **Comparative Analysis**: Compare theme distribution across states
- **Folklore Extraction**: Identify and analyze folklore, ghost stories, conjure tales, and folk medicine references
- **Interactive Visualizations**: Explore data through interactive Plotly charts
- **Word Frequency Analysis**: See the most common words used in each state's narratives
- **Works Offline**: Once loaded, everything runs in your browser

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Week-14-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the analysis script to generate data:
```bash
python src/analyze_narratives.py
```

This will parse all narrative files and create JSON data files in the `data/` directory.

5. View the website:

**Option A: Direct file opening (quick preview)**
- Simply double-click `index.html` to open it in your browser
- Note: Some browsers may block JSON loading due to CORS

**Option B: Using a local server (recommended)**
```bash
# Python
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

## Project Structure

```
Week-14-project/
├── index.html           # Home page
├── browse.html          # Browse narratives page
├── compare.html         # Comparison visualizations page
├── narratives/          # Original text files from Project Gutenberg
├── src/                 # Python analysis scripts
│   ├── parser.py       # Parses narrative files
│   ├── analysis.py     # Analyzes themes and folklore
│   └── analyze_narratives.py  # Main analysis script
├── data/                # Generated JSON files (created by analysis script)
├── webapp/              # Flask version (legacy, not used)
└── requirements.txt     # Python dependencies for analysis
```

## Deployment to Static Hosting

Since this is a static website, deployment is extremely simple!

### GitHub Pages (Free)

1. Run analysis to generate data files:
   ```bash
   python src/analyze_narratives.py
   ```

2. Commit the data files (remove `data/` from .gitignore or use `git add -f data/`)

3. Push to GitHub

4. Go to repository Settings → Pages
   - Select your branch (e.g., main)
   - Select root directory
   - Save

5. Your site will be live at `https://yourusername.github.io/repository-name/`

### Netlify (Free)

1. Generate data files: `python src/analyze_narratives.py`
2. Drag and drop the entire project folder to Netlify
3. Done! Your site is live

### Vercel (Free)

1. Generate data files: `python src/analyze_narratives.py`
2. Install Vercel CLI: `npm i -g vercel`
3. Run `vercel` in the project directory
4. Done!

**Important**: Make sure to run `python src/analyze_narratives.py` before deploying to generate the required data files in the `data/` directory.

## Data Sources

All narrative texts are from Project Gutenberg:
- Public domain historical documents
- WPA Federal Writers' Project (1936-1938)
- Interviews with formerly enslaved people

## Analysis Methods

### Theme Detection
The analysis identifies 10 major themes:
- Family & Separation
- Work & Labor
- Food & Sustenance
- Clothing & Material Life
- Housing & Living Conditions
- Religion & Spirituality
- Punishment & Violence
- Freedom & Emancipation
- Master & Slavery Relations
- Folklore & Supernatural

### Folklore Extraction
Identifies and categorizes:
- Ghost stories and hauntings
- Conjure and magic references
- Supernatural beliefs
- Folk medicine practices
- Songs and music
- Folk tales and storytelling

## License

The historical documents are in the public domain (Project Gutenberg).
The analysis code is available under the MIT License.

## Acknowledgments

- Project Gutenberg for digitizing and providing access to these historical documents
- The Federal Writers' Project workers who conducted and transcribed these interviews
- The formerly enslaved individuals who shared their stories
