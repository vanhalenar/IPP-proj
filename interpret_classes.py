class Argument:
    def __init__(self, typ, value) -> None:
        self.type = typ
        self.value = value

class Instruction:
    inst_counter = 0
    def __init__(self, opcode) -> None:
        self.opcode = opcode
        self.args = []
        Instruction.inst_counter += 1
        self.order = Instruction.inst_counter
        

    def add_argument(self, typ, value):
        self.args.append(Argument(typ, value))
    
    def execute():
        print("not implemented!")

class Program():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Program, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.instructions = []
    def add_instruction(self, instr):
        self.instructions.append(instr)

class InstructionFactory():
    def create_instruction(self, opcode):
        if opcode == "WRITE":
            return WRITE(opcode)

class WRITE(Instruction):
    def execute(self):
        print("im writin")
