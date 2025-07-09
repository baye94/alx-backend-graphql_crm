import requests
import json
from datetime import datetime

def update_low_stock():
    endpoint = "http://localhost:8000/graphql/"

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

    log_path = "/tmp/lowstockupdates_log.txt"
    with open(log_path, "a") as log:
        log.write(f"\n[{datetime.now()}] Low stock update job:\n")
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                log.write("GraphQL errors:\n")
                log.write(json.dumps(data["errors"], indent=2) + "\n")
            else:
                result = data["data"]["updateLowStockProducts"]
                log.write(result["message"] + "\n")
                for p in result["updatedProducts"]:
                    log.write(f"- {p['name']} => stock: {p['stock']}\n")
        else:
            log.write(f"Request failed with status code: {response.status_code}\n")
