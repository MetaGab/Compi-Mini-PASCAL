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
			MSG_DD   DD MSG            
			BUFFER		DB 8 DUP('$')
			CADENA_NUM		DB 10 DUP('$')
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
			NEG_STR DB '-1$'
			NEG_PTR DD NEG_STR
			n   DW ?
			i   DW ?
			j   DW ?
			k   DW ?
			fin   DW ?
			s_0   DB "Introduzca un numero entero positivo :","$"
			t0   DW ?
			s_1   DB "Los factores primos de ","$"
			s_2   DB " son: ","$"
			t1   DW ?
			t2   DW ?
			t3   DW ?
			t4   DW ?
			t5   DW ?
			t6   DW ?
			t7   DW ?
			t8   DW ?
			t9   DW ?
			t10   DW ?
			t11   DW ?
			t12   DW ?
			s_3   DB "    ","$"
			t13   DW ?
			t14   DW ?
.CODE
.386
BEGIN:
			MOV     AX, @DATA
			MOV     DS, AX
CALL  COMPI
			MOV AX, 4C00H            
			INT 21H
COMPI  PROC
	E0:
	clrscr
	WRITE s_0
	READ
	ASCTODEC n, MSG
	WRITELN
	J0:
	I_MAYOR n, 0, t0
	JF t0, E0
	H0:
	WRITE s_1
	ITOA BUFFER, n
	WRITE BUFFERTEMP
	WRITE s_2
	WRITELN
	I_ASIGNAR i, 0
	G0:
	I_MENORIGUAL i, n, t1
	JF t1, F0
	RESTA n, i, t2
	I_ASIGNAR k, t2
	I_IGUAL k, 1, t3
	JF t3, A0
	JMP F0
	JMP B0
	A0:
	B0:
	MODULO n, k, t4
	I_IGUAL t4, 0, t5
	JF t5, A1
	I_ASIGNAR fin, false
	RESTA k, 1, t6
	I_ASIGNAR j, t6
	D0:
	I_MAYOR k, 1, t7
	I_NOT fin, t8
	I_AND t7, t8, t9
	JF t9, C0
	MODULO k, j, t10
	I_IGUAL t10, 0, t11
	JF t11, A2
	I_ASIGNAR fin, true
	JMP B2
	A2:
	B2:
	I_IGUAL j, 1, t12
	JF t12, A3
	WRITE s_3
	ITOA BUFFER, k
	WRITE BUFFERTEMP
	WRITELN
	JMP B3
	A3:
	B3:
	RESTA j, 1, t13
	I_ASIGNAR j, t13
	JMP D0
	C0:
	JMP B1
	A1:
	B1:
	I0:
	SUMAR i, 1, t14
	I_ASIGNAR i, t14
	JMP G0
	F0:
		ret
COMPI  ENDP
END BEGIN