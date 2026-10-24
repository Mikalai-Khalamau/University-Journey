 org $00f4

 jmp prer

 org $8000

CODE:
 swi
 
DONE:
 bra *

PRER:
 ldx #$1f04
 ldaa #$23
 deca

END:
 