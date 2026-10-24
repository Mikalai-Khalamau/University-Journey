; ============================================
; FACTORIAL CALCULATION
; Input: N (number)
; Output: N! (factorial)
; ============================================

.MODEL small
.STACK 100h

.DATA
    input_buffer        db 16, 0, 16 dup(0)
    msg_input           db 'Enter N (calculate N!): $'
    msg_result          db 0Dh, 0Ah, 'Factorial: $'

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

    ; ===== STEP 1: Input N =====
    print_str msg_input
    call print_crlf
    
    call read_number        ; AX = N
    mov cx, ax              ; CX = N (счётчик для цикла)

    ; ===== STEP 2: Calculate factorial =====
    ; N! = 1 * 2 * 3 * ... * N
    
    mov ax, 1               ; AX = результат (начало с 1)
    
    ; Handle N = 0 or N = 1 (factorial = 1)
    cmp cx, 1
    jle print_result
    
    ; Multiply: AX = AX * 2 * 3 * ... * N
    mov bx, 2               ; BX = множитель (начинаем с 2)
    
factorial_loop:
    cmp bx, cx              ; BX > N?
    jg print_result         ; Да > выход
    
    imul bx                 ; AX = AX * BX
    inc bx                  ; BX++
    jmp factorial_loop

    ; ===== STEP 3: Output result =====
print_result:
    print_str msg_result
    call print_number
    call print_crlf

    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
