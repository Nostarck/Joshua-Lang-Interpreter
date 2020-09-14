from Scanner import Scanner
from Parser import Parser
import sys
'''
Para iniciar se llama python3 Main.py [codigo fuente]
'''
archivo_txt = open(sys.argv[1],'r')
texto = archivo_txt.read()
archivo_txt.close()

scanner = Scanner(texto)
if(scanner.error == False):
	parser  = Parser(scanner.tokens_encontrados)


