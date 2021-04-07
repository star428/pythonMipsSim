from Unit import *
from Lexical_analyzer import LexicalAnalyzer

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
        """
        # 各操作既不涉及定向也不涉及流水线互锁，只有简单的输入与输出
        # 输入：pc与另一个beq的地址
        # 输出：改变pc和if/id寄存器的状态（直接return，在总的逻辑里面再处理）
        """
        temp_IF_ID_IR = self.IM.getInst(self.PC.out_PC())

        if self.IF_ID_reg.IR is None: # 初始情况
            temp_PC = self.PC.out_PC() + 1
        else:
            if (self.IF_ID_reg.IR['opCode'] == 'bnez' or \
                self.IF_ID_reg.IR['opCode'] == 'BNEZ') and \
                self.RegFile.outData(self.IF_ID_reg.IR['Rs']) is not 0:# 不等于0跳转
                for inst in self.IM.mem:
                    if inst['addressName'] == self.IF_ID_reg.IR['immediate']:
                        temp_PC = inst['address']
                        break
                # 同时此时把相应取出来的inst清零，因为它不需要
                temp_IF_ID_IR = None


            else:
                temp_PC = self.PC.out_PC() + 1

        return temp_PC, temp_IF_ID_IR

    # IF以后的所有操作均应考虑所有指令（总共四条），并且会传递None（比如beq在ID
    # 结束那么就会将其他数据置为None同时在每一步会有针对None的传递不会出错）

    def ID(self):
        """
        # 目前只支持4条指令，按指令来取值即可（实际需要输出的只有lw,sw,add）
        # 输入端为IF/ID
        # 输出端为ID/EX
        """
        if self.IF_ID_reg.IR['opCode'] == 'bnez' or \
            self.IF_ID_reg.IR['opCode'] == 'BNEZ':
            temp_ID_EX_A = None
            temp_ID_EX_B = None
            temp_ID_EX_imm = None
        else:
            temp_ID_EX_A = self.RegFile.outData(self.IF_ID_reg.IR['Rs'])
            temp_ID_EX_B = self.RegFile.outData(self.IF_ID_reg.IR['Rt'])
            if self.IF_ID_reg.IR['opCode'] == 'add' or \
                self.IF_ID_reg.IR['opCode'] == 'ADD':
                temp_ID_EX_imm = None
            else:
                temp_ID_EX_imm = self.IF_ID_reg.IR['immediate']

        temp_ID_EX_IR = self.IF_ID_reg.IR

        return temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR

    def EX(self):
        """
        # 在这个阶段只有3条指令会执行，也就是分情况讨论即可
        # 输入：ID/EX
        # 输出：EX/MEM
        """
        temp_EX_MEM_ALUo = self.ALU.excute(self.ID_EX_reg.A, self.ID_EX_reg.B, \
            self.ID_EX_reg.imm, self.ID_EX_reg.IR) # 里面包含对四种语句的操作

        temp_EX_MEM_B = self.ID_EX_reg.B
        temp_EX_MEM_IR = self.ID_EX_reg.IR

        return temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR

    def MEM(self):
        """
        # 在这个阶段只有load和store会执行（store会执行完毕向下传none）
        # 输入：EX/MEM
        # 输出：MEM/WB
        """
        if self.EX_MEM_reg.IR['opCode'] == 'lw' or \
            self.EX_MEM_reg.IR['opCode'] == 'LW':
            temp_MEM_WB_LMD = self.DM.outData(self.EX_MEM_reg.ALUo)
            temp_MEM_WB_ALUo = self.EX_MEM_reg.ALUo
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        elif self.EX_MEM_reg.IR['opCode'] == 'sw' or \
            self.EX_MEM_reg.IR['opCode'] == 'SW':
            self.DM.writeData(self.EX_MEM_reg.B, self.EX_MEM_reg.ALUo)

            temp_MEM_WB_LMD = None
            temp_MEM_WB_ALUo = None
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        elif self.EX_MEM_reg.IR['opCode'] == 'add' or \
            self.EX_MEM_reg.IR['opCode'] == 'ADD':
            temp_MEM_WB_LMD = None
            temp_MEM_WB_ALUo = self.EX_MEM_reg.ALUo
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        else:
            temp_MEM_WB_LMD = None
            temp_MEM_WB_ALUo = None
            temp_MEM_WB_IR = self.EX_MEM_reg.IR

        return temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR

    def WB(self):
        """
        # 在这个阶段只有add和load会执行
        # 输入：MEM/WB
        # 输出：到regfile中
        """
        if self.MEM_WB_reg.IR['opCode'] == 'lw' or \
            self.MEM_WB_reg.IR['opCode'] == 'LW':
            self.RegFile.writeData(self.MEM_WB_reg.IR['Rt'], self.MEM_WB_reg.LMD)

        elif self.MEM_WB_reg.IR['opCode'] == 'add' or \
            self.MEM_WB_reg.IR['opCode'] == 'ADD':
            self.RegFile.writeData(self.MEM_WB_reg.IR['Rd'], self.MEM_WB_reg.ALUo)

        else: # beq和sw在这一步没有操作同时不用传递None
            pass


    def runOneCycle(self):
        """
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
        # 否则就代表没有语句要在这个周期在这个部件上执行
        """
        # 数据初定义区
        temp_PC, temp_IF_ID_IR = 10000, None # 10000只不过是设置一个能与int比较的数值，大就行
        temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR = None, None, \
                None, None
        temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR = None, None, None
        temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR = None, None, None

        isConflict = False
        # 数据定义结束

        # 拟定向用在这里
        # 定向结束

        # 各阶段执行开始
        if self.MEM_WB_reg.IR is not None: # 执行WB
            self.WB()

        if self.EX_MEM_reg.IR is not None: # 执行MEM
            temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR = self.MEM()

        if self.ID_EX_reg.IR is not None: # 执行EX
            temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR = self.EX()

        if self.IF_ID_reg.IR is not None: # 执行ID
            temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR = self.ID()

        if self.PC.out_PC() < len(self.IM.mem):
        # 能取到pc的时候就会取pc(取10000的时候代表没有代码了)
            temp_PC, temp_IF_ID_IR = self.IF()

        # 各阶段执行结束
        isConflict = self.testConflict()
        # 以下代码块为流水线冲突检测部件，均在ID段检测
        # 冲突检测结束
        if isConflict:
            temp_PC = self.IF_ID_reg.NPC
            temp_IF_ID_IR = self.IF_ID_reg.IR
            # 以上为送回入口
            temp_ID_EX_A, temp_ID_EX_B, temp_ID_EX_imm, temp_ID_EX_IR = None, \
            None, None, None
            # 以上为将ID/EX中的指令清零

        # 判断结束后进行寄存器的相关写，就直接写即可
        self.PC.in_PC(temp_PC)

        self.IF_ID_reg.in_reg(temp_PC, temp_IF_ID_IR)

        self.ID_EX_reg.in_reg(temp_ID_EX_A, temp_ID_EX_B,\
                temp_ID_EX_imm, temp_ID_EX_IR)

        self.EX_MEM_reg.in_reg(temp_EX_MEM_ALUo, temp_EX_MEM_B, temp_EX_MEM_IR)

        self.MEM_WB_reg.in_reg(temp_MEM_WB_LMD, temp_MEM_WB_ALUo, temp_MEM_WB_IR)

        self.clock = self.clock + 1

    def testConflict(self):
        if self.ID_EX_reg.IR is not None and self.IF_ID_reg.IR is not None:
            if self.ID_EX_reg.IR['opCode'] == 'lw' and self.IF_ID_reg.IR['opCode'] == 'lw':

                if self.ID_EX_reg.IR['Rt'] == self.IF_ID_reg.IR['Rs']:# IS不能乱用（惨痛教训
                    return True
                else:
                    return False
            else:
                return False


        if self.EX_MEM_reg.IR is not None and self.IF_ID_reg.IR is not None:
            if self.EX_MEM_reg.IR['opCode'] == 'lw' and self.IF_ID_reg.IR['opCode'] == 'lw':

                if self.EX_MEM_reg.IR['Rt'] == self.IF_ID_reg.IR['Rs']:
                    return True
                else:
                    return False
            else:
                return False

        return False

    def showStation(self):
        print('pc', self.PC.out_PC())
        print('IF/ID', self.IF_ID_reg.out_reg())
        print('ID/EX', self.ID_EX_reg.out_reg())
        print('EX/MEM', self.EX_MEM_reg.out_reg())
        print('MEM/WB', self.MEM_WB_reg.out_reg())

if __name__ == '__main__':
    str1 = """lw $R1,10($R4)
lw $R3,0($R1)
add $R5,$R6,$R7
"""
    anaylse = LexicalAnalyzer(str1)
    print(anaylse.codeList)
    print(anaylse.returnCodeAnalyseStr())
    cpu = CPU(anaylse.returnCodeAnalyse())
    for i in range(9):
        cpu.runOneCycle()
        cpu.showStation()
    print(cpu.RegFile.rf)
    print(cpu.DM.mem)
    # for i in range(3):
    #     cpu.runOneCycle()
    #     cpu.showStation()
