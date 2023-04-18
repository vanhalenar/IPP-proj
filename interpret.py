import sys
import re
import argparse
import xml.etree.ElementTree as ET
import sys

# Base class from which all instructions inherit
# This class is never instanced (pseudo-abstract class)
# Instance contains opcode and a list of arguments
# Each argument is a dictionary: {arg_type = "", arg_value = ""}
class Instruction:
    inst_counter = 0
    arg_num = 0
    order_numbers = []
    def __init__(self, opcode, order) -> None:
        self.opcode = opcode
        self.args = []
        Instruction.inst_counter += 1
        self.order = order
        if order in Instruction.order_numbers:
            sys.exit(32)
        Instruction.order_numbers.append(order)
        if order < 1:
            sys.exit(32)
        
    # Creates argument dict and adds to list
    def add_argument(self, typ, value, index):
        self.args.insert(index, dict(arg_type = typ, arg_value = value))
    
    # Each inherited class overrides this method
    def execute():
        print("not implemented!")
    
    # Called before execution
    # Checks, whether actual argument count corresponds with expected argument count
    def check_arg_quantity(self):
        if self.__class__.arg_num != len(self.args):
            sys.exit(32)
    
    # If argument is variable, returns variable from saved variables
    # If argument is constant, returns argument
    def retrieve_argument(self, arg: dict):
        if (arg["arg_type"] == "var"):
            return program.get_variable(arg["arg_value"])
        else:
            return arg

# Program class
# Singleton
class Program():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Program, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.instructions = []      # List of instructions
        self.frames_stack = []      # List of frames, used as a stack
        self.global_frame = dict()  # Global frame
        self.temporary_frame = None # Temporary frame
        self.local_frame = None     # Local Frame
        self.instruction_index = 0  # Instruction index, used as iterator in instructions list
        self.labels = dict()        # Labels, {label_name = number}
        self.call_stack = []        # Call stack, used with CALL/RETURN instructions
        self.data_stack = []        # Data stack, used with PUSHS/POPS

    def add_instruction(self, instr):
        self.instructions.append(instr)
        pass
    
    # Creates new temporary frame
    def create_frame(self):
        self.temporary_frame = dict()
    
    # Pushes temporary frame onto stack, sets local frame
    def push_frame(self):
        if self.temporary_frame is not None:
            self.frames_stack.append(self.temporary_frame)
            self.local_frame = self.frames_stack[-1]
            self.temporary_frame = None
        else:
            sys.exit(55)
    
    # Pops frame from stack, sets local frame
    def pop_frame(self):
        if self.local_frame is not None:
            self.temporary_frame = self.frames_stack.pop()
            if self.frames_stack:
                self.local_frame = self.frames_stack[-1]
            else:
                self.local_frame = None
        else:
            sys.exit(55)
    
    # Returns variable dict from correct frame
    def get_variable(self, var: str):
        if (re.match(r"^GF@", var)):
            if (var[3:] in program.global_frame.keys()):
                return program.global_frame[var[3:]]
            else:
                sys.exit(54)
        elif (re.match(r"^LF@", var)):
            if (program.local_frame is not None):
                if (var[3:] in program.local_frame.keys()):
                    return program.local_frame[var[3:]]
                else:
                    sys.exit(54)
            else:
                sys.exit(55)
        elif (re.match(r"^TF@", var)):
            if (program.temporary_frame is not None):
                if (var[3:] in program.temporary_frame.keys()):
                    return program.temporary_frame[var[3:]]
                else:
                    sys.exit(54)
            else:
                sys.exit(55)
        else:
            sys.exit(31)
    
    # Saves variable to correct frame
    # var: variable name
    # symb: variable type and value pair
    def save_to_variable(self, var: str, symb: dict):
        if (re.match(r"^GF@", var)):
            if (var[3:] in program.global_frame.keys()):
                program.global_frame[var[3:]] = symb
            else:
                sys.exit(54)
        elif (re.match(r"^LF@", var)):
            if (var[3:] in program.local_frame.keys()):
                program.local_frame[var[3:]] = symb
            else:
                sys.exit(54)
        elif (re.match(r"^TF@", var)):
            if (var[3:] in program.temporary_frame.keys()):
                program.temporary_frame[var[3:]] = symb
            else:
                sys.exit(54)
        else:
            print("bad, very bad") #change
            sys.exit() #figure this out
    
    # Adds label to labels list
    def add_label(self, label_name: str, label_num: int):
        if (label_name not in self.labels.keys()):
            self.labels[label_name] = label_num
        elif (self.labels[label_name] == label_num):
            pass
        else:
            sys.exit(52)
    
    def get_current_line(self):
        return self.instruction_index

    def jump_to_index(self, index):
        self.instruction_index = index
    
    def incr_instr_index(self):
        self.instruction_index += 1
    
    def call_stack_push(self, value):
        self.call_stack.append(value)
    
    def call_stack_pop(self):
        if (self.call_stack):
            return self.call_stack.pop()
        else:
            sys.exit(56)
    
    def data_stack_push(self, symb):
        self.data_stack.append(symb)
    
    def data_stack_pop(self):
        if (self.data_stack):
            return self.data_stack.pop()
        else:
            sys.exit(56)
    
    def get_label_names(self):
        return self.labels.keys()

