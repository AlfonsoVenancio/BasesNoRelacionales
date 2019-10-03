
#! coding: latin-1

#Uso de while.
# Serie de Fibonacci.
a, b = 0, 1     #Se puede hacer este tipo de asignación.
while b < 10:
	print("a= ", a, "b= ", b)
	a, b = b, a + b
print()


#Uso de for.
a = ['gato', 'ventana', 'casa']
for x in a:
	print(x, len(x))


