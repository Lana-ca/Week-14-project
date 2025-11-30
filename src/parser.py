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
        content = content[start_idx:]

    narratives = []

    # Georgia format: NAME, Age XX
    if state == 'Georgia':
        pattern = r'\n\n([A-Z][A-Z\s\.]+(?:JR\.|SR\.)?),?\s+Age\s+(\d+)'
        splits = re.split(pattern, content)

        for i in range(1, len(splits), 3):
            if i + 2 <= len(splits):
                name = splits[i].strip()
                age = splits[i + 1].strip()
                text = splits[i + 2].strip()

                # Extract address
                address_match = re.match(r'([^\n]+)\n', text)
                address = address_match.group(1).strip() if address_match else ""

                # Clean narrative text - skip metadata
                text_lines = text.split('\n')
                narrative_start_idx = 0

                for idx, line in enumerate(text_lines):
                    if line.strip() and not any(marker in line for marker in
                        ['Written by:', 'Edited by:', 'District Supervisor', 'Federal Writers',
                         'Athens', 'Augusta', 'and', '[HW:', '[TR:']):
                        if idx > 0 and len(line) > 50:
                            narrative_start_idx = idx
                            break

                narrative_text = '\n'.join(text_lines[narrative_start_idx:]).strip()

                if len(narrative_text) > 100:
                    narratives.append({
                        'name': name,
                        'age': age,
                        'address': address,
                        'state': state,
                        'text': narrative_text,
                        'word_count': len(narrative_text.split())
                    })

    # Florida format: NAME (all caps standalone)
    elif state == 'Florida':
        # Look for all-caps names followed by optional title and narrative
        pattern = r'\n\n([A-Z][A-Z\s]{2,})\n\n'
        matches = list(re.finditer(pattern, content))

        for i, match in enumerate(matches):
            name = match.group(1).strip()
            # Skip if it's a section header
            if name in ['FOLK STUFF', 'HANTS', 'SLAVE NARRATIVES', 'TYPEWRITTEN RECORDS']:
                continue

            start = match.end()
            # Find next narrative or end of file
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            text = content[start:end].strip()

            # Skip short sections and metadata
            if len(text) > 200 and '"' in text:
                # Try to extract age if mentioned
                age_match = re.search(r'(\d{2,3})\s+year', text)
                age = age_match.group(1) if age_match else "Unknown"

                narratives.append({
                    'name': name,
                    'age': age,
                    'address': "Florida",
                    'state': state,
                    'text': text,
                    'word_count': len(text.split())
                })

    # Missouri format: Name followed by *Interview with Name*
    elif state == 'Missouri':
        # Look for pattern: Name\n\n\n    *Interview with Name,*
        pattern = r'\n\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\n\n\n+\s+\*Interview with'
        matches = list(re.finditer(pattern, content))

        for i, match in enumerate(matches):
            name = match.group(1).strip()
            start = match.end()

            # Find narrative start (after location line)
            text_start = content.find('\n\n', start) + 2

            # Find next narrative or end
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            text = content[text_start:end].strip()

            if len(text) > 200:
                # Try to extract age
                age_match = re.search(r'born.*?(\d{4})', text) or re.search(r'(\d{2,3})\s+year', text)
                age = "Unknown"
                if age_match:
                    year = age_match.group(1)
                    if len(year) == 4:
                        age = str(1937 - int(year))  # Approximate age at interview time
                    else:
                        age = year

                narratives.append({
                    'name': name,
                    'age': age,
                    'address': "Missouri",
                    'state': state,
                    'text': text,
                    'word_count': len(text.split())
                })

    # Texas format: Name\n\n\n*Description*\n\n"Quote starts
    elif state == 'Texas':
        # Look for pattern: Name followed by blank lines and asterisk paragraph
        pattern = r'\n\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\n\n\n+\*'
        matches = list(re.finditer(pattern, content))

        for i, match in enumerate(matches):
            name = match.group(1).strip()
            start = match.start()
            # Find next narrative or end
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            text = content[start:end].strip()

            if len(text) > 300:
                # Extract age from description
                age_match = re.search(r'(\d{2,3})\s+years?\s+(?:old|of age)', text)
                age = age_match.group(1) if age_match else "Unknown"

                narratives.append({
                    'name': name,
                    'age': age,
                    'address': state,
                    'state': state,
                    'text': text,
                    'word_count': len(text.split())
                })

    # South Carolina: =NAME= format (has Windows line endings)
    elif state == 'South Carolina':
        # Normalize line endings first
        content = content.replace('\r\n', '\n').replace('\r', '\n')

        # Look for pattern: =NAME= followed by =_EX-SLAVE description_=
        pattern = r'=([A-Z][A-Z\s]+)=\s+=_EX-SLAVE'
        matches = list(re.finditer(pattern, content))

        for i, match in enumerate(matches):
            name = match.group(1).strip()
            start = match.start()
            # Find next narrative or end
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            text = content[start:end].strip()

            if len(text) > 300:
                # Extract age from EX-SLAVE line
                age_match = re.search(r'EX-SLAVE (\d{2,3}) YEARS OLD', text)
                age = age_match.group(1) if age_match else "Unknown"

                narratives.append({
                    'name': name,
                    'age': age,
                    'address': state,
                    'state': state,
                    'text': text,
                    'word_count': len(text.split())
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
        print(f"  Found {all_data[state]['narrative_count']} narratives")

    return all_data
