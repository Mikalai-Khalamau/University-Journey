.model small
.stack 100h
.data 
a db 5 dup(?)
b db "Input an Array of 5 Numbers(0-9): $"
c db "Press 0 for Bubble Sort: $"
d db "Press 1 for Selection Sort $"

.code
main proc       
    mov ax, @data
    mov ds, ax 
    
    ;1st statement print
    mov ah, 9
    lea dx, b
    int 21h
    
    ;array input phase
    lea si, a
    mov cx, 5             
    input_array:
    mov ah, 1
    int 21h
    sub al, 48
    mov [si], al
    inc si
    mov ah, 2
    mov dl, " "
    int 21h    
    loop input_array
    
    ;new_line     
    mov ah, 2
    mov dl, 10
    int 21h
    mov dl, 13
    int 21h
     
    
    ;2nd statement print  
    mov ah, 9
    lea dx, c
    int 21h   
    
    ;new_line     
    mov ah, 2
    mov dl, 10
    int 21h
    mov dl, 13
    int 21h
    
    ;3rd statement print  
    mov ah, 9
    lea dx, d ;Selection Sort
    int 21h  
    
    
    ;new_line     
    mov ah, 2
    mov dl, 10
    int 21h
    mov dl, 13
    int 21h
  
    
    
    ;if input is 0, then go for bubble sort    
    mov ah, 1
    int 21h
    sub al, 48
    cmp al, 0
    je BubbleSort
    ;if input is 1, then go for bubble sort 
    cmp al, 1
    je SelectionSort 
 
    jne exit    

    ;after completting bubble sort, print the array
    return:    
    mov cx, 5
    lea si, a
    mov ah, 2
    
    ;new_line 
    mov ah, 2
    mov dl, 10
    int 21h
    mov dl, 13
    int 21h
       
    
    
    ;print_loop
    print_array:
    mov dl, [si]
    add dl, 48
    int 21h
    inc si
    mov ah, 2
    mov dl, " "
    int 21h 
    loop print_array
    
     
    main endp
    jmp exit
    

;def buble_sort(a):
;  length = len(a)
;  i = 0
;  while i < length:
;    j = 0
;    while j < length-i-1:
;      if a[j] > a[j+1]:
;        temp = a[j]
;        a[j] = a[j+1]
;        a[j+1] = temp
;     j+=1
;    i+=1
;  return a
;a= [2, 5, 3, 4, 10, 9, 13, 6, 20, 15]
;print(buble_sort(a)) 
BubbleSort: 
    mov cx, 5                ;length=5
    sub cx, 1                ;length=4 for avoiding array indices error   
    i:                       ;while i < length:
    mov bx, cx
    mov si, 0 
    j:                       ;while j < length-i-1:
    mov al, a[si]
    ;mov bl, a[si+1]
    mov ah, a[si+1]
    ;cmp al, bl    
    cmp al, ah
    jl no_swap    
    ;swapping
    mov al, a[si]            ;temp = a[j]
    ;mov al, a[si+1]
    mov ah, a[si+1]          ;temp1 = a[j+1]
    mov a[si], ah            ;a[j] = a[j+1] = temp1
    mov a[si+1], al          ;a[j+1] = temp    
    ;loop phase next
    no_swap:
    inc si                   ;array_index/j+=1
    dec bx                   ;j<length-i-1       
    jnz j                    ;if j!=0 loop else exit
    ;loop of i
    aa:  
    loop i                   ;i decrement from 5 to 0
    ;go back to main function to print the array
    jmp return
    
;def selection_sort(a):
;  i = 0
;  while i < len(a)-1:
;    j = i + 1
;    index_min = i
;    while j < len(a):
;      if a[j] < a[index_min]:
;        index_min = j ;2
;      j+=1
;    if index_min != i:
;      temp = a[i]
;      a[i] = a[index_min]
;      a[index_min] = temp        
;    i += 1
;  return a 
;a=[2, 5, 3, 4, 6, 10, 7]
;print(selection_sort(a))

    
SelectionSort:
    MOV CX, 5 ;length
    DEC CX

    ;OuterLoop:
    MOV SI, 0        ;si=i
    
    iLoop:
    CMP SI, CX ; Compare i with length of array-1 ;while i < len(a)-1:
    JGE NextPass
    
    MOV DI, SI ; index_min = i 
   
    
    MOV BX, DI ; j = i 
    INC BX     ; j+=1        ;j = i+1
  
    jLoop:
    CMP BX, 5 ; Compare j with length of array  ;while j < len(a):
    JGE InnerLoopEnd
    

    MOV AL, a[DI]   ;al=a[index_min]                 ;a[index_min]
    MOV DL, a[BX]   ;dl=a[j]                         ;a[j]
    
    CMP DL, AL ; Compare a[j] with a[index_min]            ;if a[j] < a[index_min]:
  
  
  
    JGE NoSwap ; If a[j] >= a[index_min], no swap needed
    
  
    XCHG AL, DL     ;index_min = j  ;temp = al, al = dl, dl = temp ;al=a[i], dl=a[index_min]        ; temp=a[i]
    MOV a[DI], AL   ;a[index_min]= a[i]                                             ; a[i]=a[index_min]
    MOV a[BX], DL   ;a[i]=a[index_min]                                              ; a[index_min]=temp
    
    NoSwap:
    INC BX ; j+=1
    JMP jLoop
    
    InnerLoopEnd:
    INC SI ; i+=1
    JMP iLoop
    
    NextPass:
    jmp return


    
         
    
  
    
    
    
    
    exit:
end main