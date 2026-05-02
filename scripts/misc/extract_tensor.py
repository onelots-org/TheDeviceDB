import requests
from bs4 import BeautifulSoup
import json
import os
import re
import random

URL = "https://en.wikipedia.org/wiki/Google_Tensor"
OUTPUT = "../resources/tensor_socs.json"

with open("../resources/headers.json", "r") as f:
    headers_list = json.load(f)

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()


def clean_model(text):
    if re.search(r'[—–-]\s*(N/a|N/A|n/a)?', text) or text.lower() in ["n/a", "—", "–"]:
        return "Unknown"
    m = re.search(r'(G[SP]\d{3,4}[A-Z]?)', text)
    return m.group(1) if m else text


def fetch_tensor():
    r = requests.get(URL, headers=random.choice(headers_list))
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="wikitable")
    if not table:
        return {}
    rows = table.find_all("tr")
    headers = [clean_text(th.get_text()) for th in rows[0].find_all("th")]
    soc_names = []
    for h in headers:
        m = re.search(r'G(\d+)', h)
        if m:
            soc_names.append(f"Tensor G{m.group(1)}")
    codenames = {}
    model_numbers = {}
    for row in rows:
        th = row.find("th", scope="row")
        if not th:
            continue
        label = clean_text(th.get_text())
        cells = row.find_all("td")

        if label == "Codename":
            for i, td in enumerate(cells):
                if i < len(soc_names):
                    codenames[soc_names[i]] = clean_text(td.get_text()).split("[")[0].strip()

        elif label == "Model number":
            for i, td in enumerate(cells):
                if i < len(soc_names):
                    model_numbers[soc_names[i]] = clean_model(clean_text(td.get_text()))

    return {
        name: {
            "codename": codenames.get(name, "Unknown"),
            "model_number": model_numbers.get(name, "Unknown")
        }
        for name in soc_names
    }

def generate_tensors():
    data = fetch_tensor()
    existing = {}
    if os.path.exists(OUTPUT):
        with open(OUTPUT, "r") as f:
            content = f.read().strip()
            if content:
                existing = json.loads(content)
    existing.update(data)

    with open(OUTPUT, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"{len(data)} Tensor SoCs found.")


generate_tensors()