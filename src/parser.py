"""
Parser module for extracting narrative content from Project Gutenberg slave narrative files.
"""

import re
from typing import List, Dict, Optional


def parse_narrative_file(filepath: str, state: str) -> Dict:
    """
    Parse a single narrative file and extract individual narratives.

    Args:
        filepath: Path to the narrative text file
        state: Name of the state (e.g., 'Georgia', 'Florida')

    Returns:
        Dictionary containing parsed narratives and metadata
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of actual narratives (after Project Gutenberg header)
    start_marker = "*** START OF"
    start_idx = content.find(start_marker)
    if start_idx != -1:
        # Find the end of the marker line and skip some header material
        content = content[start_idx:]
        # Look for common patterns that indicate narrative start
        narrative_start = re.search(r'\n\n[A-Z][A-Z\s]+(?:NARRATIVES|PART \d+)\n', content)
        if narrative_start:
            content = content[narrative_start.end():]

    # Extract individual narratives
    narratives = []

    # Pattern to match narrative headers (NAME, Age XX)
    header_pattern = r'\n\n([A-Z][A-Z\s\.]+(?:JR\.|SR\.)?),?\s+Age\s+(\d+)'

    # Split by narrative headers
    splits = re.split(header_pattern, content)

    # Process splits (first element is usually preamble, then name, age, text, name, age, text...)
    for i in range(1, len(splits), 3):
        if i + 2 <= len(splits):
            name = splits[i].strip()
            age = splits[i + 1].strip()
            text = splits[i + 2].strip()

            # Extract address if present (usually on first line after name)
            address_match = re.match(r'([^\n]+)\n', text)
            address = address_match.group(1).strip() if address_match else ""

            # Clean up the text - remove metadata sections
            # Look for the actual narrative start (after "Written by", "Edited by", etc.)
            text_lines = text.split('\n')
            narrative_start_idx = 0

            for idx, line in enumerate(text_lines):
                if line.strip() and not any(marker in line for marker in
                    ['Written by:', 'Edited by:', 'District Supervisor', 'Federal Writers',
                     'Athens', 'Augusta', 'and', '[HW:', '[TR:']):
                    # Skip the address line and empty lines
                    if idx > 0 and len(line) > 50:  # Actual narrative text is usually longer
                        narrative_start_idx = idx
                        break

            narrative_text = '\n'.join(text_lines[narrative_start_idx:]).strip()

            # Only add if we have substantial narrative text
            if len(narrative_text) > 100:
                narratives.append({
                    'name': name,
                    'age': age,
                    'address': address,
                    'state': state,
                    'text': narrative_text,
                    'word_count': len(narrative_text.split())
                })

    return {
        'state': state,
        'narrative_count': len(narratives),
        'narratives': narratives
    }


def get_all_narratives() -> Dict[str, Dict]:
    """
    Parse all narrative files and return organized data.

    Returns:
        Dictionary mapping state names to their narrative data
    """
    narrative_files = {
        'Georgia': 'narratives/GEORGIA NARRATIVES  PART 1.txt',
        'Florida': 'narratives/Volume III, Florida Narratives.txt',
        'Missouri': 'narratives/for the State of Missouri.txt',
        'Texas': 'narratives/Slave Narratives_ A Folk History of Slavery in the United States from Interviews with Former Slaves, Volume XVI, Texas Narratives, Part 3.txt',
        'South Carolina': 'narratives/Untitled document.txt'
    }

    all_data = {}
    for state, filepath in narrative_files.items():
        print(f"Parsing {state} narratives...")
        all_data[state] = parse_narrative_file(filepath, state)

    return all_data
