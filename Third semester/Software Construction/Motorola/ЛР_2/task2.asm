 org $8000

 ldy #$0000
 ldx #$8200

MAIN_LOOP:
 ldaa 0,x
 ldab #8

BIT_LOOP:
 lsra
 bcs SKIP_COUNT
 iny         

SKIP_COUNT:
 decb
 bne BIT_LOOP
 inx

 cpx #$8220
 bne MAIN_LOOP

END:   


 
