.MODEL small
.STACK 100h

.DATA
    msg_rows        db 'Enter rows: $'
    msg_cols        db 'Enter columns: $'
    msg_input       db 'Number: $'
    msg_row_sum     db 0Dh, 0Ah, 'Row sums:', 0Dh, 0Ah, '$'
    msg_col_sum     db 0Dh, 0Ah, 'Column sums:', 0Dh, 0Ah, '$'
    newline         db 0Dh, 0Ah, '$'
    
    input_buf       db 16, 0, 16 dup(0)
    matrix          dw 100 dup(0)
    row_sums        dw 10 dup(0)
    col_sums        dw 10 dup(0)
    num_rows        db 0
    num_cols        db 0
    col_count       db 0

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
    
    ; ===== READ ROWS =====
    print_str msg_rows
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
    mov num_rows, al
    
    ; ===== READ COLUMNS =====
    print_str msg_cols
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
    mov num_cols, al
    
    ; ===== INPUT MATRIX =====
    lea di, matrix
    mov cx, 0
    mov cl, num_rows
    
row_loop:
    cmp cl, 0
    je calc_sums
    
    mov bx, 0
    mov bl, num_cols
    
col_loop:
    cmp bl, 0
    je next_row_input
    
    call read_number
    mov [di], ax
    add di, 2
    call print_newline
    
    dec bl
    jmp col_loop
    
next_row_input:
    dec cl
    jmp row_loop
    
    ; ===== CALCULATE ROW SUMS =====
calc_sums:
    lea si, matrix
    lea di, row_sums
    mov cx, 0
    mov cl, num_rows
    
calc_row_loop:
    cmp cl, 0
    je calc_col_sums
    
    xor ax, ax
    mov bx, 0
    mov bl, num_cols
    
row_sum_loop:
    cmp bx, 0
    je row_sum_done
    
    add ax, [si]
    add si, 2
    dec bx
    jmp row_sum_loop
    
row_sum_done:
    mov [di], ax
    add di, 2
    dec cl
    jmp calc_row_loop
    
    ; ===== CALCULATE COLUMN SUMS =====
calc_col_sums:
    mov cx, 0
    mov cl, num_cols
    
col_sum_loop:
    cmp cl, 0
    je print_results
    
    lea si, matrix
    
    mov dx, 0
    mov dl, num_cols
    sub dl, cl
    mov ax, 0
    mov al, dl
    shl ax, 1
    add si, ax
    
    xor ax, ax
    mov bx, 0
    mov bl, num_rows
    
inner_col_loop:
    cmp bx, 0
    je col_sum_done
    
    add ax, [si]
    mov dx, 0
    mov dl, num_cols
    shl dx, 1
    add si, dx
    
    dec bx
    jmp inner_col_loop
    
col_sum_done:
    lea di, col_sums
    mov dx, 0
    mov dl, num_cols
    sub dl, cl
    mov bx, 0
    mov bl, dl
    shl bx, 1
    add di, bx
    mov [di], ax
    
    dec cl
    jmp col_sum_loop
    
    ; ===== PRINT RESULTS =====
print_results:
    print_str msg_row_sum
    
    lea si, row_sums
    mov cx, 0
    mov cl, num_rows
    
print_row_loop:
    cmp cx, 0
    je print_col_loop
    
    mov ax, [si]
    call print_number
    call print_newline
    
    add si, 2
    dec cx
    jmp print_row_loop
    
print_col_loop:
    print_str msg_col_sum
    
    lea si, col_sums
    mov cx, 0
    mov cl, num_cols
    
print_col_sums:
    cmp cx, 0
    je end_prog
    
    mov ax, [si]
    call print_number
    call print_newline
    
    add si, 2
    dec cx
    jmp print_col_sums
    
end_prog:
    mov ax, 4C00h
    int 21h

END start