# Factory class, creates instances of instruction subclasses based on opcode
class InstructionFactory():
    def create_instruction(self, opcode: str, order: int):
        if opcode == "WRITE":
            return WRITE(opcode, order)
        elif opcode == "CREATEFRAME":
            return CREATEFRAME(opcode, order)
        elif opcode == "PUSHFRAME":
            return PUSHFRAME(opcode, order)
        elif opcode == "JUMPIFNEQ":
            return JUMPIFNEQ(opcode, order)
        elif opcode == "JUMPIFEQ":
            return JUMPIFEQ(opcode, order)
        elif opcode == "POPFRAME":
            return POPFRAME(opcode, order)
        elif opcode == "INT2CHAR":
            return INT2CHAR(opcode, order)
        elif opcode == "STRI2INT":
            return STRI2INT(opcode, order)
        elif opcode == "GETCHAR":
            return GETCHAR(opcode, order)
        elif opcode == "SETCHAR":
            return SETCHAR(opcode, order)
        elif opcode == "RETURN":
            return RETURN(opcode, order)
        elif opcode == "DEFVAR":
            return DEFVAR(opcode, order)
        elif opcode == "CONCAT":
            return CONCAT(opcode, order)
        elif opcode == "STRLEN":
            return STRLEN(opcode, order)
        elif opcode == "DPRINT":
            return DPRINT(opcode, order)
        elif opcode == "LABEL":
            return LABEL(opcode, order)
        elif opcode == "BREAK":
            return BREAK(opcode, order)
        elif opcode == "PUSHS":
            return PUSHS(opcode, order)
        elif opcode == "POPS":
            return POPS(opcode, order)
        elif opcode == "TYPE":
            return TYPE(opcode, order)
        elif opcode == "JUMP":
            return JUMP(opcode, order)
        elif opcode == "MOVE":
            return MOVE(opcode, order)
        elif opcode == "READ":
            return READ(opcode, order)
        elif opcode == "IDIV":
            return IDIV(opcode, order)
        elif opcode == "CALL":
            return CALL(opcode, order)
        elif opcode == "EXIT":
            return EXIT(opcode, order)
        elif opcode == "AND":
            return AND(opcode, order)
        elif opcode == "ADD":
            return ADD(opcode, order)
        elif opcode == "SUB":
            return SUB(opcode, order)
        elif opcode == "MUL":
            return MUL(opcode, order)
        elif opcode == "NOT":
            return NOT(opcode, order)
        elif opcode == "EQ":
            return EQ(opcode, order)
        elif opcode == "LT":
            return LT(opcode, order)
        elif opcode == "GT":
            return GT(opcode, order)
        elif opcode == "OR":
            return OR(opcode, order)
        else:
            sys.exit(32)
        
