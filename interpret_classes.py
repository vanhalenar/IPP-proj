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
            #print("wrong order!")               #remove this before submitting
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
        self.temporary_frame = None
        self.local_frame = None
        self.instruction_index = 0
        self.labels = dict()
        self.call_stack = []

    def add_instruction(self, instr):
        self.instructions.append(instr)
        pass
    
    def create_frame(self):
        self.temporary_frame = dict()
    
    def push_frame(self):
        if self.temporary_frame is not None:
            self.frames_stack.append(self.temporary_frame)
            self.local_frame = self.frames_stack[-1]
            self.temporary_frame = None
        else:
            sys.exit(55)
    
    def pop_frame(self):
        if self.local_frame is not None:
            self.temporary_frame = self.frames_stack.pop()
            if self.frames_stack:
                self.local_frame = self.frames_stack[-1]
            else:
                self.local_frame = None
        else:
            sys.exit(55)
    
    def get_variable(self, var):
        if (re.match(r"^GF@", var)):
            return program.global_frame[var[3:]]
        elif (re.match(r"^LF@", var)):
            if (program.local_frame is not None):
                return program.local_frame[var[3:]]
            else:
                sys.exit(55)
        elif (re.match(r"^TF@", var)):
            if (program.temporary_frame is not None):
                return program.temporary_frame[var[3:]]
            else:
                sys.exit(55)
        else:
            print("bad, very bad") #change
            sys.exit() #what code
    
    def save_to_variable(self, var, symb):
        if (re.match(r"^GF@", var)):
            program.global_frame[var[3:]] = symb
        elif (re.match(r"^LF@", var)):
            program.local_frame[var[3:]] = symb
        elif (re.match(r"^TF@", var)):
            program.temporary_frame[var[3:]] = symb
        else:
            print("bad, very bad") #change
            sys.exit() #figure this out
    
    def add_label(self, label_name, label_num):
        if (label_name not in self.labels.keys()):
            self.labels[label_name] = label_num
        elif (self.labels[label_name] == label_num):
            pass
        else:
            sys.exit(52)
    
    def get_current_line(self):
        return self.instruction_index
    
    def incr_instr_index(self):
        self.instruction_index += 1
    
    def call_stack_push(self, value):
        self.call_stack.append(value)
    
    def call_stack_pop(self):
        return self.call_stack.pop()

        

program = Program()

class InstructionFactory():
    def create_instruction(self, opcode, order):
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
        elif opcode == "STR2INT":
            return STR2INT(opcode, order)
        elif opcode == "RETURN":
            return RETURN(opcode, order)
        elif opcode == "GETCHAR":
            return GETCHAR(opcode, order)
        elif opcode == "SETCHAR":
            return SETCHAR(opcode, order)
        elif opcode == "DEFVAR":
            return DEFVAR(opcode, order)
        elif opcode == "CONCAT":
            return CONCAT(opcode, order)
        elif opcode == "STRLEN":
            return STRLEN(opcode, order)
        elif opcode == "LABEL":
            return LABEL(opcode, order)
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
        

class WRITE(Instruction):
    arg_num = 1
    def execute(self):
        arg = self.args[0]

        if (arg["arg_type"] == "var"):
            variable = program.get_variable(arg["arg_value"])
        else:    
            variable = arg
        string = variable["arg_value"]

        if (variable["arg_type"] == "string"):
            pattern = r'\\([0-9]{3})'
            escape_seqs = re.findall(pattern, string)

            for escape_seq in escape_seqs:
                char_code = int(escape_seq)
                ascii_char = chr(char_code)
                string = string.replace('\\' + escape_seq, ascii_char)

        print(string, end='')

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
        elif (self.args[1].get("arg_value") == "bool"):
            if (user_input == "true"):
                symb = dict(arg_type = "bool", arg_value = "true")
            else:
                symb = dict(arg_type = "bool", arg_value = "false")
        elif (self.args[1].get("arg_value") == "string"):
            symb = dict(arg_type = "string", arg_value = user_input)
        
        program.save_to_variable(self.args[0].get("arg_value"), symb)

class JUMP(Instruction):
    arg_num = 1
    def execute(self):
        label_name = self.args[0].get("arg_value")

        if (label_name in program.labels.keys()):
            program.instruction_index = program.labels[label_name]
        else:
            sys.exit(52)

class LABEL(Instruction):
    arg_num = 1
    def execute(self):
        label_name = self.args[0].get("arg_value")
        label_line = program.get_current_line()
        program.add_label(label_name, label_line)

class CALL(Instruction):
    arg_num = 1
    def execute(self):
        label_name = self.args[0].get("arg_value")
        program.call_stack_push(self.order+2) #i can explain
        program.instruction_index = program.labels[label_name]

class RETURN(Instruction):
    arg_num = 0
    def execute(self):
        program.instruction_index = program.call_stack_pop()

class EQ(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg1["arg_value"])
        else:
            symb3 = arg3

        if (symb2["arg_type"] != symb3["arg_type"]):
            symb = dict(arg_type = "bool", arg_value = "false")
            program.save_to_variable(arg1["arg_value"], symb)
            return
        
        if (symb2["arg_value"] == symb3["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(arg1["arg_value"], symb)

class GT(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg1["arg_value"])
        else:
            symb3 = arg3

        if (symb2["arg_type"] != symb3["arg_type"]):
            symb = dict(arg_type = "bool", arg_value = "false")
            program.save_to_variable(arg1["arg_value"], symb)
            return
        
        if (symb2["arg_value"] > symb3["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(arg1["arg_value"], symb)


class LT(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg1["arg_value"])
        else:
            symb3 = arg3

        if (symb2["arg_type"] != symb3["arg_type"]):
            symb = dict(arg_type = "bool", arg_value = "false")
            program.save_to_variable(arg1["arg_value"], symb)
            return
        
        if (symb2["arg_value"] < symb3["arg_value"]):
            symb = dict(arg_type = "bool", arg_value = "true")
        else:
            symb = dict(arg_type = "bool", arg_value = "false")
            
        program.save_to_variable(arg1["arg_value"], symb)

class AND(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg3["arg_value"])
        else:
            symb3 = arg3
        
        if (symb2["arg_type"] != "bool" or symb3["arg_type"] != "bool"):
            sys.exit(53)

        result = symb2["arg_value"] and symb3["arg_value"]

        symb = dict(arg_type = "bool", arg_value = result)

        program.save_to_variable(arg1["arg_value"], symb)

class OR(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg3["arg_value"])
        else:
            symb3 = arg3
        
        if (symb2["arg_type"] != "bool" or symb3["arg_type"] != "bool"):
            sys.exit(53)

        result = symb2["arg_value"] or symb3["arg_value"]

        symb = dict(arg_type = "bool", arg_value = result)

        program.save_to_variable(arg1["arg_value"], symb)

class NOT(Instruction):
    arg_num = 2
    def execute(self):
        arg2 = self.args[1]
        arg1 = self.args[0]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2

        if (symb2["arg_type"] != "bool"):
            sys.exit(53)

        symb = dict(arg_type = "bool", arg_value = not symb2["arg_value"])

        program.save_to_variable(arg1["arg_value"], symb)

class INT2CHAR(Instruction):
    arg_num = 2
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (symb2["arg_type"] != "int"):
            sys.exit(53)

        symb = dict(arg_type = "string", arg_value = chr(symb2["arg_value"]))

        program.save_to_variable(arg1["arg_value"], symb)

class STR2INT(Instruction):
    arg_num = 2
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (symb2["arg_type"] != "string"):
            sys.exit(53)

        symb = dict(arg_type = "string", arg_value = ord(symb2["arg_value"]))

        program.save_to_variable(arg1["arg_value"], symb)

class CONCAT(Instruction):
    arg_num = 3
    def execute(self):
        dest_var_name = self.args[0].get("arg_value")
        arg1 = self.args[1]
        arg2 = self.args[2]

        if (arg1["arg_type"] == "var"):
            symb1 = program.get_variable(arg1["arg_value"])
        else:
            symb1 = arg1

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2        

        if (symb1["arg_type"] != "string" or symb2["arg_type"] != "string"):
            sys.exit(53)

        result_string = symb1["arg_value"] + symb2["arg_value"]
        
        symb = dict(arg_type = "string", arg_value = result_string)

        program.save_to_variable(dest_var_name, symb)

class STRLEN(Instruction):
    arg_num = 2
    def execute(self):
        dest_var_name = self.args[0].get("arg_value")
        arg1 = self.args[1]

        if (arg1["arg_type"] == "var"):
            symb1 = program.get_variable(arg1["arg_value"])
        else:
            symb1 = arg1
        
        if (symb1["arg_type"] != "string"):
            sys.exit(53)

        symb = dict(arg_type = "string", arg_value = len(symb1["arg_value"]))

        program.save_to_variable(dest_var_name, symb)

class GETCHAR(Instruction):
    arg_num = 3
    def execute(self):
        dest_var_name = self.args[0].get("arg_value")
        arg1 = self.args[1]
        arg2 = self.args[2]

        if (arg1["arg_type"] == "var"):
            symb1 = program.get_variable(arg1["arg_value"])
        else:
            symb1 = arg1

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2
        
        if (symb2["arg_type"] != "int" or symb1["arg_type"] != "string"):
            sys.exit(53)
        
        if (symb2["arg_value"] >= len(symb1["arg_value"])):
            sys.exit(58)

        symb = dict(arg_type = "string", arg_value = symb1["arg_value"][symb2["arg_value"]])

        program.save_to_variable(dest_var_name, symb)
        
class SETCHAR(Instruction):
    arg_num = 3
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]
        arg3 = self.args[2]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2

        if (arg3["arg_type"] == "var"):
            symb3 = program.get_variable(arg3["arg_value"])
        else:
            symb3 = arg3

        symb1 = program.get_variable(arg1["arg_value"])

        if (symb2["arg_type"] != "int" or symb3["arg_type"] != "string"):
            sys.exit(53)
        
        if (symb2["arg_value"] >= len(symb1["arg_value"])):
            sys.exit(58)

        str_list = list(symb1["arg_value"])
        str_list[symb2["arg_value"]] = symb3["arg_value"][0]
        str_replaced = ''.join(str_list)

        symb1 = dict(arg_type = "string", arg_value = str_replaced)

        program.save_to_variable(arg1["arg_value"], symb1)

class TYPE(Instruction):
    arg_num = 2
    def execute(self):
        arg1 = self.args[0]
        arg2 = self.args[1]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2

        if (symb2["arg_value"] == None):
           symb = dict(arg_type = "string", arg_value = "")
        else:
            symb = dict(arg_type = "string", arg_value = symb2["arg_type"])

        program.save_to_variable(arg1["arg_value"], symb)

class JUMPIFEQ(Instruction):
    arg_num = 3
    def execute(self):
        label_name = self.args[0]["arg_value"]
        arg1 = self.args[1]
        arg2 = self.args[2]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2

        if (arg1["arg_type"] == "var"):
            symb1 = program.get_variable(arg1["arg_value"])
        else:
            symb1 = arg1
        
        if (symb1["arg_value"] == symb2["arg_value"]):
            if (label_name in program.labels.keys()):
                program.instruction_index = program.labels[label_name]
            else:
                sys.exit(52)

class JUMPIFNEQ(Instruction):
    arg_num = 3
    def execute(self):
        label_name = self.args[0]["arg_value"]
        arg1 = self.args[1]
        arg2 = self.args[2]

        if (arg2["arg_type"] == "var"):
            symb2 = program.get_variable(arg2["arg_value"])
        else:
            symb2 = arg2

        if (arg1["arg_type"] == "var"):
            symb1 = program.get_variable(arg1["arg_value"])
        else:
            symb1 = arg1
        
        if (symb1["arg_value"] != symb2["arg_value"]):
            if (label_name in program.labels.keys()):
                program.instruction_index = program.labels[label_name]
            else:
                sys.exit(52)