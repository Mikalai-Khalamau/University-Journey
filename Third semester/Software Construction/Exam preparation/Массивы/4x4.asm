.MODEL small
.STACK 100h

.DATA
    arr     dw 16 dup(?)        
    inbuf   db 16,0, 16 dup(0)
    msg1    db 'Enter 16 numbers:',0Dh,0Ah,'$'
    msg_num db 'Number: $'

.CODE

; Print string at DX
print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; Print newline (CR LF)
print_crlf proc
    push ax
    push dx
    mov ah, 02h
    mov dl, 0Dh
    int 21h
    mov dl, 0Ah
    int 21h
    pop dx
    pop ax
    ret
print_crlf endp

; Read number from keyboard into AX
read_num proc
    print_str msg_num
    
    push dx
    mov ah, 0Ah
    lea dx, inbuf
    int 21h
    
    mov bl, inbuf[1]
    xor bh, bh
    mov byte ptr inbuf[2+bx], 0
    
    lea si, inbuf+2
    call atoi
    pop dx
    ret
read_num endp

; Convert ASCIIZ string at DS:SI to signed number in AX
atoi proc
    push bx
    push cx
    
    xor ax, ax
    xor bx, bx
    
skip_ws:
    mov cl, [si]
    cmp cl, ' '
    je ws_next
    cmp cl, 09h
    je ws_next
    jmp chk_minus
ws_next:
    inc si
    jmp skip_ws
    
chk_minus:
    mov cl, [si]
    cmp cl, '-'
    jne parse
    mov bl, 1
    inc si
    
parse:
    mov cl, [si]
    cmp cl, 0
    je finish
    
    sub cl, '0'
    mov bx, 10
    mul bx
    xor ch, ch
    add ax, cx
    inc si
    jmp parse
    
finish:
    cmp bl, 1
    jne done
    neg ax
done:
    pop cx
    pop bx
    ret
atoi endp

; Print signed number from AX
print_num proc
    push ax
    push bx
    push cx
    push dx
    
    cmp ax, 0
    jge pos
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax
    
pos:
    cmp ax, 0
    jne digits
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp end_print
    
digits:
    xor cx, cx
    mov bx, 10
div_loop:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne div_loop
    
print_digits:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop print_digits
    
end_print:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_num endp

; Main program
start:
    mov ax, @data
    mov ds, ax
    
    ; Print header
    print_str msg1
    call print_crlf
    
    ; ===== INPUT: 16 numbers =====
    lea di, arr
    mov cx, 16
inp_loop:
    call read_num
    mov [di], ax
    add di, 2
    call print_crlf
    loop inp_loop
    
    call print_crlf
    
    ; ===== OUTPUT: print as 4x4 matrix =====
    lea si, arr
    mov bx, 0                ; BX = element counter
    
out_loop:
    mov ax, [si]
    call print_num
    
    ; print space separator
    mov ah, 02h
    mov dl, ' '
    int 21h
    
    add si, 2
    inc bx
    
    ; Every 4 elements -> new line
    mov ax, bx
    and ax, 3                ; BX mod 4
    cmp ax, 0
    jne skip_nl
    call print_crlf          ; new line after 4 elements
    
skip_nl:
    cmp bx, 16
    jl out_loop
    
    ; Exit
    mov ax, 4C00h
    int 21h

END start
