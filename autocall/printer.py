import requests
import json
from colorama import Fore, Style


def print_call(expected, url, name, res : requests.Response):
    status = res.status_code
    time = res.elapsed

    print("--------------------------------------------------")
    print(f"{name} -- {url}\n")
    print(f"{Fore.YELLOW}Call completed in {time}{Style.RESET_ALL}\n")

    if(status == expected):
        print(f"{Fore.GREEN}[PASS] Status : {Fore.GREEN}{status} OK{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[FAILED] Status : Got {Fore.RED}{status} Expected {expected}{Style.RESET_ALL}")


def print_err(call_name, exception):
    print(f"{Fore.RED}[{call_name}: Error parsing YAML] {exception}{Style.RESET_ALL}")