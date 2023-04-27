import argparse
import yaml
import call

parser = argparse.ArgumentParser(
                    prog = 'autocall',
                    description = 'Automatize network calls with yaml files',
                    )

parser.add_argument('-f', nargs='?', help='Target YAML file', dest="config_file")
parser.add_argument('--no-out', help='Turn off console output', action="store_const", dest="no_out")
parser.add_argument('--no-res', help='Disable response output for calls', action="store_const", dest="no_res")

args = parser.parse_args()
print(args)

config_file = args.config_file if args.config_file else None

no_out = args.no_out if args.no_out else None
no_res = args.no_res if args.no_res else None

print(no_out)

print_to_console = False if no_out != None else True
print_responses  = False if no_res else True

print(print_to_console)

with open(config_file, encoding='utf-8') as file:
    config = yaml.safe_load(file)

call_list : call.Call = call.create_calls(config)

for c in call_list:
    c.execute(print_to_console, print_responses)
