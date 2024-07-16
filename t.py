import time
import requests
import random
from datetime import datetime, timedelta, timezone

def read_data(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def get_authorization_header(data_line):
    return {"Authorization": data_line}

def tap_tap_task(auth_header, last_click_time, clicks):
    url = f"https://tap-tether.org/server/clicks?clicks={clicks}&lastClickTime={last_click_time}"
    response = requests.get(url, headers=auth_header)
    if response.status_code == 200:
        print(f"Tap tap successful with {clicks} clicks.")
    else:
        print(f"Tap tap failed with status code: {response.status_code}")

def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"Time remaining: {remaining_time}", end='\r')
        time.sleep(1)

def convert_to_wib(unix_timestamp):
    utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    wib_time = utc_time + timedelta(hours=7)
    return wib_time

def generate_clicks(total, parts):
    if parts <= 1:
        return [total]
    
    cuts = sorted(random.sample(range(1, total), parts - 1))
    clicks = [cuts[0]] + [cuts[i] - cuts[i-1] for i in range(1, len(cuts))] + [total - cuts[-1]]
    return clicks

def main():
    data_lines = read_data('data.txt')
    total_accounts = len(data_lines)
    
    for index, line in enumerate(data_lines):
        auth_header = get_authorization_header(line)
        last_click_time = int(time.time())  # Start with current time as UNIX timestamp
        
        print(f"Processing account {index + 1} of {total_accounts}")
        
        clicks = generate_clicks(1000, 10)  # Generate 10 random parts that sum up to 1000
        
        for click in clicks:  # 10 tap-tap tasks per account
            wib_time = convert_to_wib(last_click_time)
            print(f"Current lastClickTime (WIB): {wib_time}")
            tap_tap_task(auth_header, last_click_time, click)
            last_click_time += 1  # Update last_click_time, you can adjust as needed
            time.sleep(5)  # 5 seconds delay between tap-tap tasks

        print(f"Completed processing account {index + 1}")
    
    print("All accounts processed. Starting 1-hour countdown.")
    countdown_timer(3600)  # 1 hour countdown

if __name__ == "__main__":
    main()
