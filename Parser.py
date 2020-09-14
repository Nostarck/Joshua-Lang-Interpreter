from Nodo import *
from Checker import *
'''
Esta clase cuenta con todos los metodos de parseo de cada una de las oraciones de nuestro 
lenguaje, la clase recibe la lista de tokens que encontro el Scanner y comienza a parsear
cada metodo de parseo una vez que intente parsear una oracion, si se parseo bien devolvera
un subarbol y devolvera el puntero del token que sigue por revisar
sino logra parsearse bien devolvera una lista vacia
'''
class Parser():

	tokens_encontrados = []
	AST = 0
	puntero_error = 0
	tokens_len = 0

	def __init__(self,tokens_encontrados):

		self.tokens_encontrados = tokens_encontrados
		self.tokens_len = len(tokens_encontrados)
		self.iniciar()
	
	'''
	Si en algun lugar encuentra un error de sintaxis se llama a esta funcion para 
	imprimir el error, self.puntero_error tendra el ultimo nodo que no se pudo insertar para
	saber cual nodo no hizo match con ninguna oracion del lenguaje
	'''
	def generar_error(self):
		rastreo = ""
		error = "Sintaxis Invalida\n" 
		rastreo_maximo = 6


		if(self.puntero_error == len(self.tokens_encontrados)):
			error += "Hace falta un argumento al final\n"
		self.puntero_error -= 1

		while(self.puntero_error > -1 and rastreo_maximo > -1):
			rastreo = self.tokens_encontrados[self.puntero_error][1] + " "+rastreo
			self.puntero_error-=1
			rastreo_maximo -= 1
		rastreo += "\x1b[1;31m <--- \x1b[1;37m"
		print(rastreo)
		print(error)



	'''
	puntero_token es el nodo actual en el que estoy, cuando el nodo no hace match con alguna oracion
	se llama a esta funcion y se revisa si el token actual es mayor al puntero de error, para actualizar
	el puntero de error para tener siempre el ultimo token que no se pudo insertar
	'''
	def calcular_error(self,puntero_token):
		if(puntero_token > self.puntero_error):
			self.puntero_error = puntero_token

	'''
	Recibe el tipo de token que se sigue en nuestra oracion actual y el puntero del token actual
	si el token actual es del tipo del token de la oracion entonces devuelve true indicando 
	que hubo match, sino hizo match entonces devuelve false
	'''
	def comparar(self,tipo_token,puntero_token):
		if(puntero_token < self.tokens_len):
			if(self.tokens_encontrados[puntero_token][0] == tipo_token):
				return True
		return False
	'''
	luego de llamar a una funcion de parseo, esta devolvera un subarbol, si esta vacio 
	significa que no se pudo parsear y que en algun lugar hubo un error, si el arbol
	no esta vacio significa que se parseo correctamente la oracion de tokens
	'''
	def validar_parseo(self,subarbol):
		if(subarbol == []):
			return False
		return True
	
	'''
	Esta funcion se llama cuanndo los tokens hacen match con el token esperado, se pasa a esta
	funcion el puntero del token, para buscarlo en la lista de tokens encontrados, cuando
	lo encuentre este tendra el tipo de token que es, entonces con una serie de ifs se verifica
	que tipo de nodo hay que crear y se crea dicho nodo, la funcion devuelve el nodo creado
	'''
	def crear_nodo(self,puntero_token):
		tipo_token = self.tokens_encontrados[puntero_token][0]
		valor_token = self.tokens_encontrados[puntero_token][1]
		nodo = []
		if(tipo_token == "DECLARACION"):
			nodo = Nodo_Declaracion(tipo_token,valor_token,[])
		elif(tipo_token == "TIPO"):
			nodo = Nodo_Tipo(tipo_token,valor_token,[])
		elif(tipo_token == "NOMBRE"):
			nodo = Nodo_Nombre(tipo_token,valor_token,[])
		elif(tipo_token == "FIN"):
			nodo = Nodo_Fin(tipo_token,valor_token,[])
		elif(tipo_token == "INT"):
			nodo = Nodo_Int(tipo_token,valor_token,[])
		elif(tipo_token == "BOOL"):
			nodo = Nodo_Bool(tipo_token,valor_token,[])
		elif(tipo_token == "STRING"):
			nodo = Nodo_String(tipo_token,str(valor_token),[])
		elif(tipo_token == "OPERADOR"):
			nodo = Nodo_Operador(tipo_token,valor_token,[])
		elif(tipo_token == "OPERADOR_LOGICO"):
			nodo = Nodo_Operador_Logico(tipo_token,valor_token,[])
		elif(tipo_token == "IF"):
			nodo = Nodo_If(tipo_token,valor_token,[])
		elif(tipo_token == "ELSE"):
			nodo = Nodo_Else(tipo_token,valor_token,[])
		elif(tipo_token == "WHILE"):
			nodo = Nodo_While(tipo_token,valor_token,[])
		elif(tipo_token == "PRINT"):
			nodo = Nodo_Print(tipo_token,valor_token,[])
		elif(tipo_token == "INPUT"):
			nodo = Nodo_Input(tipo_token,valor_token,[])
		elif(tipo_token == "STRLEN"):
			nodo = Nodo_Strlen(tipo_token,valor_token,[])
		elif(tipo_token == "STRCPY"):
			nodo = Nodo_Strcpy(tipo_token,valor_token,[])
		return nodo

	'''
	Esta funcin empieza con el parseo, crea un nodo programa el cual sera el nodo padre
	del AST y luego llama a parsear_programa para empezar con el parseo
	'''
	def iniciar(self):
		self.AST = Nodo_Programa("PROGRAMA","",[])
		puntero_ast = self.AST
		puntero_token = 0
		if(self.parsear_programa(0) == True):
			checker = Checker(self.AST)
			informe = checker.checkear()
			if(type(informe) != str):#no hay errores de tipos
				return
			else:
				print(informe)
		else:
			self.generar_error()
		

	'''
	ahora lo que sigue es el algoritmo recursive descent parsing para todas las oraciones
	de nuestro lenguaje, habra un puntero_token el cual nos ira guiando por el token en el que
	vamos parseando, si una funcion parsea correctamente devuelve un subarbol con los tokens
	correspondientes y sino devuelve una lista vacia
	'''
	def parsear_programa(self,puntero_token):
		self.informe = ""
		subarbol = []
		nuevo_puntero = puntero_token
		parseo_correcto = False
		subarbol,nuevo_puntero = self.parsear_accion(puntero_token)
		if(self.validar_parseo(subarbol)):
			self.AST.agregar_nodo(subarbol)
			puntero_token = nuevo_puntero
			if(puntero_token == self.tokens_len):
				return True
			else:
				return self.parsear_programa(puntero_token)
		else:
			self.calcular_error(puntero_token)
			return False
	
	def parsear_accion(self,puntero_token):
		subarbol = []
		nuevo_puntero = puntero_token
		parseo_correcto = False
		
		#monton de ifs
		subarbol,nuevo_puntero = self.parsear_declaracion(puntero_token)
		if(self.validar_parseo(subarbol)):
			puntero_token = nuevo_puntero
			parseo_correcto = True
		else:
			subarbol,nuevo_puntero = self.parsear_asignacion(puntero_token)
			if(self.validar_parseo(subarbol)):
				puntero_token = nuevo_puntero
				parseo_correcto = True
			else:
				subarbol,nuevo_puntero = self.parsear_if(puntero_token)
				if(self.validar_parseo(subarbol)):
					puntero_token = nuevo_puntero
					parseo_correcto = True
				else:
					subarbol,nuevo_puntero = self.parsear_cletear(puntero_token)
					if(self.validar_parseo(subarbol)):
						puntero_token = nuevo_puntero
						parseo_correcto = True
					else:
						subarbol,nuevo_puntero = self.parsear_play(puntero_token)
						if(self.validar_parseo(subarbol)):
							puntero_token = nuevo_puntero
							parseo_correcto = True
						else:
							subarbol,nuevo_puntero = self.parsear_gol(puntero_token)
							if(self.validar_parseo(subarbol)):
								puntero_token = nuevo_puntero
								parseo_correcto = True
							else:
								subarbol,nuevo_puntero = self.parsear_acorde(puntero_token)
								if(self.validar_parseo(subarbol)):
									puntero_token = nuevo_puntero
									parseo_correcto = True
								else:
									subarbol,nuevo_puntero = self.parsear_quemar(puntero_token)
									if(self.validar_parseo(subarbol)):
										puntero_token = nuevo_puntero
										parseo_correcto = True
						
				

		if(parseo_correcto):
			return subarbol,puntero_token
		else:
			self.calcular_error(puntero_token)
			return [],-1


	def parsear_declaracion(self,puntero_token):
		subarbol = Nodo_Declaracion("DECLARACION","DECLARACION",[])
		nuevo_puntero = puntero_token


		if(self.comparar("TIPO",puntero_token)):
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			arbol_aux,nuevo_puntero = self.parsear_asignacion(puntero_token)
			if(self.validar_parseo(arbol_aux)):
				puntero_token = nuevo_puntero
				subarbol.agregar_nodo(arbol_aux)
				return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1

	def parsear_asignacion(self,puntero_token):
		subarbol = Nodo_Asignacion("ASIGNACION","ASIGNACION",[])
		nuevo_puntero = puntero_token
		if(self.comparar("NOMBRE",puntero_token)):
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			if(self.comparar("CAMBIO",puntero_token)):
				puntero_token+=1
				arbol_aux,nuevo_puntero = self.parsear_operacion_matematica(puntero_token)
				if(self.validar_parseo(arbol_aux)):
					puntero_token = nuevo_puntero
					subarbol.agregar_nodo(arbol_aux)
					if(self.comparar("FIN",puntero_token)):
						puntero_token += 1
						
						return subarbol,puntero_token
				else:
					arbol_aux,nuevo_puntero = self.parsear_valor(puntero_token)
					if(self.validar_parseo(arbol_aux)):
						puntero_token = nuevo_puntero
						subarbol.agregar_nodo(arbol_aux)
						if(self.comparar("FIN",puntero_token)):
							puntero_token += 1
							return subarbol,puntero_token
					else:
						arbol_aux,nuevo_puntero = self.parsear_gol(puntero_token)
						if(self.validar_parseo(arbol_aux)):
							puntero_token = nuevo_puntero
							subarbol.agregar_nodo(arbol_aux)
							return subarbol,puntero_token
						else:
							arbol_aux,nuevo_puntero = self.parsear_acorde(puntero_token)
							if(self.validar_parseo(arbol_aux)):
								puntero_token = nuevo_puntero
								subarbol.agregar_nodo(arbol_aux)
								return subarbol,puntero_token
							
						

		self.calcular_error(puntero_token)
		return [],-1

	def parsear_valor(self,puntero_token):
		subarbol = Nodo_Valor("VALOR","VALOR",[])
		nuevo_puntero = puntero_token

		if(self.comparar("INT",puntero_token)):
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			return subarbol,puntero_token
		if(self.comparar("BOOL",puntero_token)):
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			return subarbol,puntero_token
		if(self.comparar("STRING",puntero_token)):
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1
		
	
	def parsear_operacion_matematica(self,puntero_token):
		
		subarbol = Nodo_Operacion_Matematica("OPERACION_MATEMATICA","OPERACION_MATEMATICA",[])

		if(self.comparar("INT",puntero_token) or self.comparar("NOMBRE",puntero_token)):
			
			subarbol.agregar_nodo(self.crear_nodo(puntero_token))
			puntero_token+=1
			while(self.comparar("OPERADOR",puntero_token)):
				
				subarbol.agregar_nodo(self.crear_nodo(puntero_token))
				puntero_token+=1
				if(self.comparar("INT",puntero_token) or self.comparar("NOMBRE",puntero_token)):
					subarbol.agregar_nodo(self.crear_nodo(puntero_token))
					puntero_token+=1
				else:
					calcular_error(puntero_token)
					return [],-1
			return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1

	def parsear_operacion_logica(self,puntero_token):
		subarbol = Nodo_Operacion_Logica("OPERACION_LOGICA","OPERACION_LOGICA",[])
		subarbol_aux,nuevo_puntero = self.parsear_operacion_matematica(puntero_token)
		subarbol_aux2,nuevo_puntero2 = self.parsear_valor(puntero_token)
		if(self.validar_parseo(subarbol_aux) or self.comparar("NOMBRE",puntero_token) or self.validar_parseo(subarbol_aux2)):
			if(self.comparar("NOMBRE",puntero_token)):
				subarbol.agregar_nodo(self.crear_nodo(puntero_token))
				puntero_token += 1
			elif(self.validar_parseo(subarbol_aux2)):
				subarbol.agregar_nodo(subarbol_aux2)
				puntero_token = nuevo_puntero2
			elif(self.validar_parseo(subarbol_aux)):
				subarbol.agregar_nodo(subarbol_aux)
				puntero_token = nuevo_puntero

			if(self.comparar("OPERADOR_LOGICO",puntero_token)):
				subarbol.agregar_nodo(self.crear_nodo(puntero_token))
				puntero_token += 1
				subarbol_aux,nuevo_puntero = self.parsear_operacion_matematica(puntero_token)
				subarbol_aux2,nuevo_puntero2 = self.parsear_valor(puntero_token)
				if(self.validar_parseo(subarbol_aux) or self.comparar("NOMBRE",puntero_token) or self.validar_parseo(subarbol_aux2)):
					if(self.validar_parseo(subarbol_aux)):
						subarbol.agregar_nodo(subarbol_aux)
						puntero_token = nuevo_puntero
					elif(self.validar_parseo(subarbol_aux2)):
						subarbol.agregar_nodo(subarbol_aux2)
						puntero_token = nuevo_puntero2
					else:
						subarbol.agregar_nodo(self.crear_nodo(puntero_token))
						puntero_token += 1
					return subarbol,puntero_token
			
		self.calcular_error(puntero_token)
		return [],-1
						
	
	def parsear_if(self,puntero_token):
		
		if(self.comparar("IF",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token += 1

				subarbol_aux,nuevo_puntero = self.parsear_operacion_logica(puntero_token)
				if(self.validar_parseo(subarbol_aux)):
					subarbol.agregar_nodo(subarbol_aux)
					puntero_token = nuevo_puntero
					if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
						puntero_token += 1
						if(self.comparar("LLAVE_IZQUIERDA",puntero_token)):
								puntero_token += 1

								subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
								if(self.validar_parseo(subarbol_aux)):
									subarbol.agregar_nodo(subarbol_aux)
									puntero_token = nuevo_puntero

									while(True):
										subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
										if(self.validar_parseo(subarbol_aux)):
											subarbol.agregar_nodo(subarbol_aux)
											puntero_token = nuevo_puntero
										else:
											break
									if(self.comparar("LLAVE_DERECHA",puntero_token)):
										puntero_token += 1
										subarbol_aux,nuevo_puntero = self.parsear_else(puntero_token)
										if(self.validar_parseo(subarbol_aux)):
											subarbol.agregar_nodo(subarbol_aux)
											puntero_token = nuevo_puntero

										return subarbol,puntero_token
		self.calcular_error(puntero_token)								
		return [],-1	

	def parsear_else(self,puntero_token):

		if(self.comparar("ELSE",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("LLAVE_IZQUIERDA",puntero_token)):
				puntero_token += 1
				subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
				if(self.validar_parseo(subarbol_aux)):
					subarbol.agregar_nodo(subarbol_aux)
					puntero_token = nuevo_puntero
					while(True):
						subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
						if(self.validar_parseo(subarbol_aux)):
							subarbol.agregar_nodo(subarbol_aux)
							puntero_token = nuevo_puntero
						else:
							break
					if(self.comparar("LLAVE_DERECHA",puntero_token)):
						puntero_token += 1
						return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1
	
	
	def parsear_quemar(self,puntero_token):

		if(self.comparar("STRCPY",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token += 1
						
				if(self.comparar("NOMBRE",puntero_token)):
					subarbol.agregar_nodo(self.crear_nodo(puntero_token))
					puntero_token += 1
					if(self.comparar("COMA",puntero_token)):
						puntero_token += 1
						if(self.comparar("STRING",puntero_token) or self.comparar("NOMBRE",puntero_token)):
							subarbol.agregar_nodo(self.crear_nodo(puntero_token))
							puntero_token += 1
							if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
								puntero_token += 1
								if(self.comparar("FIN",puntero_token)):
									puntero_token += 1
									return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1
										
	def parsear_acorde(self,puntero_token):
		
		if(self.comparar("STRLEN",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token += 1
				if(self.comparar("STRING",puntero_token) or self.comparar("NOMBRE",puntero_token)):
					subarbol.agregar_nodo(self.crear_nodo(puntero_token))
					puntero_token += 1
					if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
						puntero_token += 1
						if(self.comparar("FIN",puntero_token)):
							puntero_token += 1
							return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1

	def parsear_gol(self,puntero_token):

		if(self.comparar("INPUT",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token += 1
				if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
					puntero_token += 1
					if(self.comparar("FIN",puntero_token)):
						puntero_token += 1
						return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1

	def parsear_play(self,puntero_token):

		if(self.comparar("PRINT",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token += 1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token += 1
				subarbol_aux,nuevo_puntero = self.parsear_valor(puntero_token)
				if(self.validar_parseo(subarbol_aux) or self.comparar("NOMBRE",puntero_token)):
					if(self.validar_parseo(subarbol_aux)):
						subarbol.agregar_nodo(subarbol_aux)
						puntero_token = nuevo_puntero
					else:
						subarbol.agregar_nodo(self.crear_nodo(puntero_token))
						puntero_token += 1

					if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
						puntero_token += 1
						if(self.comparar("FIN",puntero_token)):
							puntero_token += 1
							return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return [],-1

	
	def parsear_cletear(self,puntero_token):
		
		if(self.comparar("WHILE",puntero_token)):
			subarbol = self.crear_nodo(puntero_token)
			puntero_token+=1
			if(self.comparar("PARENTESIS_IZQUIERDO",puntero_token)):
				puntero_token+=1

				subarbol_aux,nuevo_puntero = self.parsear_operacion_logica(puntero_token)
				
				if(self.validar_parseo(subarbol_aux)):
					subarbol.agregar_nodo(subarbol_aux)
					puntero_token = nuevo_puntero
					if(self.comparar("PARENTESIS_DERECHO",puntero_token)):
						puntero_token+=1
						if(self.comparar("LLAVE_IZQUIERDA",puntero_token)):
							puntero_token+=1

							subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
							if(self.validar_parseo(subarbol_aux)):
								subarbol.agregar_nodo(subarbol_aux)
								puntero_token = nuevo_puntero

								while(True):
									subarbol_aux,nuevo_puntero = self.parsear_accion(puntero_token)
									if(self.validar_parseo(subarbol_aux)):
										subarbol.agregar_nodo(subarbol_aux)
										puntero_token = nuevo_puntero
									else:
										break

								if(self.comparar("LLAVE_DERECHA",puntero_token)):
									puntero_token += 1

									return subarbol,puntero_token
		self.calcular_error(puntero_token)
		return  [],-1


	def imprimir_AST(self):
		print(self.AST.hijos[0].hijos[0].tipo)
		
		lista = [self.AST]
		arbol_string = ""
		
		while(lista != []):

			arbol_string += lista[0].tipo + "\n---> "
			
			for hijo in lista[0].hijos:
				
				arbol_string += hijo.tipo+" "
				lista += [hijo]

			arbol_string += "\n\n";
			lista = lista[1:]

		print("Arbol AST:\n")
		print(arbol_string)
		


	

