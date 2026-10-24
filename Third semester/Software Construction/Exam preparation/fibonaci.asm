; ============================================
; FIBONACCI SEQUENCE
; Input: N (number of Fibonacci numbers)
; Output: First N Fibonacci numbers
; ============================================

.MODEL small
.STACK 100h

.DATA
    input_buffer        db 16, 0, 16 dup(0)
    msg_input           db 'Enter N (how many Fibonacci numbers): $'
    msg_result          db 0Dh, 0Ah, 'Fibonacci sequence:', 0Dh, 0Ah, '$'
    
    fibonacci_array     dw 100 dup(?)       ; Store up to 100 Fibonacci numbers
    count               dw 0                ; Counter for how many to generate

.CODE

; ===== Print string =====
print_string macro message
    push ax
    push dx
    lea dx, message
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; ===== Print newline =====
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

; ===== Read number from keyboard =====
; Output: AX = number
read_number proc
    push dx

    mov ah, 0Ah
    lea dx, input_buffer
    int 21h

    ; Convert to null-terminated string
    mov bl, input_buffer[1]
    xor bh, bh
    mov byte ptr input_buffer[2+bx], 0

    lea si, input_buffer + 2
    call string_to_integer

    pop dx
    ret
read_number endp

; ===== Convert ASCII string to integer =====
; Input: SI = pointer to string
; Output: AX = integer
string_to_integer proc
    push bx
    push cx

    xor ax, ax              ; AX = result
    xor bx, bx              ; BL = sign flag

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
string_to_integer endp

; ===== Print number =====
; Input: AX = number
print_number proc
    push ax
    push bx
    push cx
    push dx

    ; Handle negative
    cmp ax, 0
    jge print_abs
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax

print_abs:
    ; Handle zero
    cmp ax, 0
    jne extract_digits
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp end_print_num

extract_digits:
    xor cx, cx
    mov bx, 10

digit_loop:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne digit_loop

print_digit_stack:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop print_digit_stack

end_print_num:
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
    print_string msg_input
    call print_newline
    
    call read_number        ; AX = N
    mov count, ax           ; Store N

    ; ===== STEP 2: Generate Fibonacci sequence =====
    lea di, fibonacci_array

    ; Handle N = 0
    cmp ax, 0
    jle print_result

    ; Handle N = 1: F(1) = 0
    cmp ax, 1
    jl print_result
    
    mov word ptr [di], 0    ; fib[0] = 0
    add di, 2
    
    ; Handle N = 2: F(2) = 1
    cmp ax, 2
    jl print_result
    
    mov word ptr [di], 1    ; fib[1] = 1
    add di, 2

    ; Generate F(n) = F(n-1) + F(n-2) for n >= 3
    mov cx, ax              ; CX = N
    sub cx, 2               ; CX = N - 2 (remaining iterations)

fib_generate_loop:
    cmp cx, 0
    jle print_result

    ; Load fib[i-2]
    mov si, di
    sub si, 4               ; Si points to fib[i-2]
    mov ax, word ptr [si]   ; AX = fib[i-2]

    ; Load fib[i-1]
    mov si, di
    sub si, 2               ; SI points to fib[i-1]
    mov bx, word ptr [si]   ; BX = fib[i-1]

    ; Calculate fib[i] = fib[i-1] + fib[i-2]
    add ax, bx              ; AX = fib[i]

    ; Store fib[i]
    mov word ptr [di], ax
    add di, 2

    dec cx
    jmp fib_generate_loop

    ; ===== STEP 3: Output Fibonacci sequence =====
print_result:
    print_string msg_result

    lea si, fibonacci_array
    mov cx, count           ; CX = N

output_loop:
    cmp cx, 0
    jle done

    mov ax, [si]
    call print_number
    call print_newline

    add si, 2
    dec cx
    jmp output_loop

done:
    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
