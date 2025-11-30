"""
Flask web application for browsing and comparing slave narratives.
"""

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Load data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def load_json(filename):
    """Load a JSON file from the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


@app.route('/')
def index():
    """Home page with overview and summary statistics."""
    stats = load_json('comparative_stats.json')
    return render_template('index.html', stats=stats)


@app.route('/browse')
def browse():
    """Browse narratives with filtering options."""
    narratives = load_json('narratives_full.json')
    stats = load_json('comparative_stats.json')
    return render_template('browse.html', narratives=narratives, stats=stats)


@app.route('/compare')
def compare():
    """Compare themes and folklore across states."""
    themes = load_json('themes.json')
    folklore = load_json('folklore.json')
    stats = load_json('comparative_stats.json')
    word_freq = load_json('word_frequencies.json')

    return render_template('compare.html',
                          themes=themes,
                          folklore=folklore,
                          stats=stats,
                          word_freq=word_freq)


@app.route('/api/narratives/<state>')
def get_narratives(state):
    """API endpoint to get narratives for a specific state."""
    narratives = load_json('narratives_full.json')
    if narratives and state in narratives:
        return jsonify(narratives[state])
    return jsonify({'error': 'State not found'}), 404


@app.route('/api/themes')
def get_themes():
    """API endpoint to get theme analysis data."""
    themes = load_json('themes.json')
    return jsonify(themes) if themes else jsonify({'error': 'Data not found'}), 404


@app.route('/api/folklore')
def get_folklore():
    """API endpoint to get folklore analysis data."""
    folklore = load_json('folklore.json')
    return jsonify(folklore) if folklore else jsonify({'error': 'Data not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
