; ============================================
; BIT OPERATION: AND bit 2 and bit 5 -> bit 6
; Range: $8900-$8920 (33 bytes)
; ============================================

.MODEL small
.STACK 100h

.CODE

start:
    ; Setup segments
    mov ax, 8900h
    mov ds, ax              ; DS points to data at $8900

    ; ===== STEP 1: Process each byte =====
    xor si, si              ; SI = 0 (offset)

process_loop:
    cmp si, 33              ; 33 bytes ($8900-$8920)
    jge done

    mov al, byte ptr [si]   ; AL = current byte
    
    ; Extract bit 2
    mov cl, al              ; CL = copy of byte
    and cl, 00000100b       ; CL = bit 2 (cleared others)
    shr cl, 2               ; CL = bit 2 value (0 or 1)
    
    ; Extract bit 5
    mov dl, al              ; DL = copy of byte
    and dl, 00100000b       ; DL = bit 5 (cleared others)
    shr dl, 5               ; DL = bit 5 value (0 or 1)
    
    ; AND bit 2 and bit 5
    and cl, dl              ; CL = (bit2) AND (bit5) = 0 or 1
    
    ; Clear bit 6 first
    mov al, byte ptr [si]
    and al, 10111111b       ; Clear bit 6
    
    ; Place result in bit 6
    cmp cl, 1               ; If result is 1
    jne skip_set_bit6
    
    or al, 01000000b        ; Set bit 6
    
skip_set_bit6:
    mov byte ptr [si], al   ; Write back

    inc si
    jmp process_loop

done:
    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
