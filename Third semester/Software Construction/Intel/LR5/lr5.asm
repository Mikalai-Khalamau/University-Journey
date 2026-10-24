.MODEL small
.STACK 100h

.DATA
    fileIn        db 128 dup(0)
    fileOut       db 128 dup(0)
    searchWord    db 52 dup(0)        ; слово + '$' + запас
    word_len      db 0

    IDfileIn      dw ?
    IDfileOut     dw ?

    line_buf      db 200 dup(0)       ; буфер строки (<64К)
    symbol        db ?
    word_found    db 0

    msg_start     db 'Program started.',0Dh,0Ah,'$'
    msg_usage     db 'Usage: program <input_file> <output_file> <search_word>',0Dh,0Ah,'$'
    msg_open_in   db 'Opening input file...',0Dh,0Ah,'$'
    msg_open_out  db 'Creating output file...',0Dh,0Ah,'$'
    msg_search    db 'Searching for word: $'
    msg_process   db 'Processing...',0Dh,0Ah,'$'
    msg_done      db 'Processing complete.',0Dh,0Ah,'$'
    msg_err_open  db 'Error: Cannot open input file.',0Dh,0Ah,'$'
    msg_err_create db 'Error: Cannot create output file.',0Dh,0Ah,'$'
    msg_err_args  db 'Error: Invalid command line arguments.',0Dh,0Ah,'$'
    newline       db 0Dh,0Ah,'$'

.CODE

print macro msg
    push ax
    push dx
    lea dx, msg
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

;---------------------------------------
; Точка входа
;---------------------------------------
start:
    mov ax, @DATA
    mov ds, ax

    print msg_start

    ; разбор командной строки
    call parse_cmdline
    cmp ax, 0
    jne error_args

    ; показываем, какое слово ищем
    print msg_search
    lea dx, searchWord
    mov ah, 09h
    int 21h
    print newline

    print msg_open_in
    call open_input
    cmp ax, 0
    jne error_open_in

    print msg_open_out
    call create_output
    cmp ax, 0
    jne error_create_out

    print msg_process
    call process_file

    call close_files

    print msg_done
    jmp exit_program

;---------------------------------------
; Обработка ошибок
;---------------------------------------
error_args:
    print msg_err_args
    print msg_usage
    jmp exit_program

error_open_in:
    print msg_err_open
    jmp exit_program

error_create_out:
    print msg_err_create
    call close_input
    jmp exit_program

exit_program:
    mov ax, 4C00h
    int 21h

;---------------------------------------
; parse_cmdline
;  AX = 0 - успех
;  AX = 1 - ошибка
;  fileIn, fileOut - ASCIZ
;  searchWord - строка, заканчивающаяся '$'
;  word_len - длина слова
;---------------------------------------
parse_cmdline proc
    push ax
    push bx
    push cx
    push dx
    push si
    push di
    push es

    ; В COM-программе ES указывает на PSP
    mov si, 80h           ; длина командной строки в PSP
    mov cl, es:[si]       ; CL = длина tail'а
    cmp cl, 0
    je pc_error           ; нет параметров

    inc si                ; SI -> первый символ хвоста (81h)

    ; пропустить ведущие пробелы и табы
skip_leading:
    cmp cl, 0
    je pc_error
    mov al, es:[si]
    cmp al, ' '
    je sl_next
    cmp al, 09h           ; таб
    je sl_next
    jmp get_input
sl_next:
    inc si
    dec cl
    jmp skip_leading

; ---------- входной файл ----------
get_input:
    lea di, fileIn

copy_input:
    cmp cl, 0
    je pc_error
    mov al, es:[si]
    cmp al, ' '
    je end_input
    cmp al, 09h
    je end_input
    cmp al, 0Dh
    je pc_error           ; перевод строки раньше, чем все параметры
    mov [di], al
    inc si
    inc di
    dec cl
    jmp copy_input

end_input:
    mov byte ptr [di], 0  ; ASCIZ-окончание имени входного файла

    ; пропустить пробелы/табы перед выходным файлом
skip_space2:
    cmp cl, 0
    je pc_error
    mov al, es:[si]
    cmp al, ' '
    je ss2_next
    cmp al, 09h
    je ss2_next
    jmp get_output
