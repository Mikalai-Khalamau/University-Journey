; Компиляция: nasm -f bin lab2.asm -o lab2.com
; Запуск:     dosbox lab2.com

[BITS 16]
[ORG 0x100]

section .text

start:
    mov ax, 0x0003
    int 10h

    mov dx, msg_real_start
    mov ah, 0x09
    int 21h

    ; 2. СОХРАНЕНИЕ КОНТЕКСТА И ПАТЧИНГ АДРЕСОВ
    mov [saved_ss], ss
    mov [saved_sp], sp
    movzx esp, sp               ; Обнуление старших бит стека ESP

    ; Патчим адрес возврата в реальный режим сегментом CS
    mov ax, cs
    mov [patch_rm_seg], ax

    ; раскидываем 32 битный адрес по 3м кускам дескриптора кода и данных 
    ; т.е. переводим физический адрес что сейчас в нужный формат
    mov ax, cs
    movzx eax, ax
    shl eax, 4                  


    mov [gdt_code + 2], ax
    ror eax, 16
    mov [gdt_code + 4], al
    mov [gdt_code + 7], ah

    mov ax, cs
    movzx eax, ax
    shl eax, 4

    mov [gdt_data + 2], ax
    ror eax, 16
    mov [gdt_data + 4], al
    mov [gdt_data + 7], ah

    ; записали линейный адрес самой таблицы в GDTR
    mov ax, cs
    movzx eax, ax
    shl eax, 4
    add eax, gdt_table
    mov [gdtr_addr], eax

    ; Сохраняем маски прерываний PIC
    in al, 0x21
    mov [saved_pic1], al
    in al, 0xA1
    mov [saved_pic2], al

    ; ЗАПРЕТ ПРЕРЫВАНИЙ
    cli                        

    ; Запрет Немаскируемых прерываний
    in al, 0x70                 
    or al, 0x80
    out 0x70, al

    mov al, 0xFF              
    out 0x21, al
    out 0xA1, al


    lgdt [gdtr]                 

    ; Бит PE = 1 (включили защ реж)
    mov eax, cr0
    or al, 1                    
    mov cr0, eax

    jmp 0x08:pm_entry

pm_entry: 
    ; настройка нужного селектора данных
    mov ax, 0x10                
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov esp, stack_top

    ; видеосегмент
    mov ax, 0x18
    mov es, ax

    ; строку по центру
    mov si, msg_pm
    mov di, (12 * 80 + 22) * 2  ; 12-я строка, 22-я колонка
    mov ah, 0x1F                ; Атрибут: Белый текст на синем фоне

print_loop:
    lodsb
    test al, al
    jz print_done
    mov [es:di], ax
    add di, 2
    jmp print_loop

print_done:
    ; возврат в r-mode
    ; регистры безопасным селектором 0x10 (Limit = 64Kb)
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; PE = 0
    mov eax, cr0
    and al, 0xFE
    mov cr0, eax

    ; Прямой дальний прыжок в реальный режим
    db 0xEA
    dw rm_entry
patch_rm_seg:
    dw 0

rm_entry: ; r-mode
    ; Восстановление сегментов и стека
    mov ax, cs
    mov ds, ax
    mov es, ax
    mov ss, [saved_ss]
    movzx esp, word [saved_sp]

    ; Восстановление прерываний PIC и NMI
    mov al, [saved_pic1]
    out 0x21, al
    mov al, [saved_pic2]
    out 0xA1, al

    in al, 0x70
    and al, 0x7F
    out 0x70, al

    sti                         ; Разрешаем прерывания

    mov dx, msg_real_back
    mov ah, 0x09
    int 21h

    mov ax, 0x4C00
    int 21h


saved_ss    dw 0
saved_sp    dw 0
saved_pic1  db 0
saved_pic2  db 0

msg_real_start db '1. [Real Mode] Transitioning to Protected Mode...', 13, 10, '$'
msg_pm         db '>>> [INFO] Protected Mode <<<', 0
msg_real_back  db '2. [INFO] Return to real mode. Press key: $', 13, 10, '$'

stack_bottom:
    times 256 db 0
stack_top:

align 8
gdtr:
    gdtr_limit dw gdt_end - gdt_table - 1
    gdtr_addr  dd 0

gdt_table:
    ; 0x00: Null Descriptor
    dq 0

    ; 0x08: Code Segment Descriptor
    gdt_code:
    dw 0xFFFF
    dw 0x0000
    db 0x00
    db 0x9A
    db 0x00
    db 0x00

    ; 0x10: Data Segment Descriptor
    gdt_data:
    dw 0xFFFF
    dw 0x0000
    db 0x00
    db 0x92
    db 0x00
    db 0x00

    ; 0x18: Video Segment Descriptor (Base = 0x000B8000)
    gdt_video:
    dw 0xFFFF
    dw 0x8000
    db 0x0B
    db 0x92
    db 0x00
    db 0x00

gdt_end:
