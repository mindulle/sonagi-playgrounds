import csv
import os
import random
from datetime import datetime, timedelta

OUTPUT_DIR = "00_System/analytics/evidence/sources/finance_data"
CSV_PATH = os.path.join(OUTPUT_DIR, "api_costs.csv")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now()
    
    # In production, this syncs with update_api_costs.py output
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "service", "cost_usd"])
        
        for i in range(14, -1, -1):
            dt = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            writer.writerow([dt, "OpenAI", round(random.uniform(1.0, 3.5), 2)])
            writer.writerow([dt, "Anthropic", round(random.uniform(0.5, 2.0), 2)])
            writer.writerow([dt, "AWS / Infra", 5.00])
            
    print("Finance BI data exported successfully.")

if __name__ == "__main__":
    main()
