a= """
add si,2
	 input:
			 dec cx
			 push cx
			 mov dx,offset mess2
			 mov ah,9h
			 int 21h					;提示输入数组数量
			 mov cx,0						
		 	 mov ah,1h
		 	 int 21h			
			 mov ah,'-'
			 cmp al,ah
			 jz ifmem
			 inc cx
			 mov ah,00h
			 sub al,'0'
			 push ax
			 jmp izmem					;读到负号，特殊处理
	 	ifmem:
	 		lif:
	 			 mov ah,1h
				 int 21h
				 mov ah,0dh
	 			 cmp al,ah
	 			 jz life			;读到回车，跳出读取
				 inc cx
				 mov ah,00h
				 sub al,'0'
				 push ax
				jmp lif	
			life:	
				 mov bl,1
				 mov dx,0
				 endfmem:
				 	pop ax
				 	mul bl
				 	sub dx,ax
				 	mov al,bl
				 	mov bl,10
				 	mul bl
				 	mov bl,al
				 	loop endfmem
			 	 add [si],dx
			 	 jmp last
		izmem:
	 		liz:
	 			 mov ah,1h
				 int 21h
				 mov ah,0dh
	 			 cmp al,ah
	 			 jz lize			;读到回车，跳出读取
				 inc cx
				 mov ah,00h
				 sub al,'0'
				 push ax
				jmp liz
			lize:	
				 mov bl,1
				 mov dx,0
				 endzmem:
				 	pop ax
				 	mul bl
				 	add dx,ax
				 	mov al,bl
				 	mov bl,10
				 	mul bl
				 	mov bl,al
				 	loop endzmem
			 	 add [si],dx
			 	 jmp last
		last:
		add si,2
		pop cx
		mov ax,0
		cmp cx,ax
		jnz input
"""

print(a.upper())