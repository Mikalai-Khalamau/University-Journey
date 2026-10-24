.MODEL small
.STACK 100h

; CONSTANTS
NEGATIVE        EQU -1          ; Flag for negative numbers
ARRAY_MAX_SIZE  EQU 30          ; Maximum array size
ARRAY_MIN_SIZE  EQU 2           ; Minimum array size
MAX_NUM         EQU 32767       ; Maximum signed 16-bit value
MIN_NUM         EQU -32767      ; Minimum signed 16-bit value

.DATA
    ; BUFFERS
    numberBuffer    db 9 DUP(?)             ; Input buffer for string numbers
    massive         dw ARRAY_MAX_SIZE DUP(?)   ; Array to store integers
    size            db 0                    ; Actual array size
    
    ; WORKING VARIABLES
    temp            dw 5                    ; Overflow check counter
    Iterator        db "[00] (32767 max): $"  ; Element number display
    zero_res_int_excep db '0'
    max             dw MIN_NUM              ; Maximum value in array
    min             dw MAX_NUM              ; Minimum value in array
    
    ; BORDER VALUES
    MinBorder       dw ?                    ; Lower bound for transformation
    MaxBorder       dw ?                    ; Upper bound for transformation
    max_min         dw 0                    ; max - min (denominator)
    hig_low         dw 0                    ; MaxBorder - MinBorder
    
    ; FLAGS
    exception_flag  db '0'
    is_minus        db '0'                  ; Negative number flag
    is_ok           db '0'                  ; Input validity flag
    is_num          db '0'                  ; Digit check flag
    
    ; MESSAGES
    enter_size_call db 10,13,"Enter array size(2-30): $"
    enter_msg       db "Enter number $"
    reentering_msg  db 10,13,"Reenter$",10,13
    result_msg      db 10,13,"Result",10,13,"$"
    OutPuting       db 0Ah, 0Dh, "That is a result", 0Ah, 0Dh, '$'
    MinBorderMess   db 0Ah, 0Dh, "Enter your Minimal border", 0Ah, 0Dh, '$'
    MaxBorderMess   db 0Ah, 0Dh, "Enter your Maximal border", 0Ah, 0Dh, '$'
    
    ; ERROR MESSAGES
    error_division_by_zero      db 10,13, "Division by zero, exitting...",10,13,"$"
    error_WrongInput            db 10,13,"Wrong input. Other symbols in integer number.",10,13,"Reenter...",10,13,"$"
    error_Overflow              db "Overflow. ABS of number is bigger than 32767",10,13,"Reenter...$"
    error_NotNumber             db "Not a number!",10,13,"Reenter....$"
    error_InResult_Overflow     db 10,13,"Overflow in result variable. Can't calculate.",10,13,'$'

.CODE

; OutInt - Output signed integer in AX
OutInt proc
    push cx
    test ax, ax
    jns oi1
    mov cx, ax
    mov ah, 02h
    mov dl, '-'
    int 21h
    mov ax, cx
    neg ax
oi1:
    xor cx, cx
    mov bx, 10
oi2:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz oi2
    mov ah, 02h
oi3:
    pop dx
    add dl, '0'
    int 21h
    loop oi3
    pop cx
    ret
OutInt endp

; print - Macro to print string
print macro string
    push dx
    push ax
    lea dx, string
    mov ah, 09H
    int 21h
    pop ax
    pop dx
endm

; println - Macro to print newline
println macro
    push dx
    push ax
    mov ah, 02h
    mov dl, 0Ah         ; \n
    int 21h
    mov dl, 0Dh         ; \r
    int 21h
    pop ax
    pop dx
endm

; get_string - Read string from keyboard
; Input: DX - buffer address
get_string proc
    push si
    push cx
    mov si, dx
    mov byte ptr [si], 7    ; Max length

    mov ah, 0Ah             ; DOS buffered input
    int 21h

    xor ax, ax
    mov al, [si + 1]        ; Actual length

    add si, ax
    mov byte ptr [si + 2], '$'  ; Terminate string

    pop cx
    pop si
    ret
get_string endp

; atoi - Convert string to integer
; Output: AX - converted number
atoi proc
    push di
    push si
    push bx
    mov temp, 5             ; Reset overflow counter
    xor si, si
    mov si, 2
    cmp numberBuffer[si], '-'
    jne positive
    mov di, 1               ; Negative flag
    inc si

positive:
    cmp numberBuffer[si], '0'
    jb notANumber
    cmp numberBuffer[si], '9'
    ja notANumber

    xor ax, ax
    mov cx, 10

atoi_loop:
    xor bx, bx
    mov bl, numberBuffer[si]

    cmp bl, '0'
    jb created
    cmp bl, '9'
    ja created

    sub bl, '0'
    mov dx, ax              ; Save for overflow check
    mul cx
    
    cmp temp, 0
    jne continue_ati
    cmp ax, dx              ; Check overflow
    ja overflow

continue_ati:
    add ax, bx
    mov bx, ax
    and bx, 8000h           ; Check sign bit
    jnz overflow
    dec temp
    inc si
    jmp atoi_loop

overflow:
    cmp di, 1
    jne err
    cmp ax, 8000h           ; Allow -32768
    je created
err:
    print error_Overflow
    printLn
    mov is_ok, '0'
    jmp finish

notANumber:
    print error_NotNumber
    println
    jmp finish

created:
    xor cx, cx
    cmp di, 1
    jne finish
    xor ax, NEGATIVE        ; Two's complement
    inc ax

finish:
    pop dx
    pop si
    pop di
    ret
atoi endp

