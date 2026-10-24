.model tiny

CR     EQU 13                ; Carriage return
LF     EQU 10                ; Line feed
MAXLEN EQU 202               ; Buffer size
SPACE  EQU 32                ; Space character

.code
    org 100h

    mov ax, @data
    mov ds, ax

    ; Input base string 
    lea dx, base_msg
    call out_str
    lea dx, base_str
    call in_str

    ; Input search word
    lea dx, srch_msg
    call out_str
    lea dx, srch_str
    call in_str

    ; Input insert word
    lea dx, ins_msg
    call out_str
    lea dx, ins_str
    call in_str

    xor ax, ax
    xor dx, dx

    ; Check if strings are not empty
    mov al, base_str[1]
    cmp ax, 0
    je error1

    mov dl, ins_str[1]
    cmp dx, 0
    je error1

    xor dx, dx
    mov dl, srch_str[1]
    cmp dx, 0
    je error1

    ; Search for word 
    mov si, offset base_str + 2
    mov di, offset srch_str + 2
    sub al, dl
    xor cx, cx
    mov cl, al
    inc cx

search:
    pusha
    xor cx, cx
    mov cx, dx
    repe cmpsb
    jz check_word_boundary
    popa
    inc si
    loop search

    ; Word not found
    lea dx, notfound_msg
    call out_str
    jmp exit_program

check_word_boundary:
    ; SI now points after matched substring
    mov al, [si]
    cmp al, 0
    je check_before
    cmp al, SPACE
    je check_before
    cmp al, CR
    je check_before
    cmp al, LF
    je check_before
    jmp not_whole_word

check_before:
    popa                            ; Restore to get original SI
    push si                         ; Save SI (start of match)
    
    cmp si, offset base_str + 2
    je found_valid
    
    dec si
    mov al, [si]
    cmp al, SPACE
    jne not_whole_word_cleanup
    
found_valid:
    pop si                          ; Restore SI (start of match)
    jmp found

not_whole_word_cleanup:
    pop si                          ; Clean stack
    jmp not_whole_word_continue

not_whole_word:
    popa

not_whole_word_continue:
    inc si
    loop search
    
    lea dx, notfound_msg
    call out_str
    jmp exit_program

found:
    ; SI points to START of found word in base_str
    mov bx, si                      ; Save position of found word
    
    ; Calculate position (number of chars before found word)
    mov cx, si
    sub cx, offset base_str + 2
    
    ; Copy part BEFORE found word to result
    mov di, offset res_str
    mov si, offset base_str + 2
    call copy_str                   ; DI now points after copied part

    ; Insert new word
    mov cl, ins_str[1]
    mov ch, 0
    mov si, offset ins_str + 2
    call copy_str

    ; Insert space
    mov byte ptr [di], SPACE
    inc di

    ; Copy found word and everything after it
    mov si, bx                      ; SI = start of found word
    mov cl, base_str[1]             ; Total length
    mov al, bl
    sub al, byte ptr (offset base_str + 2)
    sub cl, al                      ; Remaining length from found word
    mov ch, 0
    call copy_str

    jmp res_in

res_in:
    lea dx, res_msg
    call out_str

    ; Calculate result string length (filter CR/LF)
    mov si, offset res_str
    mov di, offset res_str
    mov cl, base_str[1]
    add cl, ins_str[1]
    add cl, 1                       ; +1 for space
    mov ch, 0
    
filter_result:
    cmp cx, 0
    je filter_done
    mov al, [si]
    cmp al, CR
    je skip_char
    cmp al, LF
    je skip_char
    cmp al, 0
    je filter_done
    mov [di], al
    inc di
skip_char:
    inc si
    loop filter_result

filter_done:
    mov ax, di
    sub ax, offset res_str
    mov res_len, al

    ; Output result string byte by byte
    lea si, res_str
    mov cl, res_len
    call out_bytes

    ; Print newline after result
    call print_newline

    jmp exit_program

error1:
    lea dx, er1_msg
    call out_str

exit_program:
    mov ax, 4C00h
    int 21h

; PROCEDURES

out_str proc
    pusha
    mov dl, CR
    mov ah, 02h
    int 21h
    mov dl, LF
    mov ah, 02h
    int 21h
    popa
    mov ah, 9
    int 21h
    ret
out_str endp

print_newline proc
    push ax
    push dx
    mov dl, CR
    mov ah, 02h
    int 21h
    mov dl, LF
    mov ah, 02h
    int 21h
    pop dx
    pop ax
    ret
print_newline endp

out_bytes proc
    push ax
    push cx
    push dx
    push si
    
    xor ch, ch
    cmp cx, 0
    je out_bytes_end

out_bytes_loop:
    mov dl, [si]
    ; Skip control characters during output
    cmp dl, 32
    jb skip_output
    mov ah, 02h
    int 21h
skip_output:
    inc si
    loop out_bytes_loop

out_bytes_end:
    pop si
    pop dx
    pop cx
    pop ax
    ret
out_bytes endp

in_str proc
    push ax
    mov ah, 0ah
    int 21h
    pop ax
    ret
in_str endp

copy_str proc
    push ax
    cmp cx, 0
    jz end_copy
loop_str:
    mov al, [si]
    ; Don't copy CR or LF
    cmp al, CR
    je skip_copy
    cmp al, LF
    je skip_copy
    mov [di], al
    inc di
skip_copy:
    inc si
    loop loop_str
end_copy:
    pop ax
    ret
copy_str endp

.data
    notfound_msg db "There is no such word in your string! $"
    base_msg     db "Enter base string: $"
    srch_msg     db "Enter the word to find in the base string: $"
    ins_msg      db "Enter the word to insert in the base string before found word: $"
    res_msg      db "The result string is: $"
    er1_msg      db "Input error! $"

    base_str     db MAXLEN, MAXLEN dup (0)
    srch_str     db MAXLEN, MAXLEN dup (0)
    ins_str      db MAXLEN, MAXLEN dup (0)
    res_str      db MAXLEN dup (0)
    res_len      db 0
end start
