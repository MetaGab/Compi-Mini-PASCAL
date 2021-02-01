from node import Node
class Assembler:
    def __init__(self, variables, code, system):
        self.variables = variables
        self.type_id = {"integer": 0, "real":1, "string":2, "bool": 3}
        self.token_vars = {101: "integer", 102:"real", 119:"string", 213:"bool", 214:"bool"}
        symbol_to_macro = {"+": "SUMAR", "-": "RESTA", "*": "MULTI", "div": "DIVIDE", "<": "I_MENOR",
            ">": "I_MAYOR", ">=": "I_MAYORIGUAL", "<>": "I_DIFERENTES", "=": "I_IGUAL", "<=": "I_MENORIGUAL", 
            "and": "I_AND", "or": "I_OR", "not": "I_NOT", "s-" : "SIGNOMENOS", "%": "MODULO"
        }
        string_macros = {"<>": "S_DIFERENTES", "=": "S_IGUAL"}
        float_macros = {"+": "F_SUMAR", "-": "F_RESTA", "*": "F_MULTI", "div": "F_DIVIDE", "<": "F_MENOR",
            ">": "F_MAYOR", ">=": "F_MAYORIGUAL", "<>": "F_DIFERENTES", "=": "F_IGUAL", "<=": "F_MENORIGUAL"}
        var_stack = []
        temp_counter = 0
        string_counter = 0
        float_counter = 0
        strings = {}
        floats = {}
        assembly_variable = "INCLUDE macros.mac\nINCLUDE fp.a\nINCLUDELIB stdlib.lib\nDOSSEG\n.MODEL SMALL\n\
            STACK 100h\n.DATA\n\t\t\tMAXLEN DB 254\n\t\t\tLEN DB 0\n\t\t\tMSG   DB 254 DUP(?)\n\t\t\tMSG_DD   DD MSG\
            \n\t\t\tBUFFER		DB 8 DUP('$')\n\t\t\tCADENA_NUM		DB 10 DUP('$')\n\t\t\tBUFFERTEMP	DB 8 DUP('$')\
            \n\t\t\tBLANCO	DB '#'\n\t\t\tBLANCOS	DB '$'\n\t\t\tMENOS	DB '-$'\n\t\t\tCOUNT	DW 0\n\t\t\tNEGATIVO	DB 0\
            \n\t\t\tBUF	DW 10\n\t\t\tLISTAPAR	LABEL BYTE\n\t\t\tLONGMAX	DB 254\n\t\t\tTRUE	DW 1\n\t\t\tFALSE DW 0\
            \n\t\t\tINTRODUCIDOS	DB 254 DUP ('$')\n\t\t\tMULT10	DW 1\n\t\t\ts_true	DB 'true$'\n\t\t\ts_false DB 'false$'\
            \n\t\t\tNEG_STR DB '-1$'\n\t\t\tNEG_PTR DD NEG_STR\n"
        assembly_program = ".CODE\n.386\nBEGIN:\n\t\t\tMOV     AX, @DATA\n\t\t\tMOV     DS, AX\nCALL  COMPI\n\t\t\tMOV AX, 4C00H\
            \n\t\t\tINT 21H\nCOMPI  PROC\n"
        i = 0
        for v in variables:
            if variables[v]["used"]:
                if variables[v]["type"] in ["integer", "bool"]:
                    assembly_variable += "\t\t\t{0}   DW ?\n".format(v)
                elif variables[v]["type"] == "string":
                    assembly_variable += "\t\t\t{0}   DB 254 DUP('$')\n".format(v)
                elif variables[v]["type"] == "real":
                    assembly_variable += "\t\t\t{0}   DD {1}.00001\n".format(v,i)
                    i += 1

        for p in code:
            if hasattr(p, "token"):
                if p.token in [100, 101, 102, 119, 213, 214]:
                    if p.token == 119:
                        assembly_variable += '\t\t\ts_{0}   DB {1},"$"\n'.format(string_counter, p.lexeme)
                        strings[p.lexeme] = "s_{0}".format(string_counter)
                        string_counter += 1
                    elif p.token == 102:
                        assembly_variable += '\t\t\tf_{0}   DB "{1}","$"\n'.format(float_counter, p.lexeme)
                        assembly_variable += '\t\t\tf_{0}_ptr   DD f_{0}\n'.format(float_counter)
                        floats[p.lexeme] = "f_{0}".format(float_counter)
                        float_counter += 1
                    var_stack.append(p)
                elif p.lexeme == "s+":
                    pass
                elif p.lexeme in ["s-", "not"]:
                    op1 = var_stack.pop()
                    temp_var = "t{}".format(temp_counter)
                    result = system[p.lexeme][self.get_type(op1)]
                    variables[temp_var] = {"type": result, "used":True}
                    var_stack.append(Node(temp_var, 100, 0))
                    if self.get_type(op1) == 1:
                        if op1.token == 100:
                            assembly_variable += "\t\t\t{0}   DD 0\n".format(temp_var)
                            assembly_program += "\tLES DI, NEG_PTR\n"
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tLES DI, {0}\n".format(op1.lexeme)
                            assembly_program += "\tLSFPO\n"
                        else:
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op1.lexeme])
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tXACCOP\n"
                            assembly_variable += "\t\t\t{0}   DD 0\n".format(temp_var)
                            assembly_program += "\tLES DI, NEG_PTR\n"
                            assembly_program += "\tATOF\n"
                        assembly_program += "\tFPMUL\n"
                        assembly_program += "\tLES DI, {0}\n".format(temp_var)
                        assembly_program += "\tSSFPA\n"

                    else:
                        assembly_variable += "\t\t\t{0}   DW ?\n".format(temp_var)
                        assembly_program += "\t{0} {1}, {2}\n".format(symbol_to_macro[p.lexeme], op1.lexeme, temp_var)
                    temp_counter += 1
                elif p.lexeme == "read":
                    op1 = var_stack.pop()
                    if self.get_type(op1) == 0:
                        assembly_program += "\tREAD\n"
                        assembly_program += "\tASCTODEC {0}, MSG\n".format(op1.lexeme)
                    elif self.get_type(op1) == 1:
                        assembly_program += "\tREAD\n"
                        assembly_program += "\tLES DI, MSG_DD\n"
                        assembly_program += "\tATOF\n"
                        assembly_program += "\tLES DI, {0}\n".format(op1.lexeme)
                        assembly_program += "\tSSFPA\n"
                    elif self.get_type(op1) == 2:
                        assembly_program += "\tREAD\n"
                        assembly_program += "\tS_ASIGNAR {0}, MSG\n".format(op1.lexeme)
                    elif self.get_type(op1) == 3:
                        assembly_program += "\tREAD\n"
                        assembly_program += "\tS_IGUAL s_true, MSG, {0}\n".format(op1.lexeme)
                    assembly_program += "\tWRITELN\n"
                elif p.lexeme in "write":
                    op1 = var_stack.pop()
                    if self.get_type(op1) == 0:
                        assembly_program += "\tITOA BUFFER, {0}\n".format(op1.lexeme)
                        assembly_program += "\tWRITE BUFFERTEMP\n"
                    elif self.get_type(op1) == 1:
                        if op1.token == 100:
                            assembly_program += "\tLES DI, {0}\n".format(op1.lexeme)    
                            assembly_program += "\tLSFPA\n"
                        else:
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op1.lexeme])
                            assembly_program += "\tATOF\n"
                        assembly_program += "\tMOV DI, SEG CADENA_NUM\n"
                        assembly_program += "\tMOV ES, DI\n"
                        assembly_program += "\tLEA DI, CADENA_NUM\n"
                        assembly_program += "\tMOV AH, 2\n"
                        assembly_program += "\tMOV AL, 10\n"
                        assembly_program += "\tFTOA\n"
                        assembly_program += "\tWRITE CADENA_NUM\n"
                    elif self.get_type(op1) == 2:
                        if op1.token == 100:
                            assembly_program += "\tWRITE {0}\n".format(op1.lexeme)
                        else:
                            assembly_program += "\tWRITE {0}\n".format(strings[op1.lexeme])
                    elif self.get_type(op1) == 3:
                        if op1.token == 100:
                            assembly_program += "\tWRITEBOOL {0}\n".format(op1.lexeme)
                        else:
                            assembly_program += "\tWRITE s_{0}\n".format(op1.lexeme)
                elif p.lexeme == ":=":
                    op2 = var_stack.pop()
                    op1 = var_stack.pop()
                    if variables[op1.lexeme]["type"] in ["integer", "bool"]:
                        if self.get_type(op1) == 0 and self.get_type(op2) == 1:
                            if op2.token == 102:
                                assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op2.lexeme])
                                assembly_program += "\tATOF\n"
                            else:
                                assembly_program += "\tLES DI, {0}\n".format(op2.lexeme)
                                assembly_program += "\tLSFPA\n"
                            assembly_program += "\tFTOI\n"
                            assembly_program += "\tI_ASIGNAR {0}, AX\n".format(op1.lexeme)
                        else:
                            assembly_program += "\tI_ASIGNAR {0}, {1}\n".format(op1.lexeme, op2.lexeme)
                    elif variables[op1.lexeme]["type"] == "real":
                        if self.get_type(op1) == 1 and self.get_type(op2) == 0:
                            assembly_program += "\tMOV AX, {0}\n".format(op2.lexeme)
                            assembly_program += "\tITOF\n"
                        else:
                            if op2.token == 100:
                                assembly_program += "\tLES DI, {0}\n".format(op2.lexeme)
                                assembly_program += "\tLSFPA\n"
                            else:
                                assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op2.lexeme])
                                assembly_program += "\tATOF\n"
                        assembly_program += "\tLES DI, {0}\n".format(op1.lexeme)
                        assembly_program += "\tSSFPA\n"

                    elif variables[op1.lexeme]["type"] == "string":
                        if op2.token == 100:
                            assembly_program += "\tS_ASIGNAR {0}, {1}\n".format(op1.lexeme, op2.lexeme)
                        else:
                            assembly_program += "\tS_ASIGNAR {0}, {1}\n".format(op1.lexeme, strings[op2.lexeme])
                elif p.lexeme in ["=", "<>"]:
                    op2 = var_stack.pop()
                    op1 = var_stack.pop()
                    temp_var = "t{}".format(temp_counter)
                    variables[temp_var] = {"type": "bool", "used":True}
                    temp_counter += 1
                    assembly_variable += "\t\t\t{0}   DW ?\n".format(temp_var)
                    if self.get_type(op1) == 2:
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format(string_macros[p.lexeme], 
                        op1.lexeme if op1.token == 100 else strings[op1.lexeme], 
                        op2.lexeme if op2.token == 100 else strings[op2.lexeme], temp_var)
                    elif self.get_type(op1) in [0,3] and self.get_type(op2) in [0,3]:
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format(symbol_to_macro[p.lexeme], op1.lexeme, op2.lexeme, temp_var)
                    else:
                        if self.get_type(op1) == 0:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tMOV AX, {0}\n".format(op1.lexeme)
                            assembly_program += "\tITOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op1.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        elif op1.token == 102:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op1.lexeme])
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op1.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        if self.get_type(op2) == 0:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tMOV AX, {0}\n".format(op2.lexeme)
                            assembly_program += "\tITOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op2.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        elif op2.token == 102:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op2.lexeme])
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op2.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format(float_macros[p.lexeme], op1.lexeme, op2.lexeme, temp_var)
                    var_stack.append(Node(temp_var, 100, 0))
                elif p.token == 228:
                    assembly_program += "\tclrscr\n"
                else:
                    op2 = var_stack.pop()
                    op1 = var_stack.pop()
                    result = system[p.lexeme][self.get_type(op1)][self.get_type(op2)]
                    temp_var = "t{}".format(temp_counter)
                    variables[temp_var] = {"type": result, "used":True}
                    temp_counter += 1
                    if result in ["integer", "bool"]:
                        assembly_variable += "\t\t\t{0}   DW ?\n".format(temp_var)
                    elif result == "real":
                        assembly_variable += "\t\t\t{0}   DD {1}.000001\n".format(temp_var, i)
                        i+=1
                    if self.get_type(op1) in [0,3] and self.get_type(op2) in [0,3] : 
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format(symbol_to_macro[p.lexeme], op1.lexeme, op2.lexeme, temp_var)
                    elif result == "string":
                        assembly_variable += "\t\t\t{0}   DB 254 DUP('$')\n".format(temp_var)
                        if self.get_type(op1) == 2:
                            op1 = op1.lexeme if op1.token == 100 else strings[op1.lexeme]
                        elif self.get_type(op1) == 0:
                            assembly_program += "\tITOA BUFFER, {0}\n".format(op1.lexeme)
                            op1 = "BUFFERTEMP"
                        elif self.get_type(op1) == 1:
                            if op1.token == 100:
                                assembly_program += "\tLES DI, {0}\n".format(op1.lexeme)    
                                assembly_program += "\tLSFPA\n"
                            else:
                                assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op1.lexeme])
                                assembly_program += "\tATOF\n"
                            assembly_program += "\tMOV DI, SEG CADENA_NUM\n"
                            assembly_program += "\tMOV ES, DI\n"
                            assembly_program += "\tLEA DI, CADENA_NUM\n"
                            assembly_program += "\tMOV AH, 2\n"
                            assembly_program += "\tMOV AL, 10\n"
                            assembly_program += "\tFTOA\n"
                            op1 = "CADENA_NUM"
                        if self.get_type(op2) == 2:
                            op2 = op2.lexeme if op2.token == 100 else strings[op2.lexeme]
                        elif self.get_type(op2) == 0:
                            assembly_program += "\tITOA BUFFER, {0}\n".format(op2.lexeme)
                            op2 = "BUFFERTEMP"
                        elif self.get_type(op2) == 1:
                            if op2.token == 100:
                                assembly_program += "\tLES DI, {0}\n".format(op2.lexeme)    
                                assembly_program += "\tLSFPA\n"
                            else:
                                assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op2.lexeme])
                                assembly_program += "\tATOF\n"
                            assembly_program += "\tMOV DI, SEG CADENA_NUM\n"
                            assembly_program += "\tMOV ES, DI\n"
                            assembly_program += "\tLEA DI, CADENA_NUM\n"
                            assembly_program += "\tMOV AH, 2\n"
                            assembly_program += "\tMOV AL, 10\n"
                            assembly_program += "\tFTOA\n"
                            op2 = "CADENA_NUM"
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format("CONCATENAR", op1, op2, temp_var)
                    elif self.get_type(op1) == 1 or self.get_type(op2) == 1:
                        if self.get_type(op1) == 0:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tMOV AX, {0}\n".format(op1.lexeme)
                            assembly_program += "\tITOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op1.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        elif op1.token == 102:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op1.lexeme])
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op1.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        if self.get_type(op2) == 0:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tMOV AX, {0}\n".format(op2.lexeme)
                            assembly_program += "\tITOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op2.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        elif op2.token == 102:
                            assembly_variable += "\t\t\tt{0}   DD {1}.000001\n".format(temp_counter, i)
                            assembly_program += "\tLES DI, {0}_ptr\n".format(floats[op2.lexeme])
                            assembly_program += "\tATOF\n"
                            assembly_program += "\tLES DI, t{0}\n".format(temp_counter)
                            assembly_program += "\tSSFPA\n"
                            op2.lexeme = "t{0}".format(temp_counter)
                            i+=1
                            temp_counter += 1
                        assembly_program += "\t{0} {1}, {2}, {3}\n".format(float_macros[p.lexeme], op1.lexeme, op2.lexeme, temp_var)
                    var_stack.append(Node(temp_var, 100, 0))
            elif "BRF" in p:
                assembly_program += "\tJF {0}, {1}\n".format(var_stack.pop().lexeme,p.split("-")[1])
            elif "BRI" in p:
                assembly_program += "\tJMP {0}\n".format(p.split("-")[1])
            elif p == "writeln":
                assembly_program += "\tWRITELN\n"
            else:
                assembly_program += "\t{0}\n".format(p)
        assembly_program += "\t\tret\nCOMPI  ENDP\nEND BEGIN"
        file = open("RESULT\\red.asm", "w+")
        file.write(assembly_variable)
        file.write(assembly_program)

    def get_type(self, p):
        if p.token == 100:
            return self.type_id[self.variables[p.lexeme]["type"]]
        else:
            return self.type_id[self.token_vars[p.token]]