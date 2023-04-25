import requests
import json
from colorama import Fore, Style


def print_call(expected, name, res : requests.Response):
    status = res.status_code
    content = res.json()
    time = res.elapsed

    print(f"--------------------------------------------------")
    print(name)

    if(status == expected):
        print(f"{Fore.GREEN}[PASS] Status : {Fore.GREEN}{status} OK{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[FAILED] Status : Got {Fore.RED}{status} Expected {expected}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}Call completed in {time}{Style.RESET_ALL}")