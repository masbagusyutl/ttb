import time
import requests
import random
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote, quote
import hashlib

def read_data(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def write_data(file_path, data_lines):
    with open(file_path, 'w') as file:
        file.write("\n".join(data_lines))

def get_authorization_header(data_line):
    return {"Authorization": data_line}

def extract_username(auth_header):
    decoded_str = unquote(auth_header)
    username_key = 'username":"'
    start_index = decoded_str.find(username_key) + len(username_key)
    end_index = decoded_str.find('"', start_index)
    return decoded_str[start_index:end_index]

def tap_tap_task(auth_header, last_click_time, clicks, username):
    url = f"https://tap-tether.org/server/clicks?clicks={clicks}&lastClickTime={last_click_time}"
    response = requests.get(url, headers=auth_header)
    if response.status_code == 200:
        print(f"Tap tap successful with {clicks} clicks for {username}.")
    else:
        print(f"Tap tap failed with status code: {response.status_code}")

def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"Time remaining: {remaining_time}", end='\r')
        time.sleep(1)
    print("\nCountdown finished. Restarting tasks...")

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

def update_auth_date_and_hash(data_line):
    parts = data_line.split('&')
    new_parts = []
    for part in parts:
        if part.startswith('auth_date='):
            new_auth_date = int(time.time())
            new_parts.append(f'auth_date={new_auth_date}')
        elif part.startswith('hash='):
            new_hash = hashlib.sha256(f"{new_auth_date}{random.random()}".encode()).hexdigest()
            new_parts.append(f'hash={new_hash}')
        else:
            new_parts.append(part)
    return '&'.join(new_parts)

def process_accounts():
    data_lines = read_data('data.txt')
    total_accounts = len(data_lines)
    
    for index, line in enumerate(data_lines):
        updated_line = update_auth_date_and_hash(line)
        data_lines[index] = updated_line
        
        auth_header = get_authorization_header(updated_line)
        username = extract_username(updated_line)
        last_click_time = int(time.time())  # Start with current time as UNIX timestamp
        
        print(f"Processing account {index + 1} of {total_accounts} ({username})")
        
        clicks = generate_clicks(1000, 10)  # Generate 10 random parts that sum up to 1000
        
        for click in clicks:  # 10 tap-tap tasks per account
            wib_time = convert_to_wib(last_click_time)
            print(f"Current lastClickTime (WIB): {wib_time}")
            tap_tap_task(auth_header, last_click_time, click, username)
            last_click_time += 1  # Update last_click_time, you can adjust as needed
            time.sleep(5)  # 5 seconds delay between tap-tap tasks

        print(f"Completed processing account {index + 1} ({username})")
    
    write_data('data.txt', data_lines)  # Write the updated data back to data.txt

def main():
    while True:
        process_accounts()
        random_countdown = random.randint(20, 300)  # Random countdown between 20 and 300 seconds (5 minutes)
        print(f"All accounts processed. Starting {random_countdown}-second countdown.")
        countdown_timer(random_countdown)  # Random countdown timer

if __name__ == "__main__":
    main()
