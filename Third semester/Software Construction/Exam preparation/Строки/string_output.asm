.model small
.stack 100h

.data
    buffer db 100 dup (?)
    prompt db 'input string: $'
    newline db 0dh, 0ah, '$'
    output_msg db 'your string: $'

.code
.startup

    mov ah, 09h
    mov dx, offset prompt
    int 21h

    mov di, offset buffer

input_loop:
    mov ah, 01h
    int 21h

    cmp al, 0dh
    je  end_input

    mov [di], al
    inc di
    jmp input_loop

end_input:
    mov byte ptr [di], '$'

    mov ah, 09h
    mov dx, offset newline
    int 21h

    mov ah, 09h
    mov dx, offset output_msg
    int 21h

    mov ah, 09h
    mov dx, offset buffer
    int 21h

    mov ah, 4ch
    int 21h

end
