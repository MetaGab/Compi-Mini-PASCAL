INCLUDE macros.mac
INCLUDE fp.a
INCLUDELIB stdlib.lib
DOSSEG
.MODEL SMALL
STACK 100h
.DATA
			MAXLEN DB 254
			LEN DB 0
			MSG   DB 254 DUP(?)
			BUFFER		DB 8 DUP('$')
			BUFFERTEMP	DB 8 DUP('$')
			BLANCO	DB '#'
			BLANCOS	DB '$'
			MENOS	DB '-$'
			COUNT	DW 0
			NEGATIVO	DB 0
			BUF	DW 10
			LISTAPAR	LABEL BYTE
			LONGMAX	DB 254
			TRUE	DW 1
			FALSE DW 0
			INTRODUCIDOS	DB 254 DUP ('$')
			MULT10	DW 1
			s_true	DB 'true$'
			s_false DB 'false$'
			a   DD 0
			b   DD 0
			FPStr  DD MSG
			num_2 DD 0
.CODE
.386
BEGIN:
			MOV     AX, @DATA
			MOV     DS, AX
CALL  COMPI
			MOV AX, 4C00H
			INT 21H
COMPI  PROC
	READ
	les	di, FPStr
	atof
	les di, num_2
	sdfpa
	mov	di, seg MSG
	mov	es, di
	lea	di, MSG
	mov	ah, 2		;Two digits after "."
	mov	al, 10		;Use a total of ten positions
	ftoa
	WRITE MSG
	WRITELN
		ret
COMPI  ENDP
END BEGIN