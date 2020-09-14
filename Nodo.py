
'''
Este archivo tiene todas las clases Nodos que tendra el arbol AST, cada nodo tiene 
los siguientes atributos

tipo = tipo del nodo
valor = valor de dicho nodo
hijos = los hijos del nodo

tambien cada nodo cuenta con el metodo de visitar, el cual recibe como parametro el checker
para poder realizar el metodo visit correspondiente al tipo de nodo

'''

class Nodo:
	tipo = 0
	valor = 0
	hijos = []

	def __init__(self,tipo,valor,hijos):
		self.tipo = tipo
		self.valor = valor
		self.hijos = hijos

	def agregar_nodo(self,nuevo_nodo):
		self.hijos += [nuevo_nodo]


class Nodo_Valor(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarValor(self)
class Nodo_Programa(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarPrograma(self)
	




class Nodo_Declaracion(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarDeclaracion(self)

class Nodo_Tipo(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarTipo(self)

class Nodo_Nombre(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarNombre(self)



class Nodo_Asignacion(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarAsignacion(self)

class Nodo_Int(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarInt(self)


class Nodo_Bool(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)

	def visitar(self,checker):
		return checker.visitarBool(self)

class Nodo_String(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarString(self)



class Nodo_Operacion_Matematica(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)

	def visitar(self,checker):
		return checker.visitarOpMatematica(self)



class Nodo_Operador(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
class Nodo_Operador_Logico(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarOperadorLogico(self)
class Nodo_Operacion_Logica(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarExpresionLogica(self)


class Nodo_If(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarIf(self)

class Nodo_Else(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarElse(self)

class Nodo_While(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarWhile(self)
class Nodo_Print(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarPrint(self)

class Nodo_Input(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarInput(self)

class Nodo_Strlen(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarStrlen(self)

class Nodo_Strcpy(Nodo):
	def init(self,tipo,valor,hijos):
		Nodo.__init__(self,tipo,valor,hijos)
	def visitar(self,checker):
		return checker.visitarStrcpy(self)
	
