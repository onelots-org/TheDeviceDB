import cloudscraper
from bs4 import BeautifulSoup
import re
import json
import random

file_path = "../resources/mediatek_socs.json"

with open("../resources/headers.json", "r") as f:
    headers_list = json.load(f)

def fetch_wikipedia_page():
    url = "https://en.wikipedia.org/wiki/List_of_MediaTek_systems_on_chips"
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(random.choice(headers_list))
    response = scraper.get(url)
    response.raise_for_status()
    return response.text


def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\[\s*\w+\s*\]', '', text)  # [66], [a], etc.
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_mt_numbers(text):
    found = re.findall(r'MT\d+', text)
    seen = []
    for m in found:
        if m not in seen:
            seen.append(m)
    return seen


FAMILIES = ("Helio", "Dimensity", "Genio")


def parse_mediatek(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    aliases = {}

    for table in soup.find_all("table", class_="wikitable"):
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if not cells:
                continue

            raw = clean_text(cells[0].get_text(separator=' '))

            if not any(raw.startswith(f) for f in FAMILIES):
                continue

            if '(' in raw:
                name_part, rest = raw.split('(', 1)
                rest = rest.rstrip(')')
            else:
                mt_pos = re.search(r'\bMT\d+', raw)
                if mt_pos:
                    name_part = raw[:mt_pos.start()]
                    rest = raw[mt_pos.start():]
                else:
                    name_part = raw
                    rest = ''

            soc_name = name_part.strip()

            renamed_match = re.search(r'(.+?)\s+renamed', rest)
            if renamed_match:
                alias_target = renamed_match.group(1).strip()
                aliases[soc_name] = alias_target
                continue

            mt_numbers = extract_mt_numbers(rest)
            if not mt_numbers:
                mt_numbers = extract_mt_numbers(soc_name)
                soc_name = re.sub(r'\s+MT\d+.*', '', soc_name).strip()

            if not mt_numbers:
                mt_numbers = ["Unknown"]

            # Handle cases where / in a cell
            names = [soc_name]
            if ' / ' in soc_name:
                prefix_match = re.match(r'^(\w+\s+)', soc_name)
                prefix = prefix_match.group(1) if prefix_match else ''
                parts = soc_name.split(' / ')
                names = []
                for part in parts:
                    if ' ' not in part.strip():
                        names.append(prefix + part.strip())
                    else:
                        names.append(part.strip())

            for name in names:
                if name not in result:
                    result[name] = mt_numbers
                else:
                    for m in mt_numbers:
                        if m not in result[name]:
                            result[name].append(m)

    def resolve_alias(name, visited=None):
        if visited is None:
            visited = set()
        if name in visited:
            return ["Unknown"]
        visited.add(name)
        if name in aliases:
            return resolve_alias(aliases[name], visited)
        return result.get(name, ["Unknown"])
    for soc_name, alias_target in aliases.items():
        result[soc_name] = resolve_alias(alias_target)

    return dict(sorted(result.items()))


if __name__ == "__main__":
    print("Fetching...")
    html = fetch_wikipedia_page()
    data = parse_mediatek(html)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
