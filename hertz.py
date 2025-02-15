import requests
import time
import argparse
import os

def fetch_routes():
    url = "https://hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def location_matches(location, location_list):
    return any(loc.lower() in location.lower() for loc in location_list)

def send_telegram_notification(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Telegram notification sent")
        else:
            print(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def find_matching_routes(routes, from_locations, to_locations, seen_routes, bot_token, chat_id):
    for route_data in routes:
        pickup = route_data["pickupLocationName"]
        dropoff = route_data["returnLocationName"]
        if location_matches(pickup, from_locations) and location_matches(dropoff, to_locations):
            for route in route_data["routes"]:
                route_id = route["id"]
                if route_id not in seen_routes:
                    seen_routes.add(route_id)
                    message = (f"New trip found!\n{pickup} → {dropoff}\n"
                               f"Car: {route['carModel']}\nAvailable from: {route['availableAt'].replace('T', ', kl ')}\n"
                               f"Return by: {route['latestReturn'].replace('T', ', kl ')}")
                    print(message)
                    send_telegram_notification(message, bot_token, chat_id)

def main():
    parser = argparse.ArgumentParser(description="Find transport routes from Hertz Freerider API.")
    parser.add_argument("--from-locations", type=str, nargs='+', required=True, help="List of possible pickup locations")
    parser.add_argument("--to", type=str, nargs='+', required=True, help="List of possible dropoff locations")
    args = parser.parse_args()

    from_locations = args.from_locations
    to_locations = args.to
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set. Please configure environment variables.")
        return

    seen_routes = set()

    while True:
        print(f"Searching for new trips from {', '.join(from_locations)} to {', '.join(to_locations)}...")
        routes = fetch_routes()
        find_matching_routes(routes, from_locations, to_locations, seen_routes, bot_token, chat_id)
        time.sleep(10)

if __name__ == "__main__":
    main()
