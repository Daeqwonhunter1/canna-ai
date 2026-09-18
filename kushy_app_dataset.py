import csv
import json

def parse_strain_csv(filepath):
    """Parse strain CSV, converting NULL -> None and numeric fields -> int/float."""

    numeric_fields = {
        "id", "status", "sort", "thc", "thca", "thcv", "cbd", "cbda",
        "cbdv", "cbn", "cbg", "cbgm", "cbgv", "cbc", "cbcv", "cbv",
        "cbe", "cbt", "cbl"
    }

    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {}
            for key, value in row.items():
                if value is None or value.strip() == "" or value.strip() == "NULL":
                    cleaned[key] = None
                elif key in numeric_fields:
                    try:
                        cleaned[key] = int(value)
                    except ValueError:
                        cleaned[key] = float(value)
                else:
                    cleaned[key] = value.strip()
            rows.append(cleaned)
    return rows


def write_json(rows, output_path):
    """Write parsed rows to a JSON file as a list of objects."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    strains = parse_strain_csv("/Users/dq/Desktop/canna-ai/dataset/strains-kushy-api.2017-11-14.csv")
    write_json(strains, "/Users/dq/Desktop/canna-ai/dataset/strains-kushy.json")
    print(f"Wrote {len(strains)} strains to strains.json")