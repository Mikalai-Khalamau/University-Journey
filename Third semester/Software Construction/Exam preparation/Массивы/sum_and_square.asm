; ============================================
; ARRAY OPERATIONS
; Input: 10 numbers
; Output: Each number with:
;   - Number itself
;   - Number + Number (doubled)
;   - Number * Number (squared)
; ============================================

.MODEL small
.STACK 100h

.DATA
    array               dw 10 dup(?)        ; Array of 10 numbers
    input_buffer        db 16, 0, 16 dup(0) ; DOS input buffer
    
    msg_input           db 'Enter 10 numbers:', 0Dh, 0Ah, '$'
    msg_number          db 'Number: $'
    msg_output          db 0Dh, 0Ah, 'Results:', 0Dh, 0Ah, '$'
    msg_original        db 'Original: $'
    msg_sum             db ', Sum (n+n): $'
    msg_square          db ', Square (n*n): $'

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

; ===== Read number from keyboard =====
; Output: AX = number
read_number proc
    print_str msg_number
    
    push dx
    mov ah, 0Ah
    lea dx, input_buffer
    int 21h
    
    mov bl, input_buffer[1]
    xor bh, bh
    mov byte ptr input_buffer[2+bx], 0
    
    lea si, input_buffer + 2
    call string_to_int
    pop dx
    ret
read_number endp

; ===== Convert ASCII string to integer =====
; Input: SI = pointer to string
; Output: AX = integer
string_to_int proc
    push bx
    push cx
    
    xor ax, ax
    xor bx, bx
    
skip_spaces:
    mov cl, [si]
    cmp cl, ' '
    je next_space
    cmp cl, 09h
    je next_space
    jmp check_sign
next_space:
    inc si
    jmp skip_spaces
    
check_sign:
    mov cl, [si]
    cmp cl, '-'
    jne parse_digits
    mov bl, 1
    inc si
    
parse_digits:
    mov cl, [si]
    cmp cl, 0
    je apply_sign
    
    sub cl, '0'
    mov bx, 10
    mul bx
    xor ch, ch
    add ax, cx
    
    inc si
    jmp parse_digits
    
apply_sign:
    cmp bl, 1
    jne conv_done
    neg ax
    
conv_done:
    pop cx
    pop bx
    ret
string_to_int endp

; ===== Print number =====
; Input: AX = number
print_number proc
    push ax
    push bx
    push cx
    push dx
    
    cmp ax, 0
    jge print_pos
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax
    
print_pos:
    cmp ax, 0
    jne extract_dig
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp end_print
    
extract_dig:
    xor cx, cx
    mov bx, 10
    
dig_loop:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne dig_loop
    
print_dig_stack:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop print_dig_stack
    
end_print:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number endp

; ============================================
; MAIN PROGRAM
; ============================================
start:
    mov ax, @data
    mov ds, ax
    
    ; ===== STEP 1: Input 10 numbers =====
    print_str msg_input
    
    lea di, array
    mov cx, 10
    
input_loop:
    call read_number        ; Read number -> AX
    mov [di], ax            ; Store in array
    add di, 2
    call print_crlf
    loop input_loop
    
    ; ===== STEP 2: Output with operations =====
    print_str msg_output
    
    lea si, array
    mov cx, 10
    
output_loop:
    cmp cx, 0
    jle done
    
    ; Load number
    mov ax, [si]            ; AX = original number
    
    ; Print original
    print_str msg_original
    call print_number
    
    ; Calculate sum (n + n)
    mov bx, ax              ; BX = n
    add ax, bx              ; AX = n + n
    
    ; Print sum
    print_str msg_sum
    call print_number
    
    ; Calculate square (n * n)
    mov ax, [si]            ; AX = original number (reload)
    mov bx, ax              ; BX = n
    imul bx                 ; AX = n * n (AX = AX * BX)
    
    ; Print square
    print_str msg_square
    call print_number
    
    ; New line
    call print_crlf
    
    add si, 2
    dec cx
    jmp output_loop
    
done:
    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
