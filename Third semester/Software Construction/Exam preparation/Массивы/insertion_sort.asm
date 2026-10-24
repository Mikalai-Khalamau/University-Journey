; Insertion Sort (algorithm unchanged)
; Input: 10 integer numbers, each entered on a separate line (Enter)
; Output: sorted array (one number per line)
; Note: numbers must fit into signed 16-bit (-32768..32767)

.MODEL small
.STACK 100h

.DATA
array           dw 10 dup(?)              ; 10 numbers (16-bit)

; DOS buffered input structure for AH=0Ah
; [0]=maxlen, [1]=len, [2..]=chars
inbuf           db 16,0, 16 dup(0)

prompt_input    db "Enter 10 numbers (each on new line):",0Dh,0Ah,'$'
prompt_result   db 0Dh,0Ah,"Sorted array:",0Dh,0Ah,'$'

.CODE

; --------------------------------------------
; Print DOS '$'-terminated string
; --------------------------------------------
print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; --------------------------------------------
; Print CRLF
; --------------------------------------------
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

; --------------------------------------------
; Read one line from keyboard and convert to number
; Return: AX = number
; (no extra validation, minimal)
; --------------------------------------------
read_num proc
    push dx

    mov ah, 0Ah
    lea dx, inbuf
    int 21h

    ; Make ASCIIZ: inbuf[2+len] = 0
    mov bl, inbuf[1]
    xor bh, bh
    mov byte ptr inbuf[2+bx], 0

    lea si, inbuf+2
    call atoi

    pop dx
    ret
read_num endp

; --------------------------------------------
; atoi: DS:SI -> ASCIIZ decimal string
; Return: AX = signed 16-bit integer
; (minimal, no overflow checks)
; --------------------------------------------
atoi proc
    push bx
    push cx

    xor ax, ax
    xor bx, bx           ; BL = sign flag (0/1)

    ; Skip spaces/tabs
skip_ws:
    mov cl, [si]
    cmp cl, ' '
    je ws_next
    cmp cl, 09h
    je ws_next
    jmp check_sign
ws_next:
    inc si
    jmp skip_ws

    ; Optional minus sign
check_sign:
    mov cl, [si]
    cmp cl, '-'
    jne parse_digits
    mov bl, 1
    inc si

parse_digits:
    mov cl, [si]
    cmp cl, 0
    je done

    ; AX = AX*10 + (digit)
    sub cl, '0'
    mov bx, 10
    mul bx               ; DX:AX = AX*10
    xor ch, ch
    add ax, cx

    inc si
    jmp parse_digits

done:
    cmp bl, 1
    jne ok
    neg ax
ok:
    pop cx
    pop bx
    ret
atoi endp

; --------------------------------------------
; Print signed number in AX
; --------------------------------------------
print_num proc
    push ax
    push bx
    push cx
    push dx

    cmp ax, 0
    jge pn_abs
    mov ah, 02h
    mov dl, '-'
    int 21h
    neg ax

pn_abs:
    cmp ax, 0
    jne pn_loop
    mov ah, 02h
    mov dl, '0'
    int 21h
    jmp pn_end

pn_loop:
    xor cx, cx
    mov bx, 10
pn_div:
    xor dx, dx
    div bx               ; AX=AX/10, DX=remainder
    push dx
    inc cx
    cmp ax, 0
    jne pn_div

pn_out:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop pn_out

pn_end:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_num endp

; ============================================
; MAIN
; ============================================
main proc
    mov ax, @data
    mov ds, ax

    ; -------- PART 1: INPUT ARRAY --------
    print_str prompt_input

    lea di, array
    mov cx, 10
input_loop:
    call read_num
    mov [di], ax
    add di, 2
    loop input_loop

    ; =====================================
    ; PART 2: INSERTION SORT (same algorithm)
    ; =====================================
    mov cx, 1                        ; i = 1

outer_loop:
    cmp cx, 10
    jge sort_done

    ; key = array[i]
    mov si, cx
    shl si, 1                        ; offset = i*2
    mov ax, [array + si]             ; AX = key

    ; j = i - 1
    mov si, cx
    dec si

compare_loop:
    cmp si, 0
    jl insert_element

    ; left = array[j]
    mov bx, si
    shl bx, 1
    mov dx, [array + bx]             ; DX = left

    cmp dx, ax
    jle insert_element

    ; array[j+1] = array[j]  (shift right)
    mov di, si
    inc di
    mov bx, di
    shl bx, 1
    mov [array + bx], dx

    dec si
    jmp compare_loop

insert_element:
    ; array[j+1] = key
    inc si
    mov bx, si
    shl bx, 1
    mov [array + bx], ax

    inc cx
    jmp outer_loop

sort_done:
    ; -------- PART 3: OUTPUT SORTED ARRAY --------
    print_str prompt_result

    lea si, array
    mov cx, 10
output_loop:
    mov ax, [si]
    call print_num
    call print_crlf
    add si, 2
    loop output_loop

    mov ax, 4C00h
    int 21h
main endp

END main