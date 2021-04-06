from Unit import *

class CPU():
    def __init__(self, codeList):
        # 初始化所有部件（从左到右）
        self.PC = PC()
        self.IF_ID_reg = IF_ID_reg()
        self.ID_EX_reg = ID_EX_reg()
        self.EX_MEM_reg = EX_MEM_reg()
        self.MEM_WB_reg = MEM_WB_reg()

        self.IM = IM()
        self.IM.initIM(codeList)

        self.RegFile = RegFile()

        self.ALU = ALU()

        self.DM = DM()

        self.clock = 0

    def IF(self):
        # 各操作既不涉及定向也不涉及流水线互锁，只有简单的输入与输出
        # 输入：pc与另一个beq的地址
        # 输出：改变pc和if/id寄存器的状态（直接return，在总的逻辑里面再处理）
        temp_IF_ID_IR = self.IM.getInst(self.PC.out_PC())

        if (self.IF_ID_reg.IR['opCode'] == 'benz' or \
            self.IF_ID_reg.IR['opCode'] == 'BENZ') and \
            self.RegFile.outData(self.IF_ID_reg.IR['Rs']) == 0:
            for inst in self.IM.mem:
                if inst['addressName'] == self.IF_ID_reg.IR['addressName']:
                    temp_PC = inst['address']

        else:
            temp_PC = self.PC + 1

        return temp_PC, temp_IF_ID_IR

    def ID(self):
        # 目前只支持4条指令，按指令来取值即可（实际需要输出的只有lw,sw,add）
        # 输入端为IF/ID
        # 输出端为ID/EX

        temp_ID_EX_A = self.RegFile.outData(self.IF_ID_reg.IR['Rs'])
        temp_ID_EX_B = self.RegFile.outData(self.IF_ID_reg.IR['Rt'])
        if self.IF_ID_reg.IR['opCode'] == 'add' or \
            self.IF_ID_reg.IR['opCode'] == 'ADD':
            temp_ID_EX_imm = self.IF_ID_reg.IR['immediate']
        else:
            temp_ID_EX_imm = None

        temp_ID_EX_IR = self.IF_ID_reg.IR

        return temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR

    def EX(self):
        # 在这个阶段只有3条指令会执行，也就是分情况讨论即可
        # 输入：ID/EX
        # 输出：EX/MEM

        temp_EX_MEM_ALUo = self.ALU.excute(self.ID_EX_reg.A, self.ID_EX_reg.B, \
            self.ID_EX_reg.imm, self.ID_EX_reg.IR)

        temp_EX_MEM_B = self.ID_EX_reg.B
        temp_EX_MEM_IR = self.ID_EX_reg.IR

        return temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR

    def MEM(self):
        # 在这个阶段只有load和store会执行（store会执行完毕向下传none）
        # 输入：EX/MEM
        # 输出：MEM/WB

        if self.EX_MEM_reg.IR['opCode'] == 'lw' or \
            self.EX_MEM_reg.IR['opCode'] == 'LW':
            temp_MEM_WB_LMD = self.DM.outData(self.EX_MEM_reg.ALUo)
            temp_MEM_WB_ALUo = self.EX_MEM_reg.ALUo
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        else if self.EX_MEM_reg.IR['opCode'] == 'sw' or \
            self.EX_MEM_reg.IR['opCode'] == 'SW':
            self.DM.writeData(self.EX_MEM_reg.B, self.EX_MEM_reg.ALUo)

            temp_MEM_WB_LMD = None
            temp_MEM_WB_ALUo = None
            temp_MEM_WB_IR = None

        else:
            temp_MEM_WB_LMD = None
            temp_MEM_WB_ALUo = self.EX_MEM_reg.ALUo
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        return temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR

    def WB(self):
        # 在这个阶段只有add和load会执行
        # 输入：MEM/WB
        # 输出：到regfile中
        if self.MEM_WB_reg.IR['opCode'] == 'lw' or \
            self.MEM_WB_reg.IR['opCode'] == 'LW':
            self.RegFile.writeData(self.MEM_WB_reg.IR['Rt'], self.MEM_WB_reg.LMD)

        else:
            self.RegFile.writeData(self.MEM_WB_reg.IR['Rd'], self.MEM_WB_reg.ALUo)


    def runOneCycle(self):
        # 接下来先5个模块并行执行同时储存中间变量不着急打入下一个寄存器
        # 虽然并行但是还是得按照一定顺序，由于WB不会影响其他，所以先执行
        # 同时ID取操作在第二个时钟周期的后半段，得在WB的后米娜
        # 然后IF又受限于ID的判断，如果存在相关得先等ID执行完
        # 这些问题都是由这个不是正规的数据流向所导致的，如果像Verilog一样
        # 有着持续一个周期的节拍，那么不会有这种问题，我们现在的模拟就是相当于
        # 一个脉冲执行，所以选择从后函数向前函数执行，会冲掉这个限制

        # 然后进行cu中冲突的检测和相关操作
        # 最后将cu处理后的相关的中间变量打入相应的处理器

        # 这里我们设置如果每个寄存器的IR不是None，那么代表有程序在这一段执行
        # 否则我们就不执行，表明这一段目前没有函数在执行

        if self.MEM_WB_reg.IR is not None: # 执行WB
            self.WB()

        if self.EX_MEM_reg.IR is not None: # 执行MEM
            temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR = self.MEM()

        if self.ID_EX_reg.IR is not None: # 执行EX
            temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR = self.EX()

        if self.IF_ID_reg.IR is not None: # 执行ID
            temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR = self.ID()

        temp_PC, temp_IF_ID_IR = self.IF()
