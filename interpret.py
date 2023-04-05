import re
import argparse
import xml.etree.ElementTree as ET
import sys

#set up argument parser
parser = argparse.ArgumentParser(prog='interpret.py', description='Interprets XML representation of IPPcode23')
parser.add_argument('--input', help='Specify the input file')
parser.add_argument('--source', help='Specify the source file')

#process arguments
args = parser.parse_args()

if (args.input):
    inputfile = args.input
if (args.source):
    sourcefile = args.source

#what do if no source or input
if not(args.input or args.source):
    print("no source or input specified")
    #tree=ET.parse(STDIN) or something like that?
else:
    tree=ET.parse(sourcefile)

root=tree.getroot()

if root.tag != 'program':
    sys.exit(32) #should it be 32?
for i in root:
    if i.tag != 'instruction':
        sys.exit(32) #same issue, not sure, what the exit code should be
    attributes=list(i.attrib.keys())
    if not('order' in attributes and 'opcode' in attributes):
        sys.exit(32) #same here 