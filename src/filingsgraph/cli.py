import argparse
from filingsgraph.core.config import get_settings

def main():
    p=argparse.ArgumentParser(prog='filingsgraph'); p.add_argument('command',choices=['config','health']); args=p.parse_args()
    if args.command=='config': print(get_settings().model_dump_json(indent=2))
    else: print('FilingsGraph CLI OK')
if __name__=='__main__': main()
