.model small
.stack 0100h
.data
    message db "Et tu, Brute?", 13, 10, '$'
.code
start:
    mov ax, @data
    mov ds, ax
    
    lea dx, message
    mov ah, 09h
    int 021h
    
end start