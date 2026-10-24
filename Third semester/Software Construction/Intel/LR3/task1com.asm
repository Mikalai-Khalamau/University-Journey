.model tiny
.code 
start:
    org 0100h
    mov ah, 09h
    mov dx, offset message
    int 021h
    
    ret
    
    message db "English or Spanish?", 13, 10, '$'
end start