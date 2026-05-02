import requests
from bs4 import BeautifulSoup
import re
import json
import os
import random


def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\[\s*\w+\s*\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def derive_platform(soc_name):
    digits = re.findall(r'\d+', soc_name)
    return f"Exynos{digits[-1]}" if digits else re.sub(r'\s+', '', soc_name)


def parse_exynos(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    for table in soup.find_all("table", class_="wikitable"):
        header_text = ' '.join(clean_text(h.get_text()) for h in table.find_all('th'))
        if 'Model number' not in header_text:
            continue
        for row in table.find_all("tr"):
            cells = row.find_all('td')
            if not cells:
                continue
            first = clean_text(cells[0].get_text())
            if not first.startswith("Exynos"):
                continue
            name_match = re.match(r'^(Exynos[\w\s\+]+?)(?:\s*\(([^)]+)\))?$', first)
            if not name_match:
                continue
            soc_name = name_match.group(1).strip()
            model_number = name_match.group(2)
            model_number = re.sub(r'\[\w+\]', '', model_number).strip() if model_number else "Unknown"
            entry = {
                "model_number": model_number,
                "platform": derive_platform(soc_name),
            }
            result[soc_name] = entry
    return dict(sorted(result.items()))


def load_existing(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return {}


def merge(existing, new):
    for soc_name, new_entry in new.items():
        if soc_name not in existing:
            existing[soc_name] = new_entry
        else:
            for key, value in new_entry.items():
                if key not in existing[soc_name] or existing[soc_name][key] == "Unknown":
                    existing[soc_name][key] = value
    return dict(sorted(existing.items()))


with open("../resources/headers.json", "r") as f:
    headers_list = json.load(f)


def jsonize_exynos():
    path = "../resources/exynos_socs.json"
    url = "https://en.wikipedia.org/wiki/Exynos"
    headers = random.choice(headers_list)
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    existing = load_existing(path)
    new = parse_exynos(r.text)
    merged = merge(existing, new)
    with open(path, "w") as f:
        json.dump(merged, f, indent=2)
    print(f"{len(merged)} SoCs written in {path}.")


jsonize_exynos()
