import re

'''
Crea expresiones regulares con cada uno de los tokens de lenguaje
esta clase va a leer el codigo fuente y va a ir sacando los tokens uno a uno, si hubiera 
una palabra que no sea un token se activara una bandera indicando que hubo un error y que 
se escribieron palabras que no son tokens, de lo contrario si todo pasa bien va a devolver 
una lista con todos los tokens encontrados en el codigo fuente, la lista sera una lista de 
pares donde el primer elemento es el tipo de token, y el segundo elemento sera el valor
encontrado para ese token
por ejemeplo ["operador_logico",'>'] seria un elemento de la lista 
'''
class Scanner:
	def __init__(self,texto):
		self.texto = texto 

		
		self.token_tipo_variable = r'portero|defensa|delantero'
		self.token_int = r'[0-9]+'
		self.token_bool = r'true|false'
		self.token_string = r'"[ A-Za-z0-9]*"'
		self.token_cambio = r'cambio'
		self.token_operador = r'-|\+|/|\*'
		self.token_operador_logico = r'==|>=|<=|>|<'
		self.token_variable = r'jugador'
		self.token_instruccion = r'!'
		self.token_coma = r','
		self.token_llave_izquierda = r'\['
		self.token_llave_derecha = r']'
		self.token_while = r'cletear'
		self.token_parentesis_izquierdo = r'\('
		self.token_parentesis_derecho = r'\)'
		self.token_if = r'titular'
		self.token_else = r'suplente'
		self.token_print = r'play'
		self.token_input = r'gol'
		self.token_strlen = r'acorde'
		self.token_strcpy = r'quemar'
		self.token_nombre_variable = r'[A-Za-z0-9]+'
		self.token_error = r'[\S]+'


		self.gramatica = r'('+self.token_tipo_variable+')|('+self.token_int+')|('+self.token_bool+')|('+self.token_string+')|('+self.token_cambio+')|('+self.token_operador+')|('+self.token_operador_logico+')|('+self.token_variable+')|('+self.token_instruccion+')|('+self.token_coma+')|('+self.token_llave_izquierda+')|('+self.token_llave_derecha+')|('+self.token_while+')|('+self.token_parentesis_izquierdo+')|('+self.token_parentesis_derecho+')|('+self.token_if+')|('+self.token_else+')|('+self.token_print+')|('+self.token_input+')|('+self.token_strlen+')|('+self.token_strcpy+')|('+self.token_nombre_variable+')|('+self.token_error+')'
		self.tokens_encontrados = []
		self.tokens_erroneos =[]
		self.error = False

		self.buscar_tokens()


	def buscar_tokens(self):
		self.gramatica = re.compile(self.gramatica)
		matches = self.gramatica.finditer(self.texto)
		for match in matches:
			if(type(match.group(1)) == str):
				self.tokens_encontrados += [["TIPO",match.group(1)]]
			elif(type(match.group(2)) == str):
				self.tokens_encontrados += [["INT",match.group(2)]]
			elif(type(match.group(3)) == str):
				self.tokens_encontrados += [["BOOL",match.group(3)]]
			elif(type(match.group(4)) == str):
				self.tokens_encontrados += [["STRING",match.group(4)]]
			elif(type(match.group(5)) == str):
				self.tokens_encontrados += [["CAMBIO",match.group(5)]]
			elif(type(match.group(6)) == str):
				self.tokens_encontrados += [["OPERADOR",match.group(6)]]
			elif(type(match.group(7)) == str):
				self.tokens_encontrados += [["OPERADOR_LOGICO",match.group(7)]]
			elif(type(match.group(8)) == str):
				self.tokens_encontrados += [["DECLARACION",match.group(8)]]
			elif(type(match.group(9)) == str):
				self.tokens_encontrados += [["FIN",match.group(9)]]
			elif(type(match.group(10)) == str):
				self.tokens_encontrados += [["COMA",match.group(10)]]
			elif(type(match.group(11)) == str):
				self.tokens_encontrados += [["LLAVE_IZQUIERDA",match.group(11)]]
			elif(type(match.group(12)) == str):
				self.tokens_encontrados += [["LLAVE_DERECHA",match.group(12)]]
			elif(type(match.group(13)) == str):
				self.tokens_encontrados += [["WHILE",match.group(13)]]
			elif(type(match.group(14)) == str):
				self.tokens_encontrados += [["PARENTESIS_IZQUIERDO",match.group(14)]]
			elif(type(match.group(15)) == str):
				self.tokens_encontrados += [["PARENTESIS_DERECHO",match.group(15)]]
			elif(type(match.group(16)) == str):
				self.tokens_encontrados += [["IF",match.group(16)]]
			elif(type(match.group(17)) == str):
				self.tokens_encontrados += [["ELSE",match.group(17)]]
			elif(type(match.group(18)) == str):
				self.tokens_encontrados += [["PRINT",match.group(18)]]
			elif(type(match.group(19)) == str):
				self.tokens_encontrados += [["INPUT",match.group(19)]]
			elif(type(match.group(20)) == str):
				self.tokens_encontrados += [["STRLEN",match.group(20)]]
			elif(type(match.group(21)) == str):
				self.tokens_encontrados += [["STRCPY",match.group(21)]]
			elif(type(match.group(22)) == str):
				self.tokens_encontrados += [["NOMBRE",match.group(22)]]
			elif(type(match.group(23)) == str):
				print("ERROR Token no reconocido "+match.group(23))
				self.error = True
			
	def mostrar_tokens(self):
		cuenta = 0
		print("Tokens encontrados: \n")
		for token in self.tokens_encontrados:
			print(str(cuenta)+" "+str(token))
			cuenta +=1
		print()