# WRITE <symb>
class WRITE(Instruction):
    arg_num = 1
    def execute(self):
        arg = self.args[0]

        if (arg["arg_type"] == "var"):
            variable = program.get_variable(arg["arg_value"])
        else:    
            variable = arg
        
        if (variable["arg_type"] == "nil"):
            print("", end='')
            return

        string = variable["arg_value"]

        if (variable["arg_type"] == "bool"):
            print(str(string).lower(), end='')
            return

        if (variable["arg_type"] == "string"):
            pattern = r'\\([0-9]{3})'
            escape_seqs = re.findall(pattern, string)

            for escape_seq in escape_seqs:
                char_code = int(escape_seq)
                ascii_char = chr(char_code)
                string = string.replace('\\' + escape_seq, ascii_char)

        print(string, end='')

# CREATEFRAME
class CREATEFRAME(Instruction):
    arg_num = 0

    def execute(self):
        program.create_frame()

# PUSHFRAME
class PUSHFRAME(Instruction):
    arg_num = 0

    def execute(self):
        program.push_frame()

# POPFRAME
class POPFRAME(Instruction):
    arg_num = 0

    def execute(self):
        program.pop_frame()

# DEFVAR <var>
class DEFVAR(Instruction):
    arg_num = 1

    def execute(self):
        var_name_frame = self.args[0].get("arg_value")
        var_name = var_name_frame[3:]

        if (re.match(r"^GF@", var_name_frame)):
            if var_name not in program.global_frame.keys():
                program.global_frame[var_name] = dict(arg_type = None, arg_value = None)
            else:
                sys.exit(52)

        elif (re.match(r"^LF@", var_name_frame)):
            if (program.local_frame is not None):
                if var_name not in program.local_frame.keys():
                    program.local_frame[var_name] = dict(arg_type = "", arg_value = "")
                else:
                    sys.exit(52)
            else:
                sys.exit(55)

        elif (re.match(r"^TF@", var_name_frame)):
            if (program.temporary_frame is not None):
                if var_name not in program.temporary_frame.keys():
                    program.temporary_frame[var_name] = dict(arg_type = "", arg_value = "")
                else:
                    sys.exit(52)
            else:
                sys.exit(55)
        else:
            sys.exit(57)

# MOVE <var> <symb>
class MOVE(Instruction):
    arg_num = 2

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb = self.retrieve_argument(self.args[1])

        program.save_to_variable(var_name, symb)

# ADD <var> <symb> <symb>
class ADD(Instruction):
    arg_num = 3

    def execute(self):
        
        operand1 = self.retrieve_argument(self.args[1])
        operand2 = self.retrieve_argument(self.args[2])
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 + value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

# SUB <var> <symb> <symb>
class SUB(Instruction):
    arg_num = 3

    def execute(self):

        operand1 = self.retrieve_argument(self.args[1])
        operand2 = self.retrieve_argument(self.args[2])
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 - value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

# MUL <var> <symb> <symb>
class MUL(Instruction):
    arg_num = 3

    def execute(self):
        operand1 = self.retrieve_argument(self.args[1])
        operand2 = self.retrieve_argument(self.args[2])
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 * value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

# IDIV <var> <symb> <symb>
class IDIV(Instruction):
    arg_num = 3

    def execute(self):
        operand1 = self.retrieve_argument(self.args[1])
        operand2 = self.retrieve_argument(self.args[2])
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        if (value2 == 0):
            sys.exit(57)

        value = value1 // value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

# READ <var> <type>
class READ(Instruction):
    arg_num = 2

    def execute(self):
        try:
            user_input = inputfile.readline().strip()
        except:
            symb = dict(arg_type = "nil", arg_value = "nil")
            program.save_to_variable(self.args[0].get("arg_value"), symb)
            return

        if not user_input:
            symb = dict(arg_type = "nil", arg_value = "nil")
            program.save_to_variable(self.args[0].get("arg_value"), symb)
            return

        if (self.args[1]["arg_type"] != "type"):
            sys.exit(32)

        if (self.args[1].get("arg_value") == "int"):
            try:
                user_input = int(user_input)
                symb = dict(arg_type = self.args[1].get("arg_value"), arg_value = user_input)
            except:
                symb = dict(arg_type = "nil", arg_value = "nil")
        elif (self.args[1].get("arg_value") == "bool"):
            if (user_input == "true"):
                symb = dict(arg_type = "bool", arg_value = "true")
            else:
                symb = dict(arg_type = "bool", arg_value = "false")
        elif (self.args[1].get("arg_value") == "string"):
            symb = dict(arg_type = "string", arg_value = user_input)
        else:
            sys.exit(32)
        
        program.save_to_variable(self.args[0].get("arg_value"), symb)

