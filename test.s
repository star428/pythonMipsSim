lw $t0,10($t1)
sw $t0,10($t1)
BENZ R1,NAME
NAME:
add $t0,$t1,$t2
BENZ R2,func
add $t1,$t2,$t3
sw $t0,50($t0)
func:
add $s1,$s3,$s2
