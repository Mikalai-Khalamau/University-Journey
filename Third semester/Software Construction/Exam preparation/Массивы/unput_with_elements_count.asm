.MODEL small
.STACK 100h

.DATA
    msg_count       db 'Enter count of elements: $'
    msg_input       db 'Number: $'
    newline         db 0Dh, 0Ah, '$'
    
    input_buf       db 16, 0, 16 dup(0)
    array           dw 30 dup(0)
    array_count     db 0

.CODE

print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

print_newline proc
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
print_newline endp

read_number proc
    print_str msg_input
    
    push dx
    mov ah, 0Ah
    lea dx, input_buf
    int 21h
    
    mov bl, input_buf[1]
    xor bh, bh
    mov byte ptr input_buf[2+bx], 0
    
    lea si, input_buf+2
    call atoi
    pop dx
    ret
read_number endp

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

print_number proc
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
print_number endp

start:
    mov ax, @data
    mov ds, ax
    
    ; ===== STEP 1: READ COUNT =====
    print_str msg_count
    call print_newline
    
    mov ah, 0Ah
    lea dx, input_buf
    int 21h
    call print_newline
    
    mov bl, input_buf[1]
    xor bh, bh
    mov byte ptr input_buf[2+bx], 0
    lea si, input_buf+2
    call atoi
    
    mov array_count, al
    
    ; ===== STEP 2: INPUT ARRAY =====
    lea di, array
    mov cx, 0
    mov cl, array_count
    
input_loop:
    cmp cx, 0
    je output_array
    
    call read_number
    mov [di], ax
    add di, 2
    call print_newline
    
    dec cx
    jmp input_loop
    
    ; ===== STEP 3: OUTPUT ARRAY =====
output_array:
    lea si, array
    mov cx, 0
    mov cl, array_count
    
output_loop:
    cmp cx, 0
    je end_prog
    
    mov ax, [si]
    call print_number
    call print_newline
    
    add si, 2
    dec cx
    jmp output_loop
    
end_prog:
    mov ax, 4C00h
    int 21h

END start
