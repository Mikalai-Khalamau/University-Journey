; ============================================
; SORT MAIN DIAGONAL OF 3x3 MATRIX (DESCENDING)
; Main diagonal: matrix[0,0], matrix[1,1], matrix[2,2]
; ============================================

.MODEL small
.STACK 100h

.DATA
    matrix              dw 9 dup(?)         ; 3x3 matrix (9 words)
    input_buffer        db 16, 0, 16 dup(0)
    diagonal            dw 3 dup(?)         ; Store 3 diagonal elements
    
    msg_input           db 'Enter 9 numbers (3x3 matrix):', 0Dh, 0Ah, '$'
    msg_number          db 'Number: $'
    msg_matrix          db 0Dh, 0Ah, 'Original matrix:', 0Dh, 0Ah, '$'
    msg_diag_sorted     db 0Dh, 0Ah, 'Sorted diagonal:', 0Dh, 0Ah, '$'
    msg_result          db 0Dh, 0Ah, 'Result matrix:', 0Dh, 0Ah, '$'

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

; ===== Read number =====
; Output: AX = number
read_number proc
    print_string msg_number
    
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

; ===== Convert string to integer =====
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
    jne done_conv
    neg ax

done_conv:
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

    ; ===== STEP 1: Input 9 numbers =====
    print_string msg_input
    
    lea di, matrix
    mov cx, 9

input_loop:
    call read_number
    mov [di], ax
    add di, 2
    call print_newline
    loop input_loop

    ; ===== STEP 2: Display original matrix =====
    print_string msg_matrix
    
    lea si, matrix
    mov cx, 3
    
print_matrix_rows:
    mov bx, 0
    
print_matrix_cols:
    cmp bx, 3
    jge next_row
    
    mov ax, [si]
    call print_number
    
    mov ah, 02h
    mov dl, ' '
    int 21h
    
    add si, 2
    inc bx
    jmp print_matrix_cols
    
next_row:
    call print_newline
    loop print_matrix_rows

    ; ===== STEP 3: Extract diagonal =====
    ; diagonal[0] = matrix[0,0] = matrix[0]
    ; diagonal[1] = matrix[1,1] = matrix[4]
    ; diagonal[2] = matrix[2,2] = matrix[8]
    
    lea di, diagonal
    
    ; Get matrix[0,0]
    mov ax, word ptr [matrix + 0]
    mov [di], ax
    
    ; Get matrix[1,1] (offset = 1*3 + 1 = 4, * 2 = 8)
    mov ax, word ptr [matrix + 8]
    mov [di + 2], ax
    
    ; Get matrix[2,2] (offset = 2*3 + 2 = 8, * 2 = 16)
    mov ax, word ptr [matrix + 16]
    mov [di + 4], ax

    ; ===== STEP 4: Sort diagonal (descending) =====
    ; Bubble sort for 3 elements
    
    mov cx, 2               ; 2 passes (n-1)

sort_outer:
    cmp cx, 0
    jle sort_done
    
    lea si, diagonal
    mov bx, 2               ; 2 comparisons
    
sort_inner:
    cmp bx, 0
    jle sort_next
    
    mov ax, [si]
    mov dx, [si + 2]
    
    cmp ax, dx              ; For descending: if first < second
    jl swap_elements        ; swap
    
    jmp skip_swap
    
swap_elements:
    mov [si], dx            ; Swap first with second
    mov [si + 2], ax
    
skip_swap:
    add si, 2
    dec bx
    jmp sort_inner
    
sort_next:
    dec cx
    jmp sort_outer

sort_done:
    ; ===== STEP 5: Display sorted diagonal =====
    print_string msg_diag_sorted
    
    lea si, diagonal
    mov cx, 3
    
print_diag_loop:
    mov ax, [si]
    call print_number
    call print_newline
    
    add si, 2
    loop print_diag_loop

    ; ===== STEP 6: Put sorted diagonal back into matrix =====
    lea si, diagonal
    
    ; Put diagonal[0] -> matrix[0,0]
    mov ax, [si]
    mov word ptr [matrix + 0], ax
    
    ; Put diagonal[1] -> matrix[1,1]
    mov ax, [si + 2]
    mov word ptr [matrix + 8], ax
    
    ; Put diagonal[2] -> matrix[2,2]
    mov ax, [si + 4]
    mov word ptr [matrix + 16], ax

    ; ===== STEP 7: Display result matrix =====
    print_string msg_result
    
    lea si, matrix
    mov cx, 3
    
print_result_rows:
    mov bx, 0
    
print_result_cols:
    cmp bx, 3
    jge next_result_row
    
    mov ax, [si]
    call print_number
    
    mov ah, 02h
    mov dl, ' '
    int 21h
    
    add si, 2
    inc bx
    jmp print_result_cols
    
next_result_row:
    call print_newline
    loop print_result_rows

    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
