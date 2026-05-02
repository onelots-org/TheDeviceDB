import cloudscraper
import json
import re
from bs4 import BeautifulSoup
import random

EXISTING_JSON_PATH = "../resources/qualcomm_socs.json"
OUTPUT_JSON_PATH = "../resources/qualcomm_socs.json"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_Qualcomm_Snapdragon_systems_on_chips"

with open("../resources/headers.json", "r") as f:
    headers_list = json.load(f)

def fetch_wikipedia_page(url):
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(random.choice(headers_list))
    response = scraper.get(url)
    response.raise_for_status()
    return response.text

def extract_model_to_name(html):
    soup = BeautifulSoup(html, "html.parser")
    model_to_name = {}

    for table in soup.find_all("table", {"class": "wikitable"}):
        rows = table.find_all("tr")
        if not rows:
            continue

        headers = [th.get_text(strip=True).lower() for th in rows[0].find_all(["th", "td"])]

        model_col = None
        name_col = None
        for i, h in enumerate(headers):
            if "model" in h and "number" in h:
                model_col = i
            if "product" in h and "name" in h:
                name_col = i
        if model_col is None or name_col is None:
            continue

        row_spans = {}
        for row_idx, row in enumerate(rows[1:], start=1):
            cells = row.find_all(["td", "th"])
            col_values = {}
            for col in range(max((model_col, name_col)) + 2):
                if col in row_spans and row_spans[col][0] > 0:
                    col_values[col] = row_spans[col][1]
                    row_spans[col] = (row_spans[col][0] - 1, row_spans[col][1])
            col = 0
            cell_idx = 0
            while cell_idx < len(cells) and col <= max(model_col, name_col) + 1:
                while col in col_values:
                    col += 1
                if cell_idx >= len(cells):
                    break
                cell = cells[cell_idx]
                text = re.sub(r'\[.*?\]', '', cell.get_text(separator=" ", strip=True)).strip()
                text = re.sub(r'[\u00a0\u200b\u202f\u2009]+', ' ', text).strip()
                span = int(cell.get("rowspan", 1))
                col_values[col] = text
                if span > 1:
                    row_spans[col] = (span - 1, text)
                col += 1
                cell_idx += 1
            model_text = col_values.get(model_col, "")
            name_text = col_values.get(name_col, "")

            if not model_text or not name_text:
                continue

            for model_line in model_text.split():
                if re.match(r'^(SM|MSM|QSD|APQ|MDM|SDM|QCS|CQ|SXR)\w+', model_line):
                    model_to_name[model_line] = name_text
    return model_to_name


def load_existing_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN] {path} not found, starting fresh.")
        return {}

def update_json(existing, model_to_name):
    added_name = 0

    def clean_wiki_name(name): # Not looking forward to ever do it again...
        name = re.sub(r'[\u00a0\u200b\u202f\u2009]+', ' ', name).strip()
        name = re.sub(r'\s*\(.*?(GHz|cores).*?\)', '', name, flags=re.IGNORECASE).strip()
        name = re.sub(r'\s+Oryon\s*$', '', name, flags=re.IGNORECASE).strip()
        name = re.sub(r'\s*\([^)]*\)', '', name).strip()
        name = re.sub(r'\s+', ' ', name).strip()
        return name or "Unknown"

    def is_valid_model(model): # I hate regex but thanks LLMs
        model = re.sub(r'[^A-Z0-9\-]', '', model.upper())
        return bool(re.match(
            r'^(MSM|APQ|SDM|SM)\d+([A-Z0-9]+)?(-[A-Z0-9]+(-[A-Z0-9]+)*)?$',
            model
        ))

    def strip_suffix(model):
        return re.sub(r'-[A-Z]{2}[A-Z0-9]*$', '', model)

    for model, entry in list(existing.items()):
        existing_name = entry.get("name")
        wiki_name = model_to_name.get(model)
        if wiki_name is None:
            base_model = strip_suffix(model)
            if base_model != model:
                wiki_name = model_to_name.get(base_model)
        if wiki_name is None:
            for wiki_model, wiki_candidate in model_to_name.items():
                wiki_base = strip_suffix(wiki_model)
                if wiki_base == model:
                    wiki_name = wiki_candidate
                    break
        if wiki_name:
            wiki_name = clean_wiki_name(wiki_name)
        if existing_name and existing_name != "Unknown":
            final_name = existing_name
        elif wiki_name:
            final_name = wiki_name
        else:
            final_name = "Unknown"
            if not existing_name:
                print(f"[INFO] No Wikipedia match for: {model}")

        new_entry = {"name": final_name}
        new_entry["HLOS"] = entry.get("HLOS", "Unknown")
        new_entry["Die"] = entry.get("Die", ["Unknown"])
        for k, v in entry.items():
            if k not in ("name", "HLOS", "Die"):
                new_entry[k] = v
        existing[model] = new_entry
        if final_name != existing_name:
            added_name += 1

    for wiki_model, wiki_name in model_to_name.items():
        wiki_model_clean = re.sub(r'[^A-Za-z0-9\-]', '', wiki_model)

        if not is_valid_model(wiki_model_clean):
            print(f"[SKIP] Invalid model format: {wiki_model}")
            continue
        if re.search(r'-$', wiki_model_clean):
            print(f"[SKIP] Invalid model format (trailing dash): {wiki_model}")
            continue

        if wiki_model_clean not in existing:
            name_clean = clean_wiki_name(wiki_name)
            existing[wiki_model_clean] = {
                "name": name_clean,
                "HLOS": "Unknown",
                "Die": ["Unknown"]
            }
            print(f"[NEW] Added from Wikipedia: {wiki_model_clean} -> {name_clean}")
            added_name += 1

    existing = dict(sorted(existing.items()))
    print(f"\n[DONE] {added_name} entries updated/added.")
    return existing

def extract_qcom():
    print("[*] Fetching Wikipedia page...")
    html = fetch_wikipedia_page(WIKIPEDIA_URL)
    print("[*] Extracting model -> product name mapping...")
    model_to_name = extract_model_to_name(html)
    print(f"[*] Found {len(model_to_name)} model entries on Wikipedia.")
    print("[*] Loading existing JSON...")
    existing = load_existing_json(EXISTING_JSON_PATH)
    print("[*] Merging data...")
    updated = update_json(existing, model_to_name)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"[*] Saved to {OUTPUT_JSON_PATH}")


extract_qcom()
