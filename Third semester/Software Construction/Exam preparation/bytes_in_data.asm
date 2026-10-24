; ============================================
; SORT BYTES IN MEMORY ($8900-$89FF)
; Ascending: positive first, then negative
; ============================================

.MODEL small
.STACK 100h

.DATA
    positive_count  db 0
    negative_count  db 0

.CODE

start:
    ; Setup segments
    mov ax, 8900h
    mov ds, ax              ; DS points to data at $8900

    ; ===== STEP 1: Count positive and negative =====
    xor si, si              ; SI = 0 (offset)
    mov word ptr positive_count, 0

count_loop:
    cmp si, 256             ; End of range?
    jge sort_start
    
    mov al, byte ptr [si]
    cmp al, 0               ; Check sign
    jl is_negative
    
    inc byte ptr positive_count
    jmp next_count
    
is_negative:
    inc byte ptr negative_count
    
next_count:
    inc si
    jmp count_loop

    ; ===== STEP 2: Sort positives (bubble sort) =====
sort_start:
    mov cl, positive_count
    cmp cl, 1
    jle sort_negatives_start
    
    dec cl                  ; n-1 passes

sort_positive_outer:
    cmp cl, 0
    jle sort_negatives_start
    
    xor si, si
    mov bl, positive_count
    dec bl
    
sort_positive_inner:
    cmp bl, 0
    jle sort_positive_next
    
    mov al, byte ptr [si]
    mov ah, byte ptr [si+1]
    cmp al, ah
    jle no_swap_pos
    
    mov byte ptr [si], ah
    mov byte ptr [si+1], al
    
no_swap_pos:
    inc si
    dec bl
    jmp sort_positive_inner
    
sort_positive_next:
    dec cl
    jmp sort_positive_outer

    ; ===== STEP 3: Sort negatives (bubble sort) =====
sort_negatives_start:
    mov dh, positive_count
    xor dl, dl              ; DX for SI offset calculation
    mov si, 0
    mov cl, dl
    mov al, positive_count
    mov si, ax              ; SI = start of negative section
    
    mov cl, negative_count
    cmp cl, 1
    jle sort_done
    
    dec cl

sort_negative_outer:
    cmp cl, 0
    jle sort_done
    
    mov bl, negative_count
    dec bl
    
sort_negative_inner:
    cmp bl, 0
    jle sort_negative_next
    
    mov al, byte ptr [si]
    mov ah, byte ptr [si+1]
    cmp al, ah              ; -100 < -50 > swap
    jle no_swap_neg
    
    mov byte ptr [si], ah
    mov byte ptr [si+1], al
    
no_swap_neg:
    inc si
    dec bl
    jmp sort_negative_inner
    
sort_negative_next:
    dec cl
    jmp sort_negative_outer

sort_done:
    ; === Exit ===
    mov ax, 4C00h
    int 21h

END start
