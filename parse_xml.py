import xml.etree.ElementTree as ET
import pandas as pd
import os

files = [
    ("XMLZIPFile/2008 - keepass.xml", "keepass"),
    ("XMLZIPFile/2005 - microcare.xml", "microcare"),
    ("XMLZIPFile/1999 - dii.xml", "dii"),
]

all_reqs = []
req_id = 1

for filepath, source in files:
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # Extract all text elements
    for elem in root.iter():
        if elem.text and len(elem.text.strip()) > 20:
            all_reqs.append({
                "req_id": f"REQ-{req_id:03d}",
                "req_text": elem.text.strip(),
                "source": source,
                "true_label": "",
                "notes": ""
            })
            req_id += 1

df = pd.DataFrame(all_reqs).drop_duplicates(subset="req_text")
df.to_csv("ground_truth.csv", index=False)
print(f"Total requirements extracted: {len(df)}")
print(df.head())