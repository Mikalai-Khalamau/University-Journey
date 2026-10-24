.model small
.stack 100h

.data
    array db 9 dup(?)
    prompt db 0Dh, 0Ah, 'enter element: ', '$'

.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, array

    mov cx, 3
row_loop:
    mov bx, 3
col_loop:
    lea dx, prompt
    mov ah, 09h
    int 21h

    mov ah, 01h
    int 21h

    sub al, '0'
    mov [si], al

    inc si

    dec bx
    jnz col_loop

    dec cx
    jnz row_loop

    mov ah, 4ch
    int 21h
main endp
end main
