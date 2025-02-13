class Drink:  
    def __init__(self):  
        self._price = 0  # Usamos un atributo protegido  

    def set_price(self, price):  
        self._price = price  # Método para establecer el precio  


class Coffee(Drink):  
    def make(self):  
        print(f"Coffee: {self._price}")  # Método para mostrar el precio del café  


class Tea(Drink):  
    def make(self):  
        print(f"Tea: {self._price}")  # Método para mostrar el precio del té  


def main():  
    c = Coffee()  # Crear objeto Coffee  
    t = Tea()     # Crear objeto Tea  

##    e1 = c  # Referencia a Coffee  
##    e2 = t  # Referencia a Tea  

    c.set_price(5)  # Establecer el precio del café  
    t.set_price(6)  # Establecer el precio del té  

    c.make()  # Llamar al método make para Coffee  
    t.make()  # Llamar al método make para Tea  


if __name__ == "__main__":  
    main()  # Ejecutar función principal
