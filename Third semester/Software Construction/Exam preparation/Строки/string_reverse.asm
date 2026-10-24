; string reverse
    .model small
    .stack 200h
; constants
MAXLEN EQU 200
    .data
string_buffer db MAXLEN
db 0
db MAXLEN dup(0)

message_start db "Program started",0Dh,0Ah,'$'
message_input db "Enter string(max 200 chars)",0Dh,0Ah,'$'
message_output db 0Dh,0Ah,"You entered:",0Dh,0Ah,'$'  
message_error db "Error while input",0Dh,0Ah,'$' 
message_reversed db "Reversed string:",0Dh,0Ah,'$'
           
           
    .code    
; si-start,di-end    
ReverseRange proc
reverse_loop:
cmp si,di
jge reverse_done

mov al,[bx+si]
mov dl,[bx+di]

mov [bx+si],dl
mov [bx+di],al

inc si
dec di
jmp reverse_loop

reverse_done:
ret

ReverseRange endp
    
    
    
    
    
    
start:   
; data segment initialize
mov ax,@data
mov ds,ax    

lea dx,message_start
mov ah,09
int 21h

lea dx,message_input
mov ah,09
int 21h          

lea dx,string_buffer
mov ah,0Ah
int 21h        

lea dx,message_output
mov ah,09
int 21h

mov cl,[string_buffer+1]
mov ch,0
mov si,2


print_loop:
cmp cx,0
je after_print

mov dl,[string_buffer+si]
mov ah,2
int 21h

inc si
dec cx
jmp print_loop

after_print:
; to next string
mov dl,0Dh
mov ah,2
int 21h



; full string reverse
lea bx, string_buffer
mov si,2
mov di,si
mov cl,[string_buffer+1]
mov ch,0
add di,cx
dec di 

call ReverseRange      



;reverse every word

mov cl,[string_buffer+1]
mov ch,0
mov si,2
lea bx,string_buffer


reverse_words_loop:
mov ax,si
sub ax,2
cmp ax,cx
jge reverse_words_done

skip_spaces:
mov ax,si
sub ax,2
cmp ax,cx
jge reverse_words_done

mov al,[bx+si]
cmp al,' '
jne found_word_start

inc si
jmp skip_spaces

found_word_start:
mov di,si

found_word_end:
mov ax,di
sub ax,2
cmp ax,cx
jge found_word_end_done   


mov ax,[bx+di]
cmp al,' '
je found_word_end_done

inc di
jmp found_word_end
                    
                    
found_word_end_done:
dec di

push si
push di
push cx

call ReverseRange

pop cx
pop di
pop si

mov si,di
inc si
jmp reverse_words_loop




reverse_words_done:
lea dx,message_reversed
mov ah,09
int 21h          


mov cl,[string_buffer+1]
mov ch,0
mov si,2

print_result:
cmp cx,0
je after_print_result



mov dl,[string_buffer+si]
mov ah,2
int 21h

inc si
dec cx
jmp print_result        


after_print_result:
mov dl,0Dh
mov ah,2
int 21h

mov dl,0Ah
mov ah,2
int 21h











jmp exit_from_program




exit_from_program:  
mov ax,4C00h
int 21h
end start
