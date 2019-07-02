import project_tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-pt_fl', dest='pt_fl', type=str)
parser.add_argument('-place', dest='place', type=str)
args = parser.parse_args()

project_tools.run_smart(args.pt_fl, args.place)
