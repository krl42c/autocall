import argparse
import yaml
import call

parser = argparse.ArgumentParser(
                    prog = 'autocall',
                    description = 'Automatize network calls with yaml files',
                    )

parser.add_argument('-f', nargs='?', help='Target YAML file', dest="config_file")

args = parser.parse_args()
print(args)

config_file = args.config_file if args.config_file else None

with open(config_file, encoding='utf-8') as file:
    config = yaml.safe_load(file)

call_list : call.Call = call.create_calls(config)

for c in call_list:
    c.run_tests()