ss2_next:
    inc si
    dec cl
    jmp skip_space2

; ---------- выходной файл ----------
get_output:
    lea di, fileOut

copy_output:
    cmp cl, 0
    je pc_error
    mov al, es:[si]
    cmp al, ' '
    je end_output
    cmp al, 09h
    je end_output
    cmp al, 0Dh
    je pc_error
    mov [di], al
    inc si
    inc di
    dec cl
    jmp copy_output

end_output:
    mov byte ptr [di], 0  ; ASCIZ-имя выходного файла

    ; пропустить пробелы/табы перед словом
skip_space3:
    cmp cl, 0
    je pc_error
    mov al, es:[si]
    cmp al, ' '
    je ss3_next
    cmp al, 09h
    je ss3_next
    jmp get_word
ss3_next:
    inc si
    dec cl
    jmp skip_space3

; ---------- слово для поиска ----------
get_word:
    lea di, searchWord
    xor dl, dl            ; dl = длина слова

copy_word:
    cmp cl, 0
    je word_done
    mov al, es:[si]
    cmp al, 0Dh
    je word_done
    cmp al, ' '
    je word_done
    cmp al, 09h
    je word_done
    mov [di], al
    inc si
    inc di
    inc dl
    dec cl
    jmp copy_word

word_done:
    mov byte ptr [di], '$' ; для функции 09h и как терминатор в поиске
    mov word_len, dl
    cmp dl, 0
    je pc_error            ; пустое слово — ошибка

    xor ax, ax             ; успех
    jmp short pc_end

pc_error:
    mov ax, 1              ; ошибка

pc_end:
    pop es
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
parse_cmdline endp

;---------------------------------------
; Открытие входного файла (только чтение)
; AX=0 - успех, AX=1 - ошибка
;---------------------------------------
open_input proc
    lea dx, fileIn
    mov ah, 3Dh
    mov al, 00h            ; только чтение
    int 21h
    jc open_in_error
    mov IDfileIn, ax
    xor ax, ax
    ret
open_in_error:
    mov ax, 1
    ret
open_input endp

;---------------------------------------
; Создание выходного файла
; AX=0 - успех, AX=1 - ошибка
;---------------------------------------
create_output proc
    lea dx, fileOut
    mov ah, 3Ch
    mov cx, 0
    int 21h
    jc create_out_error
    mov IDfileOut, ax
    xor ax, ax
    ret
create_out_error:
    mov ax, 1
    ret
create_output endp

;---------------------------------------
; Закрытие обоих файлов
;---------------------------------------
close_files proc
    call close_input
    call close_output
    ret
close_files endp

close_input proc
    mov bx, IDfileIn
    mov ah, 3Eh
    int 21h
    ret
close_input endp

close_output proc
    mov bx, IDfileOut
    mov ah, 3Eh
    int 21h
    ret
close_output endp

;---------------------------------------
; Чтение одного байта в symbol
; symbol = 0 при EOF / ошибке
;---------------------------------------
read proc
    push cx
    mov bx, IDfileIn
    lea dx, symbol
    mov cx, 1
    mov ah, 3Fh
    int 21h
    cmp ax, 1
    jne read_eof
    pop cx
    ret
read_eof:
    mov symbol, 0
    pop cx
    ret
read endp

;---------------------------------------
; Запись строки из line_buf + CRLF
;---------------------------------------
write_line proc
    pusha
    mov bx, IDfileOut
    lea si, line_buf
next_char_wl:
    mov al, [si]
    cmp al, 0
    je finish_wl
    mov ah, 40h
    mov cx, 1
    mov symbol, al
    lea dx, symbol
    int 21h
    inc si
    jmp next_char_wl
finish_wl:
    mov symbol, 0Dh
    lea dx, symbol
    mov ah, 40h
    mov cx, 1
    int 21h
    mov symbol, 0Ah
    mov ah, 40h
    mov cx, 1
    int 21h
    popa
    ret
write_line endp

;---------------------------------------
; Очистка буфера строки
;---------------------------------------
clear_line_buf proc
    pusha
    lea di, line_buf
    mov cx, 200
    xor al, al