# JUMP <label>
class JUMP(Instruction):
    arg_num = 1

    def execute(self):
        label_name = self.args[0].get("arg_value")

        if (label_name in program.get_label_names()):
            program.jump_to_index(program.labels[label_name])
        else:
            sys.exit(52)

# LABEL <label>
class LABEL(Instruction):
    arg_num = 1

    def execute(self):
        pass

# CALL <label>
class CALL(Instruction):
    arg_num = 1

    def execute(self):
        label_name = self.args[0].get("arg_value")
        program.call_stack_push(self.order - 1) #i can explain
        if (label_name in program.get_label_names()):
            program.jump_to_index(program.labels[label_name])
        else:
            sys.exit(52)

# RETURN 
class RETURN(Instruction):
    arg_num = 0

    def execute(self):
        if (program.call_stack):
            program.jump_to_index(program.call_stack_pop())
        else:
            sys.exit(56)
# EQ <var> <symb> <symb>
class EQ(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])

        if (symb1["arg_type"] != "nil" and symb2["arg_type"] != "nil"):
            if (symb1["arg_type"] != symb2["arg_type"]):
                sys.exit(53)
        
        if (symb1["arg_value"] == symb2["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(var_name, symb)

# GT <var> <symb> <symb>
class GT(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])

        if (symb1["arg_type"] != symb2["arg_type"]):
            sys.exit(53)
        
        if (symb1["arg_type"] == "nil" or symb2["arg_type"] == "nil"):
            sys.exit(53)
        
        if (symb1["arg_value"] > symb2["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(var_name, symb)

# LT <var> <symb> <symb>
class LT(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])

        if (symb1["arg_type"] != symb2["arg_type"]):
            sys.exit(53)
        
        if (symb1["arg_type"] == "nil" or symb2["arg_type"] == "nil"):
            sys.exit(53)
        
        if (symb1["arg_value"] < symb2["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(var_name, symb)

# AND <var> <symb> <symb>
class AND(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])
        
        if (symb1["arg_type"] != "bool" or symb2["arg_type"] != "bool"):
            sys.exit(53)

        result = symb1["arg_value"] and symb2["arg_value"]

        symb = dict(arg_type = "bool", arg_value = result)

        program.save_to_variable(var_name, symb)

# OR <var> <symb> <symb>
class OR(Instruction):
    arg_num = 3

    def execute(self):

        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])
        
        if (symb1["arg_type"] != "bool" or symb2["arg_type"] != "bool"):
            sys.exit(53)

        result = symb1["arg_value"] or symb2["arg_value"]

        symb = dict(arg_type = "bool", arg_value = result)

        program.save_to_variable(var_name, symb)

# NOT <var> <symb> 
class NOT(Instruction):
    arg_num = 2

    def execute(self):
        
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])

        if (symb1["arg_type"] != "bool"):
            sys.exit(53)

        symb = dict(arg_type = "bool", arg_value = not symb1["arg_value"])

        program.save_to_variable(var_name, symb)

# INT2CHAR <var> <symb>
class INT2CHAR(Instruction):
    arg_num = 2

    def execute(self):
        
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        
        if (symb1["arg_type"] != "int"):
            sys.exit(53)

        try:
            char_value = chr(symb1["arg_value"])
        except:
            sys.exit(58)

        symb = dict(arg_type = "string", arg_value = char_value)
        

        program.save_to_variable(var_name, symb)

# STRI2INT <var> <symb> <symb>
class STRI2INT(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])
        
        index = symb2["arg_value"]
        
        if (symb1["arg_type"] != "string"):
            sys.exit(53)
        
        if (symb2["arg_type"] != "int"):
            sys.exit(53)
        
        if (index >= len(symb1["arg_value"])):
            sys.exit(58)

        symb = dict(arg_type = "int", arg_value = ord(symb1["arg_value"][index]))

        program.save_to_variable(var_name, symb)

# CONCAT <var> <symb> <symb>
class CONCAT(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0].get("arg_value")
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])       

        if (symb1["arg_type"] != "string" or symb2["arg_type"] != "string"):
            sys.exit(53)

        result_string = symb1["arg_value"] + symb2["arg_value"]
        
        symb = dict(arg_type = "string", arg_value = result_string)

        program.save_to_variable(var_name, symb)

# STRLEN <var> <symb>
class STRLEN(Instruction):
    arg_num = 2

    def execute(self):
        var_name = self.args[0].get("arg_value")
        symb1 = self.retrieve_argument(self.args[1])
        
        if (symb1["arg_type"] != "string"):
            sys.exit(53)

        symb = dict(arg_type = "int", arg_value = len(symb1["arg_value"]))

        program.save_to_variable(var_name, symb)

# GETCHAR <var> <symb> <symb>
class GETCHAR(Instruction):
    arg_num = 3

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])
        
        if (symb2["arg_type"] != "int" or symb1["arg_type"] != "string"):
            sys.exit(53)
        
        if (symb2["arg_value"] >= len(symb1["arg_value"])):
            sys.exit(58)

        symb = dict(arg_type = "string", arg_value = symb1["arg_value"][symb2["arg_value"]])

        program.save_to_variable(var_name, symb)

# SETCHAR <var> <symb> <symb>     
class SETCHAR(Instruction):
    arg_num = 3

    def execute(self):
        arg1 = self.args[0]
        symb1 = program.get_variable(arg1["arg_value"])
        symb2 = self.retrieve_argument(self.args[1])
        symb3 = self.retrieve_argument(self.args[2])

        if (symb2["arg_type"] != "int" or symb3["arg_type"] != "string"):
            sys.exit(53)
        
        if (symb2["arg_value"] >= len(symb1["arg_value"])):
            sys.exit(58)

        str_list = list(symb1["arg_value"])
        str_list[symb2["arg_value"]] = symb3["arg_value"][0]
        str_replaced = ''.join(str_list)

        symb1 = dict(arg_type = "string", arg_value = str_replaced)

        program.save_to_variable(arg1["arg_value"], symb1)

# TYPE <var> <symb>
class TYPE(Instruction):
    arg_num = 2

    def execute(self):
        var_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])

        if (symb1["arg_value"] == None):
           symb = dict(arg_type = "string", arg_value = "")
        else:
            symb = dict(arg_type = "string", arg_value = symb1["arg_type"])

        program.save_to_variable(var_name, symb)

# JUMPIFEQ <label> <symb> <symb>
class JUMPIFEQ(Instruction):
    arg_num = 3

    def execute(self):
        label_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])

        
        if (symb2["arg_type"] != "nil" and symb1["arg_type"] != "nil"):
            if (symb1["arg_type"] != symb2["arg_type"]):
                sys.exit(53)
        
        if (symb1["arg_value"] == symb2["arg_value"]):
            if (label_name in program.get_label_names()):
                program.jump_to_index(program.labels[label_name])
            else:
                sys.exit(52)

# JUMPIFNEQ <label> <symb> <symb>
class JUMPIFNEQ(Instruction):
    arg_num = 3

    def execute(self):
        label_name = self.args[0]["arg_value"]
        symb1 = self.retrieve_argument(self.args[1])
        symb2 = self.retrieve_argument(self.args[2])
        
        if (symb2["arg_type"] != "nil" and symb1["arg_type"] != "nil"):
            if (symb1["arg_type"] != symb2["arg_type"]):
                sys.exit(53)

        if (symb1["arg_value"] != symb2["arg_value"]):
            if (label_name in program.get_label_names()):
                program.jump_to_index(program.labels[label_name])
            else:
                sys.exit(52)

