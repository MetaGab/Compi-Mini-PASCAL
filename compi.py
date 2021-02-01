from lexicon import Lexicon
from syntax import Syntax
from assembly import Assembler
import os
import subprocess



'''
i = 533
codes = os.listdir("errors")
file = os.path.join("errors", codes[i-500])

'''
file = "codes//primos.txt"
lexico = Lexicon(file, print_result=False)
if not lexico.error_found:
    print(" ---- ¡Análisis Léxico Completado! ----")
    sintaxis = Syntax(lexico.head, print_result=False)
    if not sintaxis.error_found:
        print(" ---- ¡Análisis Sintáctico/Semántico Completado! ----")
        print(sintaxis.polish_code)
        assembly = Assembler(sintaxis.vars, sintaxis.polish_code, sintaxis.type_system)
        subprocess.call('"C:\\Users\\Gabo Banda\\Documents\\Proyectos\\ASM\\DOSBox.exe" \
            -conf "C:\\Users\\Gabo Banda\\Documents\\Proyectos\\ASM\\compi.conf"')