import argparse
from lib import rebootEth, restartEth, startEth, shutdownEth, arduino

my_parser = argparse.ArgumentParser(description='command - "python3 eth.py" start eth')

my_parser.add_argument('-a',
                       '--arduino', type=str)

my_parser.add_argument('-res',
                       '--restart', action='store_true', help='command restart eth')
my_parser.add_argument('-reb',
                       '--reboot', action='store_true', help='command reboot eth')
my_parser.add_argument('-s',
                       '--start', action='store_true', help='command start eth')
my_parser.add_argument('-sh',
                       '--shutdown', action='store_true', help='command shutdown eth')

if __name__ == '__main__':
    args = my_parser.parse_args()
    if args.arduino:
        arduino(args.arduino)
    elif args.restart:
        restartEth()
    elif args.reboot:
        rebootEth()
    elif args.shutdown:
        shutdownEth()
    elif args.start:
        startEth()
    else:
        startEth()

