import sys
import re

class Argument:
    def __init__(self, typ, value) -> None:
        self.type = typ
        self.value = value

class Instruction:
    inst_counter = 0
    arg_num = 0
    def __init__(self, opcode, order) -> None:
        self.opcode = opcode
        self.args = []
        Instruction.inst_counter += 1
        if (order != Instruction.inst_counter):
            print("wrong order!")               #remove this before submitting
            sys.exit(32)
        self.order = Instruction.inst_counter
        

    def add_argument(self, typ, value):
        self.args.append(dict(arg_type = typ, arg_value = value))
    
    def execute():
        print("not implemented!")
    
    def check_and_execute():
        pass

class Program():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Program, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.instructions = []
        self.frames_stack = []      #append() to push, pop() to pop
        self.global_frame = dict()
        self.temporary_frame = dict()
        self.local_frame = None
        self.instruction_index = 0
        self.labels = dict()

    def add_instruction(self, instr):
        self.instructions.append(instr)
        pass
    
    def create_frame(self):
        self.temporary_frame = dict()
    
    def push_frame(self):
        self.frames_stack.append(self.temporary_frame)
        self.local_frame = self.frames_stack[-1]
    
    def pop_frame(self):
        self.temporary_frame = self.frames_stack.pop()
        if self.frames_stack:
            self.local_frame = self.frames_stack[-1]
        else:
            self.local_frame = None
    
    def get_variable(self, var):
        if (re.match(r"^GF@", var)):
            return program.global_frame[var[3:]]
        elif (re.match(r"^LF@", var)):
            return program.local_frame[var[3:]]
        elif (re.match(r"^TF@", var)):
            return program.temporary_frame[var[3:]]
        else:
            print("bad, very bad") #change
    
    def save_to_variable(self, var, symb):
        if (re.match(r"^GF@", var)):
            program.global_frame[var[3:]] = symb
        elif (re.match(r"^LF@", var)):
            program.local_frame[var[3:]] = symb
        elif (re.match(r"^TF@", var)):
            program.temporary_frame[var[3:]] = symb
        else:
            print("bad, very bad") #change
    
    def add_label(self, label_name, label_num):
        self.labels[label_name] = label_num
    
    def get_current_line(self):
        return self.instruction_index
    
    def incr_instr_index(self):
        self.instruction_index += 1
        

program = Program()

class InstructionFactory():
    def create_instruction(self, opcode, order):
        if opcode == "WRITE":
            return WRITE(opcode, order)
        elif opcode == "CREATEFRAME":
            return CREATEFRAME(opcode, order)
        elif opcode == "PUSHFRAME":
            return PUSHFRAME(opcode, order)
        elif opcode == "POPFRAME":
            return POPFRAME(opcode, order)
        elif opcode == "DEFVAR":
            return DEFVAR(opcode, order)
        elif opcode == "LABEL":
            return LABEL(opcode, order)
        elif opcode == "JUMP":
            return JUMP(opcode, order)
        elif opcode == "MOVE":
            return MOVE(opcode, order)
        elif opcode == "READ":
            return READ(opcode, order)
        elif opcode == "IDIV":
            return IDIV(opcode, order)
        elif opcode == "ADD":
            return ADD(opcode, order)
        elif opcode == "SUB":
            return SUB(opcode, order)
        elif opcode == "MUL":
            return MUL(opcode, order)
        

class WRITE(Instruction):
    arg_num = 1
    def execute(self):
        arg = self.args[0]

        if (arg["arg_type"] == "var"):
            variable = program.get_variable(arg["arg_value"])
            print(variable["arg_value"])
        else:    
            print(self.args[0].get("arg_value"), end='')

class CREATEFRAME(Instruction):
    arg_num = 0
    def execute(self):
        program.create_frame()

class PUSHFRAME(Instruction):
    arg_num = 0
    def execute(self):
        program.push_frame()

class POPFRAME(Instruction):
    arg_num = 0
    def execute(self):
        program.pop_frame()