# DPRINT <symb>
class DPRINT(Instruction):
    arg_num = 1

    def execute(self):
        symb = self.retrieve_argument(self.args[0])
        
        print(symb["arg_value"], file=sys.stderr)

# EXIT <symb>
class EXIT(Instruction):
    arg_num = 1

    def execute(self):
        symb = self.retrieve_argument(self.args[0])

        if (symb["arg_type"] != "int"):
            sys.exit(53)
        
        if (symb["arg_value"] > 49 or symb["arg_value"] < 0):
            sys.exit(57)
        
        sys.exit(symb["arg_value"])

class BREAK(Instruction):
    arg_num = 0

    def execute(self):
        print("global frame:", file=sys.stderr)
        print(program.global_frame, file=sys.stderr)
        print("local frame:", file=sys.stderr)
        print(program.local_frame, file=sys.stderr)
        print("temporary frame:", file=sys.stderr)
        print(program.temporary_frame, file=sys.stderr)
        print("instruction index: ", file=sys.stderr)
        print(program.instruction_index, file=sys.stderr)

class PUSHS(Instruction):
    arg_num = 1

    def execute(self):
        symb = self.retrieve_argument(self.args[0])
        
        program.data_stack_push(symb)

class POPS(Instruction):
    arg_num = 1

    def execute(self):
        var_name = self.args[0]["arg_value"]

        symb = program.data_stack_pop()

        program.save_to_variable(var_name, symb)

        
#****************************************************************************************************************     


#set up argument parser
parser = argparse.ArgumentParser(prog='interpret.py', description='Interprets XML representation of IPPcode23')
parser.add_argument('--input', help='Specify the input file')
parser.add_argument('--source', help='Specify the source file')

#process arguments
args = parser.parse_args()

if (args.input):
    input_closed = args.input
    inputfile = open(input_closed, 'r')
else:
    inputfile = sys.stdin
if (args.source):
    sourcefile = args.source
else:
    sourcefile = sys.stdin


if not(args.input or args.source):
    print("no source or input specified")
    sys.exit(1)
else:
    try:
        tree=ET.parse(sourcefile)
    except:
        sys.exit(31)

root=tree.getroot()

# XML format checks
if root.tag != 'program':
    sys.exit(32)                                
for inst in root:
    if inst.tag != 'instruction':
        sys.exit(32)                            
    attributes=list(inst.attrib.keys())
    if not('order' in attributes and 'opcode' in attributes):
        sys.exit(32)                            
    arg_nums = []
    for arg in inst:
        if not(re.match(r"arg[123]", arg.tag)):
            sys.exit(32)                        
        arg_nums.append(int(arg.tag[3:]))
    
    if len(arg_nums) != 0:
        arg_nums = sorted(arg_nums)
        iter = 1
        for i in arg_nums:
            if i != iter:
                sys.exit(32)
            iter += 1

factory = InstructionFactory()

program = Program()

# Create instructions
for inst in root:
    try:
        order = int(inst.attrib["order"])
    except:
        sys.exit(32)
    current = factory.create_instruction(inst.attrib["opcode"], order)
    for i in inst:
        number = int(i.tag[3:])
        index = number - 1
        if (i.attrib["type"] == "int"):
            try:
                int_text = int(i.text)
            except:
                sys.exit(32)
            current.add_argument("int", int_text, index)
        elif (i.attrib["type"] == "bool"):
            if (i.text == "true"):
                bool_text = True
            else:
                bool_text = False
            current.add_argument("bool", bool_text, index)
        else:
            current.add_argument(i.attrib["type"], i.text, index)

    program.add_instruction(current)

inst_count = len(program.instructions)

# Sort instructions based on order number
program.instructions = sorted(program.instructions, key=lambda instruction: instruction.order)

# Look for labels and add them to the list
iter = 0
for i in program.instructions:
    if i.opcode == "LABEL":
        program.add_label(i.args[0]["arg_value"], iter)
    iter += 1
    
# Execute each instruction
while (program.instruction_index < inst_count):
    program.instructions[program.instruction_index].check_arg_quantity()
    program.instructions[program.instruction_index].execute()
    program.incr_instr_index()

#print(program.labels)