"""
Analysis module for extracting themes and folklore from slave narratives.
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Set
import string


class NarrativeAnalyzer:
    """Analyzer for extracting themes and patterns from narratives."""

    # Define theme keywords for categorization
    THEME_KEYWORDS = {
        'Family & Separation': [
            'mother', 'father', 'ma', 'pa', 'mama', 'papa', 'children', 'child',
            'son', 'daughter', 'family', 'sold', 'separated', 'brother', 'sister',
            'husband', 'wife', 'baby', 'babies', 'kin', 'kinfolk'
        ],
        'Work & Labor': [
            'work', 'field', 'cotton', 'plantation', 'plow', 'hoe', 'chop',
            'pick', 'harvest', 'labor', 'task', 'job', 'cook', 'weave', 'spin',
            'tobacco', 'rice', 'corn', 'crops'
        ],
        'Food & Sustenance': [
            'eat', 'food', 'bread', 'meat', 'cornbread', 'molasses', 'syrup',
            'possum', 'rabbit', 'fish', 'cook', 'meal', 'supper', 'dinner',
            'breakfast', 'hungry', 'garden', 'taters', 'potatoes', 'peas'
        ],
        'Clothing & Material Life': [
            'clothes', 'dress', 'shirt', 'shoes', 'barefoot', 'wear', 'cloth',
            'wool', 'cotton', 'homespun', 'weave', 'sew', 'coat', 'hat'
        ],
        'Housing & Living Conditions': [
            'cabin', 'house', 'quarters', 'room', 'chimney', 'fireplace',
            'bed', 'sleep', 'floor', 'roof', 'door', 'window', 'log'
        ],
        'Religion & Spirituality': [
            'pray', 'prayer', 'church', 'preacher', 'god', 'lord', 'jesus',
            'bible', 'heaven', 'baptize', 'sin', 'soul', 'sunday', 'sing',
            'hymn', 'meeting', 'religion'
        ],
        'Punishment & Violence': [
            'whip', 'whipped', 'beat', 'lash', 'punish', 'overseer', 'paddle',
            'stripe', 'blood', 'cruel', 'mean', 'hurt', 'hit', 'strike'
        ],
        'Freedom & Emancipation': [
            'free', 'freedom', 'emancipation', 'yankee', 'lincoln', 'war',
            'soldier', 'run away', 'escape', 'liberty', 'surrender'
        ],
        'Master & Slavery Relations': [
            'master', 'mistress', 'marse', 'missus', 'owner', 'belong',
            'slave', 'slavery', 'servant', 'marster', 'massa'
        ],
        'Folklore & Supernatural': [
            'ghost', 'haint', 'witch', 'conjure', 'charm', 'spell', 'spirit',
            'haunt', 'voodoo', 'luck', 'sign', 'omen', 'magic', 'root',
            'doctor', 'potion', 'hex'
        ]
    }

    # Folklore-specific patterns
    FOLKLORE_PATTERNS = {
        'Ghost Stories': ['ghost', 'haint', 'haunt', 'spirit', 'dead', 'cemetery', 'graveyard'],
        'Conjure & Magic': ['conjure', 'conjurer', 'conjur', 'witch', 'charm', 'spell', 'hex', 'root doctor', 'voodoo'],
        'Supernatural Beliefs': ['sign', 'omen', 'luck', 'unlucky', 'fortune', 'predict', 'dream'],
        'Folk Medicine': ['remedy', 'cure', 'herb', 'tea', 'poultice', 'doctor', 'sick', 'medicine'],
        'Songs & Music': ['sing', 'song', 'spiritual', 'hymn', 'music', 'fiddle', 'banjo', 'dance'],
        'Stories & Tales': ['story', 'tale', 'tell', 'told', 'heard', 'say', 'remember']
    }

    def __init__(self, narratives_by_state: Dict):
        """Initialize analyzer with parsed narratives."""
        self.narratives_by_state = narratives_by_state

    def analyze_themes(self) -> Dict:
        """
        Analyze theme distribution across all states.

        Returns:
            Dictionary with theme analysis for each state
        """
        theme_analysis = {}

        for state, data in self.narratives_by_state.items():
            state_themes = defaultdict(int)
            total_words = 0

            for narrative in data['narratives']:
                text_lower = narrative['text'].lower()
                words = text_lower.split()
                total_words += len(words)

                # Count theme keywords
                for theme, keywords in self.THEME_KEYWORDS.items():
                    for keyword in keywords:
                        # Use word boundary matching
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        count = len(re.findall(pattern, text_lower))
                        state_themes[theme] += count

            theme_analysis[state] = {
                'themes': dict(state_themes),
                'total_words': total_words,
                'narrative_count': len(data['narratives'])
            }

        return theme_analysis

    def extract_folklore(self) -> Dict:
        """
        Extract folklore and folk tale references from narratives.

        Returns:
            Dictionary with folklore analysis for each state
        """
        folklore_analysis = {}

        for state, data in self.narratives_by_state.items():
            folklore_counts = defaultdict(int)
            folklore_examples = defaultdict(list)

            for narrative in data['narratives']:
                text_lower = narrative['text'].lower()

                # Count folklore pattern occurrences
                for category, keywords in self.FOLKLORE_PATTERNS.items():
                    for keyword in keywords:
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        matches = re.finditer(pattern, text_lower)

                        for match in matches:
                            folklore_counts[category] += 1

                            # Extract a snippet around the match for context
                            start = max(0, match.start() - 100)
                            end = min(len(narrative['text']), match.end() + 100)
                            snippet = narrative['text'][start:end].strip()

                            # Only keep first 5 examples per category
                            if len(folklore_examples[category]) < 5:
                                folklore_examples[category].append({
                                    'name': narrative['name'],
                                    'snippet': snippet
                                })

            folklore_analysis[state] = {
                'folklore_counts': dict(folklore_counts),
                'examples': {k: v for k, v in folklore_examples.items() if v}
            }

        return folklore_analysis

    def get_word_frequencies(self, top_n: int = 100) -> Dict:
        """
        Get most common words for each state (excluding common stop words).

        Args:
            top_n: Number of top words to return

        Returns:
            Dictionary mapping states to their top words
        """
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'were', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'so',
            'than', 'too', 'very', 'just', 'there', 'here', 'then', 'now', 'said',
            'her', 'his', 'my', 'our', 'your', 'me', 'him', 'us', 'one', 'two',
            'three', 'not', 'no', 'yes', 'up', 'down', 'out', 'about', 'into'
        }

        word_frequencies = {}

        for state, data in self.narratives_by_state.items():
            all_words = []

            for narrative in data['narratives']:
                # Clean and tokenize
                text_lower = narrative['text'].lower()
                # Remove punctuation
                text_clean = text_lower.translate(str.maketrans('', '', string.punctuation))
                words = text_clean.split()

                # Filter stop words and short words
                filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
                all_words.extend(filtered_words)

            # Count and get top N
            word_counts = Counter(all_words)
            word_frequencies[state] = word_counts.most_common(top_n)

        return word_frequencies

    def get_comparative_stats(self) -> Dict:
        """
        Get comparative statistics across states.

        Returns:
            Dictionary with comparative statistics
        """
        stats = {}

        for state, data in self.narratives_by_state.items():
            narratives = data['narratives']
            word_counts = [n['word_count'] for n in narratives]

            stats[state] = {
                'narrative_count': len(narratives),
                'total_words': sum(word_counts),
                'avg_narrative_length': sum(word_counts) / len(narratives) if narratives else 0,
                'shortest_narrative': min(word_counts) if word_counts else 0,
                'longest_narrative': max(word_counts) if word_counts else 0,
                'total_people_interviewed': len(narratives)
            }

        return stats