class DEFVAR(Instruction):
    arg_num = 1
    def execute(self):
        var_name_frame = self.args[0].get("arg_value")
        var_name = var_name_frame[3:]

        if (re.match(r"^GF@", var_name_frame)):
            if var_name not in program.global_frame.keys():
                program.global_frame[var_name] = dict(arg_type = "", arg_value = "")
            else:
                sys.exit(52)

        elif (re.match(r"^LF@", var_name_frame)):
            if var_name not in program.local_frame.keys():
                program.local_frame[var_name] = dict(arg_type = "", arg_value = "")
            else:
                sys.exit(52)

        elif (re.match(r"^TF@", var_name_frame)):
            if var_name not in program.temporary_frame.keys():
                program.temporary_frame[var_name] = dict(arg_type = "", arg_value = "")
            else:
                sys.exit(52)

        else:
            pass #handle error

#MOVE <var> <symb>
class MOVE(Instruction):
    arg_num = 2
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]

        if (arg2["arg_type"] == "var"):
            symb = program.get_variable(arg2["arg_value"])
        else:
            symb = arg2
        
        var_name = arg1["arg_value"]

        program.save_to_variable(var_name, symb)

#ADD <var> <symb> <symb>
class ADD(Instruction):
    arg_num = 3
    def execute(self):
        if (self.args[2].get("arg_type") == "var"):
            operand2 = program.get_variable(self.args[2].get("arg_value"))
        else:
            operand2 = self.args[2]
        
        if (self.args[1].get("arg_type") == "var"):
            operand1 = program.get_variable(self.args[1].get("arg_value"))
        else:
            operand1 = self.args[1]
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 + value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

class SUB(Instruction):
    arg_num = 3
    def execute(self):
        if (self.args[2].get("arg_type") == "var"):
            operand2 = program.get_variable(self.args[2].get("arg_value"))
        else:
            operand2 = self.args[2]
        
        if (self.args[1].get("arg_type") == "var"):
            operand1 = program.get_variable(self.args[1].get("arg_value"))
        else:
            operand1 = self.args[1]
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 - value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

class MUL(Instruction):
    arg_num = 3
    def execute(self):
        if (self.args[2].get("arg_type") == "var"):
            operand2 = program.get_variable(self.args[2].get("arg_value"))
        else:
            operand2 = self.args[2]
        
        if (self.args[1].get("arg_type") == "var"):
            operand1 = program.get_variable(self.args[1].get("arg_value"))
        else:
            operand1 = self.args[1]
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        value = value1 * value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

class IDIV(Instruction):
    arg_num = 3
    def execute(self):
        if (self.args[2].get("arg_type") == "var"):
            operand2 = program.get_variable(self.args[2].get("arg_value"))
        else:
            operand2 = self.args[2]
        
        if (self.args[1].get("arg_type") == "var"):
            operand1 = program.get_variable(self.args[1].get("arg_value"))
        else:
            operand1 = self.args[1]
        
        if (operand1["arg_type"] != "int" or operand2["arg_type"] != "int"):
            sys.exit(53)

        value1 = operand1["arg_value"]
        value2 = operand2["arg_value"]

        if (value2 == 0):
            sys.exit(57)

        value = value1 // value2
    
        symb = dict(arg_type = "int", arg_value = value)

        program.save_to_variable(self.args[0].get("arg_value"), symb)

class READ(Instruction):
    arg_num = 2
    def execute(self):
        user_input = input('enter input: ')
        if (self.args[1].get("arg_value") == "int"):
            try:
                user_input = int(user_input)
                symb = dict(arg_type = self.args[1].get("arg_value"), arg_value = user_input)
            except:
                symb = dict(arg_type = "nil", arg_value = "nil")
        
        program.save_to_variable(self.args[0].get("arg_value"), symb)

class JUMP(Instruction):
    arg_num = 1
    def execute(self):
        label_name = self.args[0].get("arg_value")

        program.instruction_index = program.labels[label_name]

class LABEL(Instruction):
    arg_num = 1
    def execute(self):
        label_name = self.args[0].get("arg_value")
        label_line = program.get_current_line()
        program.add_label(label_name, label_line)
        