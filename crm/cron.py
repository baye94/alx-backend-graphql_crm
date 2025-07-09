# crm/cron.py
import requests
import json
from datetime import datetime

def update_low_stock():
    endpoint = "http://localhost:8000/graphql/"  # Assure-toi que c'est l'URL correcte

    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                id
                name
                stock
            }
            message
        }
    }
    """

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, headers=headers, json={"query": mutation})

    log_file = "/tmp/low_stock_updates_log.txt"
    with open(log_file, "a") as log:
        log.write(f"\n[{datetime.now()}] Cron Job Execution:\n")
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                log.write("Errors:\n")
                log.write(json.dumps(data["errors"], indent=2))
            else:
                products = data["data"]["updateLowStockProducts"]["updatedProducts"]
                message = data["data"]["updateLowStockProducts"]["message"]
                log.write(message + "\n")
                for p in products:
                    log.write(f" - {p['name']}: stock = {p['stock']}\n")
        else:
            log.write(f"Request failed: HTTP {response.status_code}\n")
