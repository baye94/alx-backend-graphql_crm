# crm/cron.py
import requests
import json
import datetime
import os

# Assuming your GraphQL endpoint is at /graphql/
# Adjust this URL if your endpoint is different
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/" # Use your Django project's URL

def update_low_stock():
    """
    Executes a GraphQL mutation to update low-stock products
    and logs the results.
    """
    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            message
        }
    }
    """
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': mutation}, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        log_file_path = "/tmp/low_stock_updates_log.txt"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file_path, "a") as log_file:
            log_file.write(f"[{timestamp}] Low Stock Update Job Started:\n")

            if 'errors' in data:
                log_file.write(f"  GraphQL Errors: {json.dumps(data['errors'], indent=2)}\n")
                print(f"GraphQL Errors during low stock update: {data['errors']}")
            elif 'data' in data and data['data']['updateLowStockProducts']:
                result = data['data']['updateLowStockProducts']
                log_file.write(f"  Message: {result['message']}\n")
                print(f"Low Stock Update Message: {result['message']}")

                updated_products = result.get('updatedProducts', [])
                if updated_products:
                    log_file.write("  Updated Products:\n")
                    for product in updated_products:
                        log_entry = f"    - Name: {product['name']}, New Stock: {product['stock']}\n"
                        log_file.write(log_entry)
                        print(f"  Updated: {product['name']}, New Stock: {product['stock']}")
                else:
                    log_file.write("  No products were updated.\n")
            else:
                log_file.write("  Unexpected GraphQL response format.\n")
                print("Unexpected GraphQL response format.")
            log_file.write("-" * 50 + "\n")

    except requests.exceptions.ConnectionError as e:
        error_message = f"[{timestamp}] Connection Error: Could not connect to GraphQL endpoint at {GRAPHQL_ENDPOINT}. Is your Django server running? Error: {e}\n"
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(error_message)
        print(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"[{timestamp}] Request Error: An error occurred during the HTTP request to {GRAPHQL_ENDPOINT}. Error: {e}\n"
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"[{timestamp}] An unexpected error occurred: {e}\n"
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(error_message)
        print(error_message)