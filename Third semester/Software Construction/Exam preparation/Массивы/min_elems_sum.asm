.MODEL small
.STACK 100h

.DATA
    matrix          dw 9 dup(?)         ; Matrix 3x3 (9 elements)
    min_elements    dw 3 dup(?)         ; Minimum of each row (3 results)
    inbuf           db 16, 0, 16 dup(0)
    msg_input       db 'Enter 9 numbers (3x3 matrix):', 0Dh, 0Ah, '$'
    msg_num         db 'Number: $'
    msg_result      db 0Dh, 0Ah, 'Minimum elements:', 0Dh, 0Ah, '$'
    msg_sum         db 0Dh, 0Ah, 'Sum of minimums: $'

.CODE

; ===== Print string =====
print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; ===== Print newline =====
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

; ===== Read number =====
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

; ===== String to integer =====
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

; ===== Print number =====
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

; ===== MAIN PROGRAM =====
start:
    mov ax, @data
    mov ds, ax
    
    ; ===== INPUT: 9 numbers =====
    print_str msg_input
    call print_crlf
    
    lea di, matrix
    mov cx, 9
inp_loop:
    call read_num
    mov [di], ax
    add di, 2
    call print_crlf
    loop inp_loop
    
    ; ===== PROCESS: Find minimum of each row =====
    lea si, matrix
    lea di, min_elements
    mov cx, 3                   ; 3 rows
    
row_loop:
    cmp cx, 0
    je calc_sum
    
    ; Load first element as minimum
    mov ax, [si]                ; AX = first element (minimum initially)
    
    ; Compare with second element
    mov bx, [si+2]              ; BX = second element
    cmp ax, bx
    jle skip_min1
    mov ax, bx                  ; AX = min(ax, bx)
    
skip_min1:
    ; Compare with third element
    mov bx, [si+4]              ; BX = third element
    cmp ax, bx
    jle skip_min2
    mov ax, bx                  ; AX = min(ax, bx)
    
skip_min2:
    ; Store minimum of row
    mov [di], ax
    add di, 2
    add si, 6                   ; Move to next row (3 elements * 2 bytes)
    
    dec cx
    jmp row_loop
    
    ; ===== CALCULATE SUM OF MINIMUMS =====
calc_sum:
    lea si, min_elements
    xor ax, ax                  ; AX = sum
    mov cx, 3
    
sum_loop:
    cmp cx, 0
    je print_results
    
    add ax, [si]
    add si, 2
    dec cx
    jmp sum_loop
    
    ; ===== OUTPUT: Print minimums =====
print_results:
    print_str msg_result
    
    lea si, min_elements
    mov cx, 3
    
print_min_loop:
    cmp cx, 0
    je print_final_sum
    
    mov ax, [si]
    call print_num
    call print_crlf
    
    add si, 2
    dec cx
    jmp print_min_loop
    
    ; ===== OUTPUT: Print sum =====
print_final_sum:
    lea si, min_elements
    xor ax, ax
    mov cx, 3
    
sum_final_loop:
    cmp cx, 0
    je print_sum
    
    add ax, [si]
    add si, 2
    dec cx
    jmp sum_final_loop
    
print_sum:
    print_str msg_sum
    call print_num
    call print_crlf
    
    ; ===== EXIT =====
    mov ax, 4C00h
    int 21h

END start
