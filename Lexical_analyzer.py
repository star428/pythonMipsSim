class LexicalAnalyzer():
    def __init__(self, strCode):
        self.strCode = strCode
        self.codeList = [] # 未分析的语句
        self.codeDict = [] # 分析后的语句
        self.divideIntoPer()
        self.analyseInstruction()

    def divideIntoPer(self):
        # 将str转换为一个个的单行

        start = 0
        for end in range(len(self.strCode)):
            if self.strCode[end] == '\n':
                strTemp = self.strCode[start:end]
                self.codeList.append(strTemp)
                start = end + 1

    def analyseInstruction(self):
        # 将每一句翻译同时生成一个list里面每个dict都是相关语句的信息

        ifPass = False # 跳过已经在地址表示符号时处理过的地址的吓一跳语句
        for index in range(len(self.codeList)):

            tempInst = self.codeList[index] # 取出单条指令
            tempdict = {'address':None, 'addressName':None, 'opCode':None, \
            'Rs':None, 'Rt':None, 'Rd':None, 'immediate':None} # 储存单条指令的相关信息

            if ifPass:
                ifPass = False
                continue

            if tempInst.find(' ') == -1: # 意味着这个是地址的表示符号
                tempdict['addressName'] = tempInst[:-1]

                tempInst = self.codeList[index + 1]
                ifPass = True

            tempdict['opCode'] = tempInst[:tempInst.find(' ')]
            tempInst = tempInst[tempInst.find(' ') + 1:] # 现在的inst就是不包含opcode的inst

            if tempdict['opCode'] == 'lw' or \
                    tempdict['opCode'] == 'LW' or \
                    tempdict['opCode'] == 'sw' or \
                    tempdict['opCode'] == 'SW':

                    tempdict['Rt'] = tempInst[ : tempInst.find(',')]
                    tempdict['immediate'] = int(tempInst[tempInst.find(',') + 1: \
                        tempInst.find('(')])
                    tempdict['Rs'] = tempInst[tempInst.find('(') + 1 : -1]

            if tempdict['opCode'] == 'add' or \
                    tempdict['opCode'] == 'ADD':

                    for reg in ['Rd', 'Rs']:
                        tempdict[reg] = tempInst[ : tempInst.find(',')]
                        tempInst = tempInst[tempInst.find(',') + 1 : ]

                    tempdict['Rt'] = tempInst

            if tempdict['opCode'] == 'bnez' or \
                    tempdict['opCode'] == 'BNEZ':

                    tempdict['Rs'] = tempInst[ : tempInst.find(',')]
                    tempdict['immediate'] = tempInst[tempInst.find(',') + 1 :]

            self.codeDict.append(tempdict)

        # 最后根据分析的条目给出各个地址
        for index in range(len(self.codeDict)):
            self.codeDict[index]['address'] = index


    def returnCodeAnalyse(self):
        return self.codeDict

    def returnCodeAnalyseStr(self):
        string = ''
        for dict in self.codeDict:
            string = string + str(dict) + '\n'

        return string

if __name__ == '__main__':

# str是自带的，如果使用str当变量名会导致冲突
    str1 = """lw $t0,10($t1)
sw $t0,10($t1)
BNEZ R1,NAME
NAME:
add $t0,$t1,$t2
BNEZ R2,func
add $t1,$t2,$t3
sw $t0,50($t0)
func:
add $s1,$s3,$s2
"""
    lexical = LexicalAnalyzer(str1)
    print(lexical.codeList)
    print(lexical.returnCodeAnalyseStr())
