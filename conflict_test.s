1. lw and lw

lw $R1,10($R4)
lw $R3,0($R1)
add $R5,$R6,$R7

2. lw and sw

lw $R1,0($R2)
sw $R1,1($R2)
add $R5,$R6,$R7

3. lw and add

lw $R1,0($R2)
add $R3,$R1,$R2
add $R5,$R6,$R7

4. lw and bnez

lw $R1,0($R2)
bnez $R1,NAME 
add $R5,$R6,$R7
NAME:
add $R8,$R9,$R10

sw不会与其他的任何指令相冲突
bnez也不会与任何指令相冲突（控制冲突在if段已经解决会直接将相关的寄存器清零）

5. add and lw

add $R3,$R1,$R2
lw $R4,0($R3)
add $R5,$R6,$R7

6. add and sw

add $R3,$R1,$R2
sw $R4,0($R3)
add $R5,$R6,$R7

7. add and add

add $R3,$R1,$R2
add $R4,$R3,$R1
add $R5,$R6,$R7

8. add and bnez

add $R3,$R1,$R2
bnez $R3,name
add $R5,$R6,$R7
name:
add $R8,$R9,$R10
