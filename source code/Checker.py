from parser import *
from Nodo import *


'''
Esta clase por medio del patron de dise;o visitor, se hara el checkeo de tipos
tiene 3 atributos
tablas: es la tabla de valores la cual sera representada por una 
lista de diccionarios, cada diccionario sera un scope del programa, 
estos diccionarios tendran como llave el nombre de la variable, y los valores seran pares
donde el primer elemento es el tipo de la variable y el segundo elemento es el valor actual
de dicha variable, cada vez que empiece una funcion (if,else,while) se creara un diccionario para
ese scope y se metera a la lista, y cuando termine la funcion ese diccionario sera eliminado
de la lista

largoTablas: la cantidad de diccionarios en la lista
AST: el arbol


'''
class Checker:

	tablas = [dict()]
	largoTablas = 1
	AST = []


	def __init__(self,AST):
		self.AST = AST
	'''
	inicia con el checkeo llamando al metodo visitar del nodo padre (nodo programa)
	'''
	def checkear(self):
		return self.AST.visitar(self)

	'''
	esta funcion recibe el nombre de una variable, y la busca en la lista de tablas de valores
	si encuentra el nombre entonces devuelve una tupla, donde el primer elemento es el indice
	de la tabla donde se encontro la variable, y el segundo elemento es la informacion
	de dicha variable
	'''
	def revisarTabla(self,nombre):
		busqueda = 0
		n = 0
		for tabla in self.tablas:
			busqueda = tabla.get(nombre)
			if(type(busqueda) == list):
				return n,tabla[nombre]
			n+=1
		return -1,busqueda


	'''
	el visitor de programa consiste en recorrer todos sus hijos y llamar a los visitors de
	cada hijo, los visitos devuelven listas de 2 elementos indicando el resultado del visitor
	si hubo un error en algun momento devovlera un string con el mensaje de error correspondiente

	'''
	def visitarPrograma(self,nodo):
		#for con los hijos haciendo su visit
		estado = ""
		for hijo in nodo.hijos:
			estado = hijo.visitar(self)
			if(type(estado) == str):
				break
		return estado
	'''
	la declaracion consiste en tomar el nombre de la variable, buscarla en las tablas de
	valores, y sino esta entonces agrega esa variable a la tabla y como informacion pone 
	el tipo de la variable y se pone el valor por defecto de dicho tipo
	siempre una declaracion va antes de una asignacion, asi que luego de meter dicha
	variable a la tabla, se llama el visitor de asignacion
	'''
	def visitarDeclaracion(self,nodo):
		
		#insertar el nombre con el tipo y valor del tipo de la declaracion
		tipo = nodo.hijos[0].visitar(self)
		nombre = nodo.hijos[1].hijos[0].valor
		tabla,busqueda = self.revisarTabla(nombre)
		if(tabla == -1):#no esta en la tabla
			self.tablas[0][nombre] = tipo
			return nodo.hijos[1].visitar(self)

		else:
			return "error la variable "+nombre+" ya ha sido declarada antes"
	


	def visitarTipo(self,nodo):
		if(nodo.valor == "portero"):
			return ["BOOL","true"]
		elif(nodo.valor == "defensa"):
			return ["INT",0]
		else:
			return ["STRING",""]
	'''
	Busca el nombre de la variable en la tabla si esta entonces verifica que el valor
	que le voy a meter sea del tipo de la variable y si todo esto coincide, entonces
	actualiza el valor de la variable en la tabla de valores
	'''
	def visitarAsignacion(self,nodo):

		#buscar que exista el nombre
		nombre = nodo.hijos[0].valor
		tabla,busqueda = self.revisarTabla(nombre)
		if(tabla != -1):
			#si esta verificar que el valor sea del tipo de la variable
			#si es del tipo de la variable modificar la tabla
			info = nodo.hijos[1].visitar(self)
			
			if(info[0] == "INPUT"): #se asigna con un input


				if(self.tablas[tabla][nombre][0] == "INT"):
					try:
						self.tablas[tabla][nombre] = ["INT",int(info[1])]
					except:
						return "el valor ingresado no es de tipo int como la variable "+nombre
				elif(self.tablas[tabla][nombre][0] == "BOOL"):
					if(info[1] == "true" or info[1] == "false"):
						self.tablas[tabla][nombre] = bool(info[1])
					else:
						return "el valor ingresado no es de tipo bool como la variable "+nombre
				
				return self.tablas[tabla][nombre]


			if(busqueda[0] == info[0]):#el tipo coincide con el tipo del valor ingresado
				self.tablas[tabla][nombre] = info
				return info
			if(type(info) == str):#hubo un error
				return info
			else:
				return "El valor "+str(info[0])+" no es del tipo de la variable "+nombre+"\ndebe ser de tipo "+busqueda[0]
		else:
			return "Error la variable "+nombre+" no ha sido declarada"
		
	'''
	verifica que los 2 elementos que se estan comparando sean del mismo tipo, y si coincide
	procede a hacer la comparacion devolviendo siempre un par donde el primer elemento
	indica que estamos devolviendo un valor de tipo BOOL y el segundo elemento sseria el valor
	de la comparacion que podria ser true o false 
	'''
	def visitarExpresionLogica(self,nodo):

		num1 = nodo.hijos[0].visitar(self)
		operador = nodo.hijos[1].visitar(self)
		num2 = nodo.hijos[2].visitar(self)
		if(num1[0] == 'INT'):
			if(num2[0] == 'INT'):

				if(operador[1] == "=="):
					return ["BOOL",str(int(num1[1]) == int(num2[1])).lower()]
				elif(operador[1] == "!="):
					return ["BOOL",str(int(num1[1]) != int(num2[1])).lower()]
				elif(operador[1] == ">"):
					return ["BOOL",str(int(num1[1]) > int(num2[1])).lower()]
				elif(operador[1] == "<"):
					return ["BOOL",str(int(num1[1]) < int(num2[1])).lower()]
				elif(operador[1] == ">="):
					return ["BOOL",str(int(num1[1]) >= int(num2[1])).lower()]
				elif(operador[1] == "<="):
					return ["BOOL",str(int(num1[1]) <= int(num2[1])).lower()]
		if(num1[0] == num2[0]):
			if(operador[1] == "=="):
				return ["BOOL",str(num1[1] == num2[1]).lower()]
			elif(operador[1] == "!="):
				return ["BOOL",str(num1[1] != num2[1]).lower()]	
		return "Los tipos de la expresion logica son de diferente tipo o hay un problema en la comparacion"+num1[0]+" - "+num2[0]

	'''
	
	'''
	def visitarIf(self,nodo):

		self.tablas = [dict()] + self.tablas #ingreso la nueva tabla
		self.largoTablas+=1

		indice = 1
		largo = len(nodo.hijos) #largo de hijos del if a los que voy a llamarle el visitor
		ultimo = nodo.hijos[largo-1]
		if(ultimo.tipo == "ELSE"):
			largo-=1
		condicion = nodo.hijos[0]

		if(condicion.visitar(self)[1] == "true"): #si es true recorro los hijos del if 
			for nd in nodo.hijos[1:]:             #para llamarle el visitor a cada uno
				if(indice == largo):
					self.tablas = self.tablas[1:]
					self.largoTablas -= 1
					return ["IF","CORRECTO"]

				estado = nd.visitar(self)
				if(type(estado) == str):
					return estado
				indice+=1


		if(ultimo.tipo == "ELSE"):#si la condicion del if no se cumple y hubiera un else
								  #se recorre los hijos del else para llamar los visitors a cada uno
			self.tablas = self.tablas[1:]
			self.largoTablas -= 1
			return ultimo.visitar(self)


	def visitarElse(self,nodo):
		self.tablas = [dict()] + self.tablas
		self.largoTablas += 1
		for nd in nodo.hijos:
			estado = nd.visitar(self)
			if(type(estado) == str):
				return estado
		self.tablas = self.tablas[1:]
		self.largoTablas -= 1
		return ["ELSE","CORRECTO"]
	'''
	Mientras la condicion se siga cumpliendo se volvera a llamar a visitarWhile para
	hacerle el visitor a sus elementos, en el momento que la condicion no se cumpla 
	la funcion termina
	'''
	def visitarWhile(self,nodo):
		
		self.tablas = [dict()] + self.tablas
		self.largoTablas += 1

		condicion = nodo.hijos[0].visitar(self)

		if(condicion[1] == "true"):
			for nd in nodo.hijos[1:]:
				estado = nd.visitar(self)
				if(type(estado) == str):
					return estado
			self.tablas = self.tablas[1:]
			self.largoTablas -= 1
			self.visitarWhile(nodo)
		return ["WHILE","CORRECTO"]

	'''
	un valor puede ser un int, bool o un string, estos valores siempre estaran en el hijo
	del nodo valor entonces se llama el visitor del hijo y este devolera un par, donde
	el primer elemento es el tipo del valor y el segundo elemento es el valor real
	'''
	def visitarValor(self,nodo):
		
		return nodo.hijos[0].visitar(self) 

	def visitarInt(self,nodo):

		return [nodo.tipo,nodo.valor]
	
	def visitarBool(self,nodo):

		return [nodo.tipo,nodo.valor]

	def visitarOperadorLogico(self,nodo):
		
		return [nodo.tipo,nodo.valor]
	
	def visitarString(self,nodo):

		return [nodo.tipo,nodo.valor]

	'''
	hace un input y se devuelve un par donde el primer elemento indica que es un visitor
	de tipo input, y el segundo elemento es el valor que se acaba de ingresar
	'''
	def visitarInput(self,nodo):
		x = input()
		return ["INPUT",x]


	'''
	el hijo del print va a ser lo que se quiere imprimir, el cual debe ser una variable o 
	un string, si no hay errores lo imprime
	'''
	def visitarPrint(self,nodo):
		estado = nodo.hijos[0].visitar(self)
		if(type(estado) != str):#no hubo error
			print(estado[1])	
			return ["PRINT","CORRECTO"]
		return estado
	'''
	el hijo del strlen sera el string al cual le queremos sacar el largo, se verifica 
	que el hijo sea un strig y si lo es devuelve el largo
	'''
	def visitarStrlen(self,nodo):

		estado = nodo.hijos[0].visitar(self)
		if(type(estado) == str):
			return estado
		else:
			if(estado[0] == "STRING"):
				return ["INT",len(estado[1])-2]
			else:
				return "el paramentro de acorde debe ser de tipo STRING"

	'''
	el primer hijo del strcpy sera la variable a la cual le queremos meter el valor del segundo hijo
	el cual obviamente debe ser un string tambien, se verifica que el primer parametro sea
	una variable string y que la variable exista y se verifica que el segundo parametro 
	sea un string si todo esto va bien, entonces se procede a copiar el segundo string
	en el primero 
	'''
	def visitarStrcpy(self,nodo):

		estado = nodo.hijos[0].visitar(self)
		estado2 = nodo.hijos[1].visitar(self)
		

		if(estado[0] == "STRING" and estado2[0] == "STRING"):
			nombre = nodo.hijos[0].valor
			tabla,busqueda = self.revisarTabla(nombre)
			self.tablas[tabla][nombre] = ["STRING",estado2[1]]
		else:
			return "el primer parametro de quemar() debe ser una variable string y el segundo debe ser una variable string o un string"
			

	def visitarNombre(self,nodo_nombre):
		#buscar en la tabla el nombre
		#si lo encuentra devolver [tipo,valor]
		#sino error de no declaracion
		
		tabla, simbolo = self.revisarTabla(nodo_nombre.valor)
		if(tabla != -1):
			return [simbolo[0],simbolo[1]]
		return "No se ha declarado la variable "+nodo_nombre.valor

	def aplicarOperacion(self,largoOperando,largoOperador,pilaOperando,pilaOperador):
		if(pilaOperador[0] == "+"):
			pilaOperando = [(pilaOperando[1] + pilaOperando[0])] + pilaOperando[2:]
		elif(pilaOperador[0] == "-"):
			pilaOperando = [(pilaOperando[1] - pilaOperando[0])] + pilaOperando[2:]
		elif(pilaOperador[0] == "*"):
			pilaOperando = [(pilaOperando[1] * pilaOperando[0])] + pilaOperando[2:]
		elif(pilaOperador[0] == "-"):
			pilaOperando = [(pilaOperando[1] - pilaOperando[0])] + pilaOperando[2:]
		pilaOperador = pilaOperador[1:]
		largoOperador-=1
		largoOperando-=1
		return largoOperando,largoOperador,pilaOperando,pilaOperador


	'''
	los hijos seran la expresion matematica, entonces se agarran esos hijos y se convierte
	la expresion matematica en una expresion matematica posfija, para poder hacer el algoritmo
	de resolver operaciones matematicas con una pila para una expresion posfija
	'''
	def visitarOpMatematica(self,nodo):
		#resolver la operacion matematica y devolver
		#convertir a string
		infix = ""
		prioridad = {"+":0,"-":0,"*":1,"/":1}
		largoOperando = 0
		largoOperador = 0
		pilaOperando = []
		pilaOperador = []

		for hijo in nodo.hijos:	
			if(hijo.tipo == "OPERADOR"):
				
				if(largoOperador > 0):
					while(largoOperador > 0 and (prioridad[pilaOperador[0]] >= prioridad[hijo.valor])):
						largoOperando,largoOperador,pilaOperando,pilaOperador = self.aplicarOperacion(largoOperando,largoOperador,pilaOperando,pilaOperador)
						
				pilaOperador = [hijo.valor] + pilaOperador
				largoOperador+=1				
			else:
				info = hijo.visitar(self)
				if(type(info) == str):#ocurrio un error
					return info
				pilaOperando = [int(info[1])] + pilaOperando
				largoOperando+=1
				

		while(largoOperador > 0):
			largoOperando,largoOperador,pilaOperando,pilaOperador = self.aplicarOperacion(largoOperando,largoOperador,pilaOperando,pilaOperador)
		
		return ["INT",pilaOperando[0]]


