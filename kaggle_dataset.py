import csv
import json

def parse_cannytics_csv(filepath):
    """Parse Cannytics strain CSV into a list of dicts."""

    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {
                "strain": row["Strain"].strip(),
                "type": row["Type"].strip().lower() if row["Type"] else None,
                "rating": float(row["Rating"]) if row["Rating"].strip() else None,
                "effects": [e.strip() for e in row["Effects"].split(",")] if row["Effects"] else [],
                "flavor": [f.strip() for f in row["Flavor"].split(",")] if row["Flavor"] else [],
                "description": row["Description"].strip() if row["Description"] else None,
            }
            rows.append(cleaned)
    return rows


def write_json(rows, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    strains = parse_cannytics_csv("/Users/dq/Desktop/canna-ai/dataset/strains-kaggle-api.csv")
    write_json(strains, "/Users/dq/Desktop/canna-ai/dataset/strains-kaggle.json")
    print(f"Wrote {len(strains)} strains to strains-kaggle.json")