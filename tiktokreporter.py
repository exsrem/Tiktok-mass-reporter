import tls_client
import requests
from datetime import datetime
import os, random, re, time, concurrent.futures, fade, urllib
import json
import pyfiglet
from termcolor import colored

def print_exsrem_banner():
    ascii_art = pyfiglet.figlet_format("EXSREM", font="slant")
    print(colored(ascii_art, "yellow"))

# Banner
banner = fade.fire("""
  _____ _ _    _____     _
 |_   _(_) | _|_   _|__ | | __
   | | | | |/ / | |/ _ \'| |/ /
   | | | |   <  | | (_) |   <
   |_| |_|_|'_\' |_|'___/|_|'_\'
                 MASS REPORT TOOL
    Made by EXSREM & Lunanoir for Cyber Zone Hack Team( https://t.me/+AK_N-NrTng5kNmRk )   Github: https://github.com/exsrem
 """)


# Proxy list
proxy_list = []

# Report types
report_types = {
    1: (90013, "Violence"),
    2: (90014, "Sexual Abuse"),
    3: (90016, "Animal Abuse"),
    4: (90017, "Criminal Activities"),
    5: (9020, "Hate"),
    6: (9007, "Bullying"),
    7: (90061, "Suicide Or Self-Harm"),
    8: (90064, "Dangerous Content"),
    9: (90084, "Sexual Content"),
    10: (90085, "Porn"),
    11: (90037, "Drugs"),
    12: (90038, "Firearms Or Weapons"),
    13: (9018, "Sharing Personal Info"),
    14: (90015, "Human Exploitation"),
    15: (91015, "Under Age")
}

# Counter class
class Counter:
    success = 0
    failed = 0

# Utility functions
class Basics:
    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_timestamp():
        return f"[{datetime.now().strftime('%H:%M:%S')}]"

import json

def ask_proxy():
    global proxy_list
    proxy_list = []
    while True:
        try:
            choices = input(colored(f"{Basics.get_timestamp()} Select proxy options (e.g.[space] 1 2 for multiple):\n"
                            "1. Default (Proxyscrape)\n"
                            "2. GitHub Free Proxy List\n"
                            "3. Custom file (Text or JSON)\n","blue")).strip()
            choices = [int(choice.strip()) for choice in choices.split(" ") if choice.strip().isdigit()]

            if not choices:
                print(colored(f"{Basics.get_timestamp()} No valid choices entered. Try again.","red"))
                continue

            for choice in choices:
                if choice == 1:
                    # Default proxy source (Proxyscrape)
                    free_api = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies"
                    response = requests.get(free_api)
                    if response.status_code == 200:
                        proxies = response.text.strip().split("\n")
                        proxy_list.extend(proxies)
                        print(colored(f"{Basics.get_timestamp()} Loaded {len(proxies)} proxies from Proxyscrape.","magenta"))
                    else:
                        print(colored(f"{Basics.get_timestamp()} Failed to fetch proxies from Proxyscrape.","green"))
                elif choice == 2:
                    # GitHub proxy source
                    github_url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/all/data.json"
                    response = requests.get(github_url)
                    if response.status_code == 200:
                        data = json.loads(response.text)
                        proxies = [entry["proxy"] for entry in data if "proxy" in entry]
                        proxy_list.extend(proxies)
                        print(colored(f"{Basics.get_timestamp()} Loaded {len(proxies)} proxies from GitHub Free Proxy List.","yellow"))
                    else:
                        print(f"{Basics.get_timestamp()} Failed to fetch proxies from GitHub.")
                elif choice == 3:
                    # Load proxies from custom file
                    file_path = input(colored(f"{Basics.get_timestamp()} Enter the proxy file path: ","blue")).strip()
                    if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                        if file_path.endswith(".json"):
                            # JSON file format
                            with open(file_path, "r") as f:
                                data = json.load(f)
                                proxies = [entry["proxy"] for entry in data if "proxy" in entry]
                                proxy_list.extend(proxies)
                            print(colored(f"{Basics.get_timestamp()} Loaded {len(proxies)} proxies from the JSON file.","red"))
                        else:
                            # Text file format
                            with open(file_path, "r") as f:
                                proxies = [line.strip() for line in f if line.strip()]
                                proxy_list.extend(proxies)
                            print(colored(f"{Basics.get_timestamp()} Loaded {len(proxies)} proxies from the text file.","blue"))
                    else:
                        print(colored(f"{Basics.get_timestamp()} Invalid file path. Skipping this option.","green"))
                else:
                    print(colored(f"{Basics.get_timestamp()} Invalid choice: {choice}. Skipping.","yellow"))

            proxy_list = [proxy if proxy.startswith("http://") or proxy.startswith("https://")
                          else f"http://{proxy}" for proxy in proxy_list]

            if proxy_list:
                print(colored(f"{Basics.get_timestamp()} Total proxies loaded: {len(proxy_list)}","magenta"))
                break
            else:
                print(colored(f"{Basics.get_timestamp()} No proxies were loaded. Try again.","magenta"))
        except ValueError:
            print(colored(f"{Basics.get_timestamp()} Invalid input. Enter numbers separated by commas.","blue"))
        except json.JSONDecodeError:
            print(colored(f"{Basics.get_timestamp()} Failed to parse JSON file. Ensure it is in valid JSON format.","green"))


def report_process(url, report_code):
    session = tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True)
    try:
        proxy = random.choice(proxy_list).strip()
        session.proxies = {"http": proxy}
    except IndexError:
        print(colored(f"{Basics.get_timestamp()} No proxies available. Skipping proxy setup.","magenta"))

    try:
        reason_format = re.search(r"reason=(\d+)", url)
        if reason_format:
            report_url = url.replace(f"reason={reason_format.group(1)}", f"reason={report_code}")
        else:
            report_url = url

        response = session.get(report_url)
        if "Thanks for your feedback" in response.text or response.status_code == 200:
            Counter.success += 1
        else:
            Counter.failed += 1
    except Exception as e:
        Counter.failed += 1
        print(f"{Basics.get_timestamp()} Error: {e}")

    total_attempts = Counter.success + Counter.failed

    if total_attempts > 0:
        success_rate = (Counter.success /total_attempts) * 100
        failure_rate = (Counter.failed / total_attempts) * 100
        Basics.clear_console()
        print(f"{Basics.get_timestamp()} {print_exsrem_banner()}")
        print(colored(f"{Basics.get_timestamp()} Total request percent: {total_attempts/len(proxy_list)*100}","green"))
        print(colored(f"{Basics.get_timestamp()} Success: {Counter.success}/{Counter.success + Counter.failed} ({success_rate:.2f}%)","green"))
        print(colored(f"{Basics.get_timestamp()} Failed: {Counter.failed}/{Counter.success + Counter.failed} ({failure_rate:.2f}%)","green"))

# Main function
if __name__ == "__main__":
    
    Basics.clear_console()
    print(banner)
    print_exsrem_banner()

    # Proxy selection
    ask_proxy()

    print_exsrem_banner()

    # Thread count input
    while True:
        try:
            thread_count = int(input(colored(f"{Basics.get_timestamp()} Enter the number of threads: ","magenta")))
            if thread_count > 0:
                break
            else:
                print(colored(f"{Basics.get_timestamp()} Threads must be greater than 0.","green"))
        except ValueError:
            print(f"{Basics.get_timestamp()} Invalid input. Please enter a number.")

    # Clear console
    Basics.clear_console()
    print_exsrem_banner()
    # URL input
    while True:
        url = input(colored(f"{Basics.get_timestamp()} Enter the report link: ","blue")).strip()
        if url.startswith("http://") or url.startswith("https://"):
            break
        else:
            print(colored(f"{Basics.get_timestamp()} Invalid URL. URL must start with 'http://' or 'https://'. Try again.","red"))

    # Select report type
    Basics.clear_console()
    print_exsrem_banner()
    for key, (_, name) in report_types.items():
        print(f"{key}. {name}")
    while True:
        try:
            report_type = int(input(colored(f"{Basics.get_timestamp()} Enter the report type number: ","magenta")))
            if report_type in report_types:
                report_code = report_types[report_type][0]
                break
            else:
                print(colored(f"{Basics.get_timestamp()} Invalid report type. Try again.","magenta"))
        except ValueError:
            print(f"{Basics.get_timestamp()} Invalid input. Enter a number.")

    # Start reporting
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(report_process, url, report_code) for _ in range(len(proxy_list))]
        concurrent.futures.wait(futures)

    print(colored(f"{Basics.get_timestamp()} Reporting completed. \nTotal Requests: {Counter.success + Counter.failed}","green"))
    print(colored(f"{Basics.get_timestamp()} Success: {Counter.success}","green"))
    print(colored(f"{Basics.get_timestamp()} Failed: {Counter.failed}","green"))
