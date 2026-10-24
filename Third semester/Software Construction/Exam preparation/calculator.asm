; Simple calculator
    .model small
    .stack 200h

MAXLEN EQU 10

    .data
num1_str    db MAXLEN, 0, MAXLEN dup(0)
num2_str    db MAXLEN, 0, MAXLEN dup(0)
operation   db ?
num1        dw ?
num2        dw ?
result      dw ?

msg_start   db "=== SIMPLE CALCULATOR ===",0Dh,0Ah,'$'
msg_num1    db "Enter first number: $"
msg_op      db 0Dh,0Ah,"Enter operation (+, -, *, /): $"
msg_num2    db 0Dh,0Ah,"Enter second number: $"
msg_res     db 0Dh,0Ah,"Result: $"
msg_error   db 0Dh,0Ah,"ERROR: Invalid input!",0Dh,0Ah,'$'

    .code

; ========================================
; StringToNumber
; ========================================
StringToNumber proc
    mov ax,0
    mov ch,0
    mov si,2
    
str_loop:
    cmp cx,0
    je str_done
    
    mov dl,[si]
    cmp dl,'0'
    jl str_error
    cmp dl,'9'
    jg str_error
    
    sub dl,'0'
    
    mov bx,ax
    mov ax,10
    imul bx
    mov bl,dl
    mov bh,0
    add ax,bx
    
    inc si
    dec cx
    jmp str_loop
    
str_done:
    ret
    
str_error:
    mov ax,-1
    ret
    
StringToNumber endp

; ========================================
; PerformOperation
; ========================================
PerformOperation proc
    mov dx,ax
    mov cl,operation
    
    cmp cl,'+'
    je op_add
    cmp cl,'-'
    je op_sub
    cmp cl,'*'
    je op_mul
    cmp cl,'/'
    je op_div
    
    mov dx,-1
    ret
    
op_add:
    add dx,bx
    ret
    
op_sub:
    sub dx,bx
    ret
    
op_mul:
    mov ax,dx
    imul bx
    mov dx,ax
    ret
    
op_div:
    cmp bx,0
    je op_div_err
    mov ax,dx
    cwd
    idiv bx
    mov dx,ax
    ret
    
op_div_err:
    mov dx,-1
    ret
    
PerformOperation endp

; ========================================
; NumberToString
; ========================================
NumberToString proc
    cmp dx,0
    jge num_pos
    
    mov ah,2
    mov dl,'-'
    int 21h
    
    neg dx
    
num_pos:
    mov ax,dx
    mov cx,0
    
num_extract:
    mov dx,0
    mov bx,10
    div bx
    
    push dx
    inc cx
    
    cmp ax,0
    jne num_extract
    
num_print:
    cmp cx,0
    je num_done
    
    pop dx
    add dl,'0'
    mov ah,2
    int 21h
    
    dec cx
    jmp num_print
    
num_done:
    ret
    
NumberToString endp

; ========================================
; MAIN
; ========================================
start:
    mov ax,@data
    mov ds,ax

    lea dx,msg_start
    mov ah,09
    int 21h

    lea dx,msg_num1
    mov ah,09
    int 21h

    lea dx,num1_str
    mov ah,0Ah
    int 21h

    lea dx,msg_op
    mov ah,09
    int 21h

    mov ah,01h
    int 21h
    mov operation,al

    lea dx,msg_num2
    mov ah,09
    int 21h

    lea dx,num2_str
    mov ah,0Ah
    int 21h

    ; Convert and calculate
    mov bx,offset num1_str
    mov cl,[num1_str+1]
    mov ch,0
    call StringToNumber
    mov num1,ax
    
    cmp ax,-1
    je error

    mov bx,offset num2_str
    mov cl,[num2_str+1]
    mov ch,0
    call StringToNumber
    mov num2,ax
    
    cmp ax,-1
    je error

    mov ax,num1
    mov bx,num2
    call PerformOperation
    mov result,dx

    lea dx,msg_res
    mov ah,09
    int 21h
    
    mov dx,result
    call NumberToString
    
    mov dl,0Dh
    mov ah,2
    int 21h
    mov dl,0Ah
    mov ah,2
    int 21h
    
    jmp exit_prog

error:
    lea dx,msg_error
    mov ah,09
    int 21h

exit_prog:
    mov ax,4C00h
    int 21h

    end start