clear_loop:
    mov [di], al
    inc di
    loop clear_loop
    popa
    ret
clear_line_buf endp

;---------------------------------------
; Проверка: есть ли слово searchWord в line_buf
; - с учётом границ слова (пробел, таб, CR/LF, 0)
; - регистр не учитывается
; Результат: word_found = 1/0
;---------------------------------------
check_word_in_buffer proc
    pusha
    mov word_found, 0

    xor ch, ch
    mov cl, word_len
    cmp cl, 0
    je check_done          ; пустое слово не ищем

    lea si, line_buf
    xor dx, dx             ; позиция в line_buf (смещение от si)

scan_loop:
    ; текущий символ строки
    mov bp, si
    add bp, dx
    mov al, [bp]
    cmp al, 0
    je check_done          ; дошли до конца строки

    ; проверка левой границы
    cmp dx, 0
    je left_ok             ; в начале строки граница ок
    mov bp, si
    add bp, dx
    dec bp
    mov al, [bp]
    call is_delimiter
    cmp al, 1
    jne skip_pos           ; слева не разделитель -> не начало слова

left_ok:
    ; попытка сопоставить слово с позиции dx
    xor di, di             ; индекс в searchWord

match_char:
    ; символ из line_buf по позиции dx+di
    mov bp, si
    add bp, dx
    add bp, di
    mov al, [bp]

    ; символ из searchWord по di
    mov bp, offset searchWord
    add bp, di
    mov ah, [bp]

    ; конец searchWord по '$'?
    cmp ah, '$'
    je check_right

    ; конец строки?
    cmp al, 0
    je skip_pos

    ; сравнение без учёта регистра
    push ax
    call to_upper
    mov bl, al             ; верхний регистр символа строки
    pop ax
    mov al, ah             ; символ искомого слова
    call to_upper
    cmp al, bl
    jne skip_pos

    ; до сих пор совпадает — идём дальше
    inc di
    jmp match_char

check_right:
    ; всё слово совпало, проверяем правую границу
    mov bp, si
    add bp, dx
    add bp, di
    mov al, [bp]
    call is_delimiter
    cmp al, 1
    je found_it            ; справа граница -> это отдельное слово

skip_pos:
    inc dx
    jmp scan_loop

found_it:
    mov word_found, 1

check_done:
    popa
    ret
check_word_in_buffer endp

;---------------------------------------
; is_delimiter:
; AL = символ
; AL = 1, если разделитель слова
; AL = 0 иначе
;---------------------------------------
is_delimiter proc
    cmp al, 0
    je is_delim_yes
    cmp al, ' '
    je is_delim_yes
    cmp al, 09h
    je is_delim_yes
    cmp al, 0Dh
    je is_delim_yes
    cmp al, 0Ah
    je is_delim_yes
    mov al, 0
    ret
is_delim_yes:
    mov al, 1
    ret
is_delimiter endp

;---------------------------------------
; to_upper:
; AL = символ
; AL = тот же символ в верхнем регистре, если это 'a'..'z'
;---------------------------------------
to_upper proc
    cmp al, 'a'
    jb to_upper_done
    cmp al, 'z'
    ja to_upper_done
    sub al, 32
to_upper_done:
    ret
to_upper endp

;---------------------------------------
; Основная обработка файла:
; читаем по строкам (CR/LF), кладём в line_buf,
; ищем слово, при наличии — пишем строку в выходной файл
;---------------------------------------
process_file proc
next_line:
    call clear_line_buf
    lea di, line_buf
    mov word_found, 0

read_line_loop:
    call read
    cmp symbol, 0
    je all_done           ; EOF
    cmp symbol, 0Dh
    je process_line       ; конец строки (CR)
    cmp symbol, 0Ah
    je read_line_loop     ; пропускаем LF
    mov al, symbol
    mov [di], al
    inc di
    cmp di, offset line_buf+195 ; небольшой запас, чтобы не выйти за буфер
    jb read_line_loop

process_line:
    mov byte ptr [di], 0  ; 0-терминатор строки
    call check_word_in_buffer
    cmp word_found, 1
    jne next_line
    call write_line
    jmp next_line

all_done:
    ret
process_file endp

end start