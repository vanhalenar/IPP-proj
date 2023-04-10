import re
import argparse
import xml.etree.ElementTree as ET
import sys
import interpret_classes as IC

#set up argument parser
parser = argparse.ArgumentParser(prog='interpret.py', description='Interprets XML representation of IPPcode23')
parser.add_argument('--input', help='Specify the input file')
parser.add_argument('--source', help='Specify the source file')

#process arguments
args = parser.parse_args()

if (args.input):
    inputfile = args.input
    sys.stdin = open(inputfile, 'r')
if (args.source):
    sourcefile = args.source

#what do if no source or input
if not(args.input or args.source):
    print("no source or input specified")
    sys.exit(1)
    #tree=ET.parse(STDIN) or something like that?
else:
    try:
        tree=ET.parse(sourcefile)
    except:
        sys.exit(31)

root=tree.getroot()

if root.tag != 'program':
    sys.exit(32)                                #should it be 32?
for inst in root:
    if inst.tag != 'instruction':
        sys.exit(32)                            #same issue, not sure, what the exit code should be
    attributes=list(inst.attrib.keys())
    if not('order' in attributes and 'opcode' in attributes):
        sys.exit(32)                            #same here
    arg_count = 0
    for arg in inst:
        if not(re.match(r"arg[123]", arg.tag)):
            sys.exit(32)                        #gotta look into this
        arg_count += 1
        arg_number = int(arg.tag[3:])
        if (arg_number != arg_count):
            sys.exit(32)

factory = IC.InstructionFactory()
program = IC.program

for inst in root:
    try:
        order = int(inst.attrib["order"])
    except:
        sys.exit(32)
    current = factory.create_instruction(inst.attrib["opcode"], order)
    for i in inst:
        if (i.attrib["type"] == "int"):
            try:
                int_text = int(i.text)
            except:
                sys.exit(32)
            current.add_argument("int", int_text)
        elif (i.attrib["type"] == "bool"):
            if (i.text == "true"):
                bool_text = True
            else:
                bool_text = False
            current.add_argument("bool", bool_text)
        else:
            current.add_argument(i.attrib["type"], i.text)
    
    if (inst.attrib["opcode"] == "LABEL"):
        program.add_label(current.args[0].get("arg_value"), current.order-1)
    program.add_instruction(current)


inst_count = len(program.instructions)


while (program.instruction_index < inst_count):
    program.instructions[program.instruction_index].execute()
    program.incr_instr_index()

#print(program.labels)