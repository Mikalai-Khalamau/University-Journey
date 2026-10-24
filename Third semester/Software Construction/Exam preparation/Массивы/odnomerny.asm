.model small
.stack 100h

.data
    array db 10 dup(?)                          ; Array of 10 bytes
    prompt db 0Dh, 0Ah, 'Enter element: ', '$'
    result_msg db 0Dh, 0Ah, 'Your array: ', '$'
    space_msg db ' ', '$'

.code
main proc
    mov ax, @data
    mov ds, ax

    ; ========================================
    ; INPUT: Read 10 single-digit numbers
    ; ========================================
    lea si, array                ; SI = pointer to array
    mov cx, 10                   ; CX = 10 elements

input_loop:
    ; Print prompt
    lea dx, prompt
    mov ah, 09h
    int 21h

    ; Read single character (digit 0-9)
    mov ah, 01h
    int 21h                      ; AL = ASCII digit

    ; Convert ASCII to number
    sub al, '0'                  ; AL = 0-9
    mov [si], al                 ; Store in array

    inc si                       ; Next array position

    loop input_loop              ; Repeat 10 times

    ; ========================================
    ; OUTPUT: Print the array
    ; ========================================
    lea dx, result_msg
    mov ah, 09h
    int 21h

    lea si, array                ; SI = pointer to array
    mov cx, 10                   ; CX = 10 elements

output_loop:
    ; Get element
    mov al, [si]                 ; AL = element
    add al, '0'                  ; Convert to ASCII

    ; Print character
    mov dl, al
    mov ah, 02h
    int 21h

    ; Print space
    lea dx, space_msg
    mov ah, 09h
    int 21h

    inc si                       ; Next element
    loop output_loop             ; Repeat 10 times

    ; Exit
    mov ah, 4ch
    int 21h
    
main endp
end main
