lw $R0,10($R1)
sw $R0,10($R1)
BNEZ R1,NAME
NAME:
add $R0,$R1,$R2
BNEZ R2,func
add $R1,$R2,$R3
sw $R0,10($R0)
func:
add $R1,$R3,$R2