; func - Linear transformation procedure
; Formula: (number - min)/(max - min) * (high - low) + low
func PROC
    ; Calculate max - min
    mov bx, max
    mov cx, min
    sub bx, cx
    mov max_min, bx

    ; Calculate high - low
    mov bx, MaxBorder
    mov cx, MinBorder
    sub bx, cx
    mov hig_low, bx

    mov si, offset massive
    mov cl, size
    mov ch, 0

func_loop:
    push cx

    ; number - min
    mov bx, [si]
    mov cx, min
    sub bx, cx

    ; Multiply by (high - low)
    mov ax, bx
    imul hig_low
    cmp dx, 0
    jne overflow_end

    ; Divide by (max - min)
    mov cx, max_min
    mov dx, 0
    idiv cx                 ; Result in AX

    mov cx, ax
    add ax, MinBorder       ; Add low bound

    ; Check for overflow
    cmp MinBorder, 0
    jg greater_0

lower_0:
    cmp ax, cx
    jg overflow_end
    jmp crtd

greater_0:
    cmp ax, cx
    jl overflow_end

crtd:
    mov [si], ax            ; Store transformed value

    pop cx
    add si, 2
    loop func_loop
    jmp fin_func

overflow_end:
    printLn
    print error_InResult_Overflow
    printLn
    mov is_ok, '0'
    pop cx
    jmp fin_func

error:
    printLn
    print error_division_by_zero
    printLn
    mov is_ok, '0'
    pop cx

fin_func:
    ret
func ENDP

; getMax - Macro to find maximum in array
getMax macro
    local array_Loop_max, next
    push si
    push ax
    push cx
    xor cx, cx
    mov cl, size
    mov si, 0

array_Loop_max:
    mov ax, massive[si]
    cmp ax, max
    jle next

    mov ax, massive[si]
    mov max, ax

next:
    add si, 2
    loop array_Loop_max

    pop cx
    pop ax
    pop si
endm

; getMin - Macro to find minimum in array
getMin macro
    local array_Loop_min, next
    push si
    push ax
    push cx
    xor cx, cx
    mov cl, size
    mov si, 0

array_Loop_min:
    mov ax, massive[si]
    cmp ax, min
    jge next

    mov ax, massive[si]
    mov min, ax

next:
    add si, 2
    loop array_Loop_min

    pop cx
    pop ax
    pop si
endm

; Check_num - Validate numeric input
Check_num PROC
    push si
    mov is_ok, '0'
    jmp check_start

err_min_zero:
    mov is_ok, '0'
    jmp finish_check_num

check_start:
    mov si, offset numberBuffer+2
    mov is_minus, '0'
    mov is_ok, '0'

    cmp byte ptr [si], '-'
    jne check_num_for
    mov is_minus, '1'
    inc si

    cmp byte ptr [si], '0'
    je err_min_zero

check_num_for:
    call Compare_num
    cmp is_num, '0'
    je finish_check_num

    inc si
    cmp byte ptr [si], '$'
    jne check_num_for

    mov is_ok, '1'

finish_check_num:
    pop si
    ret
Check_num ENDP

; Compare_num - Check if character is digit
Compare_num PROC
    mov is_num, '0'
    mov ah, [si]
    cmp ah, '0'
    jb fin
    cmp ah, '9'
    ja fin
    mov is_num, '1'
fin:
    ret
Compare_num ENDP

; Element - Display element number
Element PROC
    push bx
    push si
    push cx
    xor ax, ax

    mov bl, 10
    mov al, cl
    div bl

    mov si, offset Iterator
    add al, 48
    mov [si+1], al

    add ah, 48
    mov [si+2], ah

    pop cx
    pop si
    pop bx
    ret
Element ENDP

; MAIN PROGRAM
start:
    mov ax, @DATA
    mov ds, ax

    jmp enter_size

enterLoop_err:
    print error_wrongInput
    jmp enterLoop

    mov dx, offset numberBuffer

    ; Enter array size
enter_size:
    print enter_size_call
    lea dx, numberBuffer
    call get_string
    call Check_num
    cmp is_ok, '0'
    je enter_size
    call atoi
    cmp ax, ARRAY_MIN_SIZE
    jb enter_size
    cmp ax, ARRAY_MAX_SIZE
    ja enter_size
    mov cx, ax
    mov si, 0

    ; Enter array elements
enterLoop:
    push si
    mov is_ok, '0'
    println
    print enter_msg
    call Element
    print Iterator
    lea dx, numberBuffer
    call get_string

    call Check_num
    cmp is_ok, '0'
    je enterLoop_err

    printLn

    push cx
    call atoi
    cmp cx, 0
    pop cx
    jne enterLoop

    pop si
    mov massive[si], ax
    inc size
    add si, 2               ; Move to next element

    dec cx
    cmp cx, 0
    jne enterLoop

    ; Enter borders
border_enter_low:
    println
    print MinBorderMess
    lea dx, numberBuffer
    call get_string

    call Check_num
    cmp is_ok, '0'
    je border_enter_low
    call atoi
    cmp is_ok, '0'
    je border_enter_low
    mov MinBorder, ax

border_enter_hight:
    println
    print MaxBorderMess
    lea dx, numberBuffer
    call get_string

    call Check_num
    cmp is_ok, '0'
    je border_enter_hight
    call atoi
    cmp is_ok, '0'
    je border_enter_hight
    mov MaxBorder, ax

    ; Find min/max and transform
    getMin
    getMax

    call func
    cmp is_ok, '0'
    je fin_main

    ; Output results
    printLn
    print result_msg
    printLn

    mov ch, 0
    mov cl, size
    mov si, offset massive

output_loop:
    mov ax, [si]
    call OutInt
    printLn
    add si, 2
    loop output_loop

fin_main:
    mov ax, 4C00h
    int 21h
end start
