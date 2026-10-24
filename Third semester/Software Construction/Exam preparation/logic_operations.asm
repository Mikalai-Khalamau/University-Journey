; ============================================
; BIT OPERATIONS: OR, XOR, AND with user choice
; User selects operation and inputs 2 numbers
; ============================================

.MODEL small
.STACK 100h

.DATA
    input_buffer        db 16, 0, 16 dup(0)
    
    msg_menu            db 0Dh, 0Ah, '=== BIT OPERATIONS ===', 0Dh, 0Ah
                        db '1. OR', 0Dh, 0Ah
                        db '2. XOR', 0Dh, 0Ah
                        db '3. AND', 0Dh, 0Ah
                        db 'Choose (1-3): $'
    
    msg_first_num       db 'Enter first number: $'
    msg_second_num      db 'Enter second number: $'
    msg_result          db 0Dh, 0Ah, 'Result: $'
    
    choice              db 0
    first_number        dw 0
    second_number       dw 0
    result_value        dw 0

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
string_to_integer endp

; ===== Print number =====
; Input: AX = number
print_number proc
    push ax
    push bx
    push cx
    push dx

    cmp ax, 0
    jge print_abs
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax

print_abs:
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

    ; ===== STEP 1: Show menu and get choice =====
    print_string msg_menu
    call read_number        ; AX = choice (1-3)
    mov choice, al

    ; ===== STEP 2: Input first number =====
    print_string msg_first_num
    call read_number
    mov first_number, ax

    ; ===== STEP 3: Input second number =====
    print_string msg_second_num
    call read_number
    mov second_number, ax

    ; ===== STEP 4: Perform operation =====
    mov al, choice

    ; Check which operation
    cmp al, '1'             ; OR?
    je do_or

    cmp al, '2'             ; XOR?
    je do_xor

    cmp al, '3'             ; AND?
    je do_and

    ; Invalid choice
    jmp show_result

    ; ===== OPERATION 1: OR =====
do_or:
    mov ax, first_number
    mov bx, second_number
    or ax, bx               ; AX = first OR second
    mov result_value, ax
    jmp show_result

    ; ===== OPERATION 2: XOR =====
do_xor:
    mov ax, first_number
    mov bx, second_number
    xor ax, bx              ; AX = first XOR second
    mov result_value, ax
    jmp show_result

    ; ===== OPERATION 3: AND =====
do_and:
    mov ax, first_number
    mov bx, second_number
    and ax, bx              ; AX = first AND second
    mov result_value, ax

    ; ===== STEP 5: Print result =====
show_result:
    print_string msg_result
    mov ax, result_value
    call print_number
    call print_newline

    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
