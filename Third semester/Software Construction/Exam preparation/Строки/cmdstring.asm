; ============================================
; COMMAND LINE STRING OUTPUT (character by character)
; Input: String from command line
; Output: Each character on new line
; ============================================

.MODEL small
.STACK 100h

.DATA
    msg_empty   db 'No arguments provided!', 0Dh, 0Ah, '$'
    msg_output  db 'Characters:', 0Dh, 0Ah, '$'

.CODE

; ===== Print string =====
print_str macro s
    push ax
    push dx
    lea dx, s
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

; ===== Print newline =====
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

; ===== MAIN PROGRAM =====
start:
    mov ax, @data
    mov ds, ax
    
    ; ===== Get command line arguments =====
    ; PSP (Program Segment Prefix) at DS:0080h
    ; Byte at 0080h = length of command line
    ; String starts at 0081h
    
    mov cl, byte ptr ds:[0080h]     ; CL = length of command line
    cmp cl, 0                       ; Empty?
    je no_args
    
    ; Skip leading spaces
    mov si, 0081h                   ; SI = start of command line
    
skip_spaces:
    cmp cl, 0
    je no_args
    
    mov al, byte ptr ds:[si]
    cmp al, ' '
    jne start_output
    
    inc si
    dec cl
    jmp skip_spaces
    
no_args:
    print_str msg_empty
    jmp exit_program
    
    ; ===== Output header =====
start_output:
    print_str msg_output
    call print_crlf
    
    ; ===== Output each character =====
output_loop:
    cmp cl, 0                       ; End of string?
    je exit_program
    
    mov al, byte ptr ds:[si]        ; AL = current character
    
    ; Skip carriage return at end
    cmp al, 0Dh
    je exit_program
    
    ; Print character
    mov ah, 02h
    mov dl, al
    int 21h
    
    ; Print newline
    call print_crlf
    
    inc si
    dec cl
    jmp output_loop
    
exit_program:
    mov ax, 4C00h
    int 21h

END start
