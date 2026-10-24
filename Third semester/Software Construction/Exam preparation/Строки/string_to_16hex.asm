.model small
.stack 100h

.data
    buffer  db 100 dup (?)           ; input buffer
    prompt  db 'input string: $'
    newline db 0Dh,0Ah,'$'
    output_msg db 'your string: $'

.code
.startup

    ; print prompt
    mov ah, 09h
    mov dx, offset prompt
    int 21h

    ; DI points to buffer start
    mov di, offset buffer

; ===== INPUT LOOP (character by character) =====
input_loop:
    mov ah, 01h          ; DOS: read char with echo
    int 21h              ; AL = char

    cmp al, 0Dh          ; Enter pressed?
    je  end_input

    mov [di], al         ; store char
    inc di
    jmp input_loop

end_input:
    mov byte ptr [di], '$'   ; terminate string with '$'

    ; ===== REMOVE SPACES IN-PLACE =====
    mov si, offset buffer    ; SI = read pointer
    mov di, offset buffer    ; DI = write pointer

remove_loop:
    mov al, [si]             ; read char
    cmp al, '$'
    je  remove_done          ; end of string

    cmp al, ' '              ; space?
    je  skip_char            ; skip spaces

    mov [di], al             ; keep non-space
    inc di

skip_char:
    inc si
    jmp remove_loop

remove_done:
    mov byte ptr [di], '$'   ; new end of string
    ; ===== END REMOVE SPACES =====

    ; print newline
    mov ah, 09h
    mov dx, offset newline
    int 21h

    ; print "your string: "
    mov ah, 09h
    mov dx, offset output_msg
    int 21h


; ===== OUTPUT LOOP (character by character) =====
    mov si, offset buffer    ; SI -> first character

print_loop:
    mov al, [si]             ; get current character
    cmp al, '$'              ; end of string?
    je  print_done

    mov ah, 02h              ; DOS: print char in DL
    mov dl, al
    int 21h

    inc si
    jmp print_loop

print_done:
    ; final newline (optional)
    mov ah, 09h
    mov dx, offset newline
    int 21h

    mov ah, 4Ch
    int 21h

end
