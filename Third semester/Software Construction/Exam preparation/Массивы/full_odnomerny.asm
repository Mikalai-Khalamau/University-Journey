.MODEL small
.STACK 100h

.DATA
    array           dw 5 dup(?)         ; Array of 5 words
    input_buffer    db 16, 0, 16 dup(0) ; DOS input buffer
    header_msg      db 'Enter 5 numbers:', 0Dh, 0Ah, '$'
    prompt_msg      db 'Number: $'

.CODE

; ===== PRINT STRING =====
; Macro to print string at address in DX
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
; Print CR (carriage return) and LF (line feed)
print_crlf proc
    push ax
    push dx
    mov ah, 02h         ; DOS function: print character
    mov dl, 0Dh         ; CR
    int 21h
    mov dl, 0Ah         ; LF
    int 21h
    pop dx
    pop ax
    ret
print_crlf endp

; ===== READ NUMBER FROM KEYBOARD =====
; Output: AX = the number read
read_num proc
    print_str prompt_msg
    
    push dx
    mov ah, 0Ah         ; DOS function: read string
    lea dx, input_buffer
    int 21h
    
    ; Convert to null-terminated string
    mov bl, input_buffer[1]  ; BL = actual length typed
    xor bh, bh               ; Clear BH
    mov byte ptr input_buffer[2+bx], 0  ; Add null terminator
    
    lea si, input_buffer + 2  ; SI points to string start
    call ascii_to_int
    pop dx
    ret
read_num endp

; ===== CONVERT ASCII STRING TO INTEGER =====
; Input: SI = pointer to string
; Output: AX = integer value
ascii_to_int proc
    push bx
    push cx
    
    xor ax, ax
    xor bx, bx             ; BL = sign flag
    
    ; Skip whitespace
skip_whitespace:
    mov cl, [si]
    cmp cl, ' '
    je ws_next
    cmp cl, 09h            ; Tab
    je ws_next
    jmp check_minus
ws_next:
    inc si
    jmp skip_whitespace
    
    ; Check for minus sign
check_minus:
    mov cl, [si]
    cmp cl, '-'
    jne parse_digits
    mov bl, 1              ; Set sign flag
    inc si
    
    ; Parse digits: AX = AX*10 + digit
parse_digits:
    mov cl, [si]
    cmp cl, 0              ; End of string?
    je apply_sign
    
    sub cl, '0'            ; Convert ASCII to digit
    mov bx, 10
    mul bx                 ; AX = AX * 10
    xor ch, ch
    add ax, cx             ; AX = AX + digit
    inc si
    jmp parse_digits
    
    ; Apply sign if negative
apply_sign:
    cmp bl, 1
    jne finish
    neg ax
finish:
    pop cx
    pop bx
    ret
ascii_to_int endp

; ===== PRINT SIGNED NUMBER =====
; Input: AX = number to print
print_num proc
    push ax
    push bx
    push cx
    push dx
    
    ; Print minus if negative
    cmp ax, 0
    jge positive
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax
    
positive:
    ; Handle zero case
    cmp ax, 0
    jne extract_digits
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp end_print
    
    ; Extract digits and put on stack
extract_digits:
    xor cx, cx
    mov bx, 10
digit_loop:
    xor dx, dx
    div bx                 ; AX / 10: quotient in AX, remainder in DX
    push dx                ; Push digit to stack
    inc cx                 ; Increment digit count
    cmp ax, 0
    jne digit_loop
    
    ; Print digits (pop from stack in reverse order)
print_all_digits:
    pop dx
    add dl, '0'            ; Convert digit to ASCII
    mov ah, 02h
    int 21h
    loop print_all_digits
    
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
    
    ; Print header message
    print_str header_msg
    call print_crlf
    
    ; ===== INPUT LOOP: Read 5 numbers =====
    lea di, array          ; DI = pointer to array start
    mov cx, 5              ; CX = counter (5 iterations)
input_loop:
    call read_num          ; Read number -> AX
    mov [di], ax           ; Store AX into memory at DI
    add di, 2              ; Move pointer to next word (2 bytes)
    call print_crlf
    loop input_loop
    
    ; ===== OUTPUT LOOP: Print 5 numbers =====
    lea si, array          ; SI = pointer to array start
    mov cx, 5              ; CX = counter (5 iterations)
output_loop:
    mov ax, [si]           ; Load word from memory at SI into AX
    call print_num         ; Print AX
    call print_crlf
    add si, 2              ; Move pointer to next word (2 bytes)
    loop output_loop
    
    ; ===== EXIT =====
    mov ax, 4C00h
    int 21h

END start
