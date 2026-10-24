.model small
.stack 100h

.data
    buffer     db 100 dup (?)
    prompt     db 'Input string: $'
    newline    db 0Dh,0Ah,'$'
    output_msg db 'Hex representation: $'

.code
.startup

    ; ===== INPUT =====
    mov ah, 09h
    mov dx, offset prompt
    int 21h

    mov di, offset buffer

input_loop:
    mov ah, 01h
    int 21h
    cmp al, 0Dh
    je  end_input
    mov [di], al
    inc di
    jmp input_loop

end_input:
    mov byte ptr [di], '$'

    ; print newline
    mov ah, 09h
    mov dx, offset newline
    int 21h

    ; print message
    mov ah, 09h
    mov dx, offset output_msg
    int 21h

    ; ===== OUTPUT HEX =====
    mov si, offset buffer

hex_loop:
    mov al, [si]
    cmp al, '$'
    je  hex_done

    call byte_to_hex         ; print AL as 2 hex digits

    ; space separator
    mov ah, 02h
    mov dl, ' '
    int 21h

    inc si
    jmp hex_loop

hex_done:
    ; final newline
    mov ah, 09h
    mov dx, offset newline
    int 21h

    mov ah, 4Ch
    int 21h

; ===== PROCEDURES =====

; byte_to_hex: print AL as 2 hex chars
byte_to_hex proc
    push ax
    push bx

    ; upper nibble
    mov bl, al
    shr bl, 4
    call print_hex_digit

    ; lower nibble
    mov bl, al
    and bl, 0Fh
    call print_hex_digit

    pop bx
    pop ax
    ret
byte_to_hex endp

; print_hex_digit: print BL (0..15) as '0'..'F'
print_hex_digit proc
    push ax
    push dx

    cmp bl, 10
    jl  is_digit

    ; A..F
    mov dl, bl
    sub dl, 10
    add dl, 'A'
    jmp do_print

is_digit:
    mov dl, bl
    add dl, '0'

do_print:
    mov ah, 02h
    int 21h

    pop dx
    pop ax
    ret
print_hex_digit endp

end
