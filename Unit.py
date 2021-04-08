class PC():
    def __init__(self):
        self.PC = 0

    def in_PC(self, value):
        self.PC = value

    def out_PC(self):
        return self.PC

    def PC_next(self):
        self.PC = self.PC + 1

    def PC_reset(self):
        self.PC = 0

class IF_ID_reg():
    def __init__(self):
        self.NPC = None
        self.IR = None

    def in_reg(self, NPC, IR):
        self.NPC = NPC
        self.IR = IR

    def  out_reg(self):
        return self.NPC, self.IR

class ID_EX_reg():
    def __init__(self):
        self.A = None
        self.B = None
        self.imm = None
        self.IR = None

    def in_reg(self, A, B, imm, IR):
        self.A = A
        self.B = B
        self.imm = imm
        self.IR = IR

    def out_reg(self):
        return self.A, self.B, self.imm, self.IR

class EX_MEM_reg():
    def __init__(self):
        self.ALUo = None
        self.B = None
        self.IR = None

    def in_reg(self, ALUo, B, IR):
        self.ALUo = ALUo
        self.B = B
        self.IR = IR

    def out_reg(self):
        return self.ALUo, self.B, self.IR

class MEM_WB_reg():
    def __init__(self):
        self.LMD = None
        self.ALUo = None
        self.IR  = None

    def in_reg(self, LMD, ALUo, IR):
        self.LMD = LMD
        self.ALUo = ALUo
        self.IR = IR

    def out_reg(self):
        return self.LMD, self.ALUo, self.IR

class IM():
    def __init__(self):
        self.mem = None

    def initIM(self, instDict):
        self.mem = instDict # 仍旧是list，里面是dict

    def getInst(self, address):
        return self.mem[address] # 按照index取出inst

class RegFile():
    def __init__(self):
        self.rf = {}
        self.initRF()

    def initRF(self):
        for index in range(32):
            self.rf['$R%s' % index] = 1
            self.rf['$F%s' % index] = 0

    def outData(self, regName):
        return self.rf[regName]

    def writeData(self, regName, Data):
        self.rf[regName] = Data

class ALU():
    def excute(self, A, B, imm, IR):
        if IR['opCode'] == 'lw' or \
                IR['opCode'] == 'LW' or \
                IR['opCode'] == 'sw' or \
                IR['opCode'] == 'SW':
                return A + imm

        if IR['opCode'] == 'add' or IR['opCode'] == 'ADD':
            return A + B
        # 虽然不执行但是还是得保证它有五段流水线
        if IR['opCode'] == 'bnez' or IR['opCode'] == 'BNEZ':
            return None

class DM():
    def __init__(self):
        self.mem = {}
        self.initDM()

    def initDM(self):
        for index in range(64):
            self.mem[index] = index

    def outData(self, address):
        return self.mem[address] # 这里的address是数值

    def writeData(self, address, data):
        self.mem[address] = data

if __name__ == "__main__":
    RegFile = RegFile()
    print(RegFile.rf)
