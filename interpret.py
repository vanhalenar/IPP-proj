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
    sys.exit(32)                                #should it be 32?
for inst in root:
    if inst.tag != 'instruction':
        sys.exit(32)                            #same issue, not sure, what the exit code should be
    attributes=list(inst.attrib.keys())
    if not('order' in attributes and 'opcode' in attributes):
        sys.exit(32)                            #same here
    for arg in inst:
        if not(re.match(r"arg[123]", arg.tag)):
            sys.exit(32)                        #gotta look into this

factory = IC.InstructionFactory()
program = IC.program

for inst in root:
    current = factory.create_instruction(inst.attrib["opcode"], int(inst.attrib["order"]))
    for i in inst:
        if (i.attrib["type"] == "int"):
            current.add_argument(i.attrib["type"], int(i.text))
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