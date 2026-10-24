.MODEL small
.STACK 100h

.DATA
    ; ===== DATA SECTION =====
    matrix          dw 9 dup(?)          ; Matrix 3x3 (9 elements)
    row_averages    dw 3 dup(?)          ; Average for each row (3 results)
    input_buffer    db 16, 0, 16 dup(0)  ; DOS input buffer
    
    msg_input       db 'Enter 9 numbers (3x3 matrix):', 0Dh, 0Ah, '$'
    msg_prompt      db 'Number: $'
    msg_output      db 0Dh, 0Ah, 'Row averages:', 0Dh, 0Ah, '$'

.CODE

; ===== MACRO: Print string =====
print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h         ; DOS function: print string
    int 21h
    pop dx
    pop ax
endm

; ===== PRINT NEWLINE =====
print_newline proc
    push ax
    push dx
    mov ah, 02h
    mov dl, 0Dh         ; Carriage Return
    int 21h
    mov dl, 0Ah         ; Line Feed
    int 21h
    pop dx
    pop ax
    ret
print_newline endp

; ===== READ NUMBER FROM KEYBOARD =====
; Output: AX = number
read_number proc
    print_str msg_prompt
    
    push dx
    mov ah, 0Ah                     ; DOS function: read string
    lea dx, input_buffer
    int 21h
    
    ; Add null terminator to string
    mov bl, input_buffer[1]         ; BL = actual length
    xor bh, bh
    mov byte ptr input_buffer[2+bx], 0
    
    lea si, input_buffer + 2
    call string_to_int
    pop dx
    ret
read_number endp

; ===== CONVERT STRING TO INTEGER =====
; Input: SI = pointer to string
; Output: AX = integer
string_to_int proc
    push bx
    push cx
    
    xor ax, ax                      ; AX = 0 (result)
    xor bx, bx                      ; BL = sign flag
    
    ; Skip whitespace
skip_space:
    mov cl, [si]
    cmp cl, ' '
    je next_char
    cmp cl, 09h                     ; Tab
    je next_char
    jmp check_sign
next_char:
    inc si
    jmp skip_space
    
    ; Check for minus sign
check_sign:
    mov cl, [si]
    cmp cl, '-'
    jne parse_loop
    mov bl, 1                       ; Set sign flag
    inc si
    
    ; Parse digits
parse_loop:
    mov cl, [si]
    cmp cl, 0                       ; End of string?
    je apply_sign
    
    sub cl, '0'                     ; Convert ASCII to digit
    mov bx, 10
    mul bx                          ; AX = AX * 10
    xor ch, ch
    add ax, cx                      ; AX = AX + digit
    inc si
    jmp parse_loop
    
    ; Apply sign if negative
apply_sign:
    cmp bl, 1
    jne done
    neg ax
done:
    pop cx
    pop bx
    ret
string_to_int endp

; ===== PRINT SIGNED NUMBER =====
; Input: AX = number to print
print_number proc
    push ax
    push bx
    push cx
    push dx
    
    ; Handle negative numbers
    cmp ax, 0
    jge positive
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax
    
positive:
    ; Handle zero
    cmp ax, 0
    jne extract_digits
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp finish_print
    
    ; Extract digits (push to stack)
extract_digits:
    xor cx, cx                      ; CX = digit counter
    mov bx, 10
    
digit_loop:
    xor dx, dx
    div bx                          ; AX / 10, quotient in AX, remainder in DX
    push dx                         ; Push digit to stack
    inc cx
    cmp ax, 0
    jne digit_loop
    
    ; Print digits (pop from stack)
print_digits:
    pop dx
    add dl, '0'                     ; Convert to ASCII
    mov ah, 02h
    int 21h
    loop print_digits
    
finish_print:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number endp

; ===== MAIN PROGRAM =====
start:
    mov ax, @data
    mov ds, ax
    
    ; ===== STEP 1: INPUT (read 9 numbers) =====
    print_str msg_input
    call print_newline
    
    lea di, matrix                  ; DI = pointer to matrix
    mov cx, 9                       ; CX = 9 elements
    
input_loop:
    call read_number                ; Read number -> AX
    mov [di], ax                    ; Store in matrix
    add di, 2                       ; Move to next element (word = 2 bytes)
    call print_newline
    loop input_loop
    
    ; ===== STEP 2: PROCESS (calculate row averages) =====
    lea si, matrix                  ; SI = pointer to matrix
    lea di, row_averages            ; DI = pointer to results
    mov cx, 3                       ; CX = 3 rows
    
row_loop:
    ; Calculate sum of 3 elements in current row
    mov ax, [si]                    ; AX = element[0]
    add ax, [si+2]                  ; AX += element[1]
    add ax, [si+4]                  ; AX += element[2]
    
    ; Divide sum by 3 to get average
    mov bx, 3
    cwd                             ; Extend AX to DX:AX (for signed division)
    idiv bx                         ; AX = AX / 3 (signed division)
    
    mov [di], ax                    ; Store average
    add di, 2                       ; Move to next result
    add si, 6                       ; Move to next row (3 elements * 2 bytes = 6)
    
    loop row_loop
    
    ; ===== STEP 3: OUTPUT (print averages) =====
    print_str msg_output
    
    lea si, row_averages            ; SI = pointer to results
    mov cx, 3                       ; 3 rows
    
output_loop:
    mov ax, [si]                    ; Load average
    call print_number               ; Print average
    call print_newline
    add si, 2                       ; Move to next average
    loop output_loop
    
    ; ===== EXIT =====
    mov ax, 4C00h
    int 21h

END start
