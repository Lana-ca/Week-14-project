# WPA Slave Narratives Comparative Analysis

A web-based tool for analyzing and comparing historical slave narratives from the WPA Federal Writers' Project (1936-1938). This project provides comparative analysis of themes, folklore, and textual patterns across narratives from five states: Georgia, Florida, Missouri, Texas, and South Carolina.

## Features

- **Browse Narratives**: Read individual narratives with filtering by state, name, and length
- **Comparative Analysis**: Compare theme distribution across states
- **Folklore Extraction**: Identify and analyze folklore, ghost stories, conjure tales, and folk medicine references
- **Interactive Visualizations**: Explore data through interactive charts and statistics
- **Word Frequency Analysis**: See the most common words used in each state's narratives

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

5. Start the web application:
```bash
python webapp/app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
Week-14-project/
├── narratives/          # Original text files from Project Gutenberg
├── src/
│   ├── parser.py       # Parses narrative files and extracts content
│   ├── analysis.py     # Analyzes themes and folklore
│   └── analyze_narratives.py  # Main analysis script
├── webapp/
│   ├── app.py          # Flask application
│   ├── templates/      # HTML templates
│   └── static/         # CSS, JS (currently using CDN)
├── data/               # Generated JSON analysis files (created by script)
├── requirements.txt    # Python dependencies
└── README.md
```

## Deployment

### Deploy to Render

1. Create a `Procfile` in the project root:
```
web: gunicorn webapp.app:app
```

2. Push your code to GitHub

3. Create a new Web Service on [Render](https://render.com):
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt && python src/analyze_narratives.py`
   - Set start command: `gunicorn webapp.app:app`
   - Set environment: Python 3

### Deploy to Heroku

1. Install the Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Create a `Procfile` in the project root:
```
web: gunicorn webapp.app:app
```

4. Deploy:
```bash
git push heroku main
```

5. Run the analysis script on Heroku:
```bash
heroku run python src/analyze_narratives.py
```

### Deploy to PythonAnywhere

1. Upload your code to PythonAnywhere
2. Create a virtual environment and install dependencies
3. Run the analysis script: `python src/analyze_narratives.py`
4. Configure a web app pointing to `webapp/app.py`
5. Set the WSGI configuration to use Flask

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
