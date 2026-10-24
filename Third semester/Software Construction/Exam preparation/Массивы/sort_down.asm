; ============================================
; INSERTION SORT - 10 numbers (DESCENDING)
; Input: 10 signed integers (-32768..32767)
; Output: sorted array in descending order
; ============================================

.MODEL small
.STACK 100h

.DATA
    array               dw 10 dup(?)        ; Array of 10 signed integers

    ; DOS buffered input: [0]=maxlen, [1]=actual_len, [2..]=data
    input_buffer        db 16, 0, 16 dup(0)

    msg_input           db "Enter 10 numbers (each on new line):", 0Dh, 0Ah, '$'
    msg_output          db 0Dh, 0Ah, "Sorted array (descending):", 0Dh, 0Ah, '$'

.CODE

; ===== Print string ending with '$' =====
print_string macro message
    push ax
    push dx
    lea dx, message
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; ===== Print carriage return + line feed =====
print_newline proc
    push ax
    push dx
    mov ah, 02h
    mov dl, 0Dh             ; CR
    int 21h
    mov dl, 0Ah             ; LF
    int 21h
    pop dx
    pop ax
    ret
print_newline endp

; ===== Read number from keyboard =====
; Output: AX = signed 16-bit number
read_number proc
    push dx

    mov ah, 0Ah             ; DOS: buffered input
    lea dx, input_buffer
    int 21h

    ; Make null-terminated string
    mov bl, input_buffer[1]
    xor bh, bh
    mov byte ptr input_buffer[2+bx], 0

    lea si, input_buffer + 2
    call convert_string_to_int

    pop dx
    ret
read_number endp

; ===== Convert ASCII string to signed integer =====
; Input: SI = pointer to string
; Output: AX = signed integer
convert_string_to_int proc
    push bx
    push cx

    xor ax, ax              ; AX = result
    xor bx, bx              ; BL = sign flag

skip_whitespace:
    mov cl, [si]
    cmp cl, ' '
    je skip_next
    cmp cl, 09h             ; Tab
    je skip_next
    jmp check_minus_sign
skip_next:
    inc si
    jmp skip_whitespace

check_minus_sign:
    mov cl, [si]
    cmp cl, '-'
    jne parse_digits
    mov bl, 1               ; Set negative flag
    inc si

parse_digits:
    mov cl, [si]
    cmp cl, 0               ; End of string?
    je apply_negative_sign

    sub cl, '0'             ; Convert ASCII to digit
    mov bx, 10
    mul bx                  ; AX = AX * 10
    xor ch, ch
    add ax, cx              ; AX += digit

    inc si
    jmp parse_digits

apply_negative_sign:
    cmp bl, 1
    jne conversion_done
    neg ax
conversion_done:
    pop cx
    pop bx
    ret
convert_string_to_int endp

; ===== Print signed number in AX =====
print_number proc
    push ax
    push bx
    push cx
    push dx

    ; Handle negative numbers
    cmp ax, 0
    jge print_absolute
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax

print_absolute:
    ; Handle zero
    cmp ax, 0
    jne convert_to_digits
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp done_printing

convert_to_digits:
    xor cx, cx              ; CX = digit counter
    mov bx, 10
divide_by_10:
    xor dx, dx
    div bx                  ; AX / 10, remainder in DX
    push dx                 ; Save digit
    inc cx
    cmp ax, 0
    jne divide_by_10

print_digit_stack:
    pop dx
    add dl, '0'             ; Convert to ASCII
    mov ah, 02h
    int 21h
    loop print_digit_stack

done_printing:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number endp

; ============================================
; MAIN PROGRAM
; ============================================
main proc
    mov ax, @data
    mov ds, ax

    ; === STEP 1: Read 10 numbers ===
    print_string msg_input

    lea di, array
    mov cx, 10
read_array_loop:
    call read_number
    mov [di], ax
    add di, 2               ; Next word (2 bytes)
    call print_newline
    loop read_array_loop

    ; === STEP 2: Insertion Sort (Descending) ===
    mov cx, 1               ; i = 1 (start from second element)

outer_sort_loop:
    cmp cx, 10
    jge sort_finished

    ; Load key = array[i]
    mov si, cx
    shl si, 1               ; offset = i * 2
    mov ax, [array + si]    ; AX = key

    ; j = i - 1
    mov si, cx
    dec si                  ; j = i - 1

inner_compare_loop:
    cmp si, 0               ; j < 0?
    jl insert_key_position

    ; Load array[j]
    mov bx, si
    shl bx, 1
    mov dx, [array + bx]    ; DX = array[j]

    ; For DESCENDING: if array[j] < key, stop shifting
    cmp dx, ax
    jg insert_key_position

    ; Shift right: array[j+1] = array[j]
    mov di, si
    inc di
    mov bx, di
    shl bx, 1
    mov [array + bx], dx

    dec si
    jmp inner_compare_loop

insert_key_position:
    ; Place key at correct position: array[j+1] = key
    inc si
    mov bx, si
    shl bx, 1
    mov [array + bx], ax

    inc cx
    jmp outer_sort_loop

sort_finished:
    ; === STEP 3: Output sorted array ===
    print_string msg_output

    lea si, array
    mov cx, 10
output_array_loop:
    mov ax, [si]
    call print_number
    call print_newline
    add si, 2
    loop output_array_loop

    ; === Exit ===
    mov ax, 4C00h
    int 21h
main endp

END main
