; print hello world

    .model small
    .stack 200h   
    .data
message db "HELLO WORLD",0Ah,0Dh,07h,'$'  
message2 db "GOODBYE HEAVEN",'$' 
; 07h - sound, we can delete  
; 0A+0Dh - to next string
    .code
start:
 mov ax,@data
 mov ds,ax
 ;mov dx, offset message  
 lea dx,message
 mov ah,9
 int 21h  
 
 lea dx,message2
 mov ah,9
 int 21h 
 
 mov ax,4C00h
 int 21h

end start