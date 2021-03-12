import types
import collections

class Tablero:
    def __init__(self):
        self.lineasHorizontales = [[],[],[],[],[]]
        self.lineasVerticales = [[],[],[],[]]
        self.grid = [['+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+'],
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                    ['+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+'],
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                    ['+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+'],
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                    ['+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+'],
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                    ['+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+',' ',' ',' ','+']]

    def actualizaTablero(self, x1, y1, x2, y2, jugador):
        self.grid[x1+x2+1][(y1+y2)*2]=str(jugador)  
                
    def imprimirTablero(self):
        for i in range(9):
            for j in range(17):
                print(self.grid[i][j], end = '')
            print()

    def iniciaJuego(self):
        self.agregarLineas()
        self.imprimirTablero()

    def agregarLineas(self):
        for i in range(5):
            for j in range(4):
                self.lineasHorizontales[i].append(Linea(i, j, i, (j+1))) #Agrega las líneas horizontales [(0,0),(0,1)]
        
        for i in range(4):
            for j in range(5):
                self.lineasVerticales[i].append(Linea(i, j, (i+1), j))   #Agrega las líneas verticales [(0,0),(1,0)]
    

    #Esta función se encarga de verificar si todos los puntos ya se unieron, pues si es así el juego ya habrá acabado
    def finDelJuego(self):
        for i in range(5):
            for j in range(4):
                if(self.lineasHorizontales[i][j].ocupada == False):
                    return False
        for i in range(4):
            for j in range(5):
                if(self.lineasVerticales[i][j].ocupada == False):
                    return False
        return True
    #Esta función nos permite hacer una tirada, dibujar una línea entre dos puntos
    #def realizaTiro(self):

    def cuadradoCompleto(self, arriba, abajo, izquierda, derecha):
        #Recorriendo horizontales
        for i in range(5):
            for j in range(4):
                if((collections.Counter(self.lineasHorizontales[i][j].get_coordenadas()) == collections.Counter(arriba)) or (collections.Counter(self.lineasHorizontales[i][j].get_coordenadas()) == collections.Counter(abajo))):
                    if(self.lineasHorizontales[i][j].ocupada == False):
                        return False
        #Recorriendo verticales
        for i in range(4):
            for j in range(5):
                if((collections.Counter(self.lineasVerticales[i][j].get_coordenadas()) == collections.Counter(izquierda)) or (collections.Counter(self.lineasVerticales[i][j].get_coordenadas()) == collections.Counter(derecha))):
                    if(self.lineasVerticales[i][j].ocupada == False):      
                        return False
        return True

    def juega(self, jugador):
        if(jugador.ficha == 'H'): #Turno del humano
            return (self.realizaMovimiento(jugador))
        else:
            return self.realizaMovimientoIA(jugador)

    #Esta función busca cuadrados con 3 lados y ahi pone un cuarto, sino lo encuentra regresa False
    def funcionDeCosto1(self, jugador):
        listaLineasVacias = []
        for i in range(4): #Es hasta 4 porque la última fila de líneas horizontales no se recorre
            for j in range(4):
                #Calculamos las coordenadas de las líneas que conforman un cuadrado
                if (self.lineasHorizontales[i][j].ocupada == False):
                    listaLineasVacias.append(self.lineasHorizontales[i][j].get_coordenadas()) #Buscamos la línea de arriba
                if(self.lineasHorizontales[i+1][j].ocupada == False):
                    listaLineasVacias.append(self.lineasHorizontales[i+1][j].get_coordenadas()) #Bucamos la línea de abajo
                if(self.lineasVerticales[i][j].ocupada == False): #Línea izquierda
                    listaLineasVacias.append(self.lineasVerticales[i][j].get_coordenadas())
                if(self.lineasVerticales[i][j+1].ocupada == False):
                    listaLineasVacias.append(self.lineasVerticales[i][j+1].get_coordenadas())
                if(len(listaLineasVacias) == 1):
                    flag = self.pintaLinea(listaLineasVacias[0])
                    if(flag): #Si es que si la pintó
                        punto1, punto2 = listaLineasVacias[0]
                        x1,y1 = punto1
                        x2,y2 = punto2
                        ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                    return True
                else:
                    listaLineasVacias.clear()
        return False
    
    def movimientoValidoH(self, i, j):
        cont = 0
        if(i-1 == -1):
            if(self.lineasHorizontales[i+1][j].ocupada == True):
                cont = cont + 1
            if(self.lineasVerticales[i][j].ocupada == True):
                cont = cont + 1
            if(self.lineasVerticales[i][j+1].ocupada == True):
                cont = cont + 1
            if(cont == 2):
                return False
            else: return True
        if(i+1 >= 4):
            if(self.lineasHorizontales[i-1][j].ocupada == True):
                cont = cont + 1
            if(self.lineasVerticales[i-1][j].ocupada == True):
                cont = cont + 1
            if(self.lineasVerticales[i-1][j+1].ocupada == True):
                cont = cont + 1
            if(cont == 2):
                return False
            else: return True
        if(self.lineasHorizontales[i+1][j].ocupada == True): #Linea horizontal abajo
                cont = cont + 1
        if(self.lineasVerticales[i][j].ocupada == True): #Linea de la izq inferior
            cont = cont + 1
        if(self.lineasVerticales[i][j+1].ocupada == True): #Linea der inferior
            cont = cont + 1
        if(self.lineasHorizontales[i-1][j].ocupada == True): #linea de arriba
                cont = cont + 1
        if(self.lineasVerticales[i-1][j].ocupada == True): #Linea izq superior
            cont = cont + 1
        if(self.lineasVerticales[i-1][j+1].ocupada == True): #Linea der superior
            cont = cont + 1
        if(cont == 4 or cont == 3 or cont == 2):
            return False
        else:
            return True

    def movimientoValidoV(self, i, j):
        cont = 0
        if(j-1 == -1):
            if(self.lineasVerticales[i][j+1].ocupada == True): #Linea de la derecha
                cont = cont + 1
            if(self.lineasHorizontales[i][j].ocupada == True): #Linea de arriba
                cont = cont + 1
            if(self.lineasHorizontales[i+1][j].ocupada == True): #Linea abajo
                cont = cont + 1
            if(cont == 2):
                return False
            else: return True
        if(j+1 >= 4):
            if(self.lineasVerticales[i][j-1].ocupada == True): #Linea de la izquierda
                cont = cont + 1
            if(self.lineasHorizontales[i][j-1].ocupada == True): #Linea de arriba
                cont = cont + 1
            if(self.lineasHorizontales[i+1][j-1].ocupada == True): #Linea abajo
                cont = cont + 1
            if(cont == 2):
                return False
            else: return True
        if(self.lineasVerticales[i][j+1].ocupada == True): #Linea de la derecha
                cont = cont + 1
        if(self.lineasHorizontales[i][j].ocupada == True): #Linea de arriba
            cont = cont + 1
        if(self.lineasHorizontales[i+1][j].ocupada == True): #Linea abajo
            cont = cont + 1
        if(self.lineasVerticales[i][j-1].ocupada == True): #Linea de la izquierda
            cont = cont + 1
        if(self.lineasHorizontales[i][j-1].ocupada == True): #Linea de arriba
            cont = cont + 1
        if(self.lineasHorizontales[i+1][j-1].ocupada == True): #Linea abajo
            cont = cont + 1
        if(cont == 4):
            return False
        else:
            return True
    #Esta función busca crear o extender cadenas de las que después se pueda aprovechar            
    def funcionDeCosto2(self, jugador):
        for i in range(5):
            for j in range(4):
                if (self.lineasHorizontales[i][j].ocupada == True):
                    if(j+1 >= 4):
                        if(self.lineasHorizontales[i][j-1].ocupada == False):
                            if(self.movimientoValidoH(i, j-1)): 
                                flag = self.pintaLinea(self.lineasHorizontales[i][j-1].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j-1].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                    else:
                        if(self.lineasHorizontales[i][j+1].ocupada == False):
                            if(self.movimientoValidoH(i, j+1)):
                                flag = self.pintaLinea(self.lineasHorizontales[i][j+1].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j+1].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                else:
                    if(self.movimientoValidoH(i, j)):
                                flag = self.pintaLinea(self.lineasHorizontales[i][j].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                    else:
                        if(self.movimientoValidoH(i, j+1)):
                                        flag = self.pintaLinea(self.lineasHorizontales[i][j+1].get_coordenadas())
                                        if(flag):
                                            x1,y1,x2,y2=self.lineasHorizontales[i][j+1].get_AllCoor()
                                            ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                            if(ban):
                                                return ban,2 #Regresa que si se completó un cuadrado
                                            else:
                                                return True,1
        for i in range(4):
            for j in range(5):
                if (self.lineasVerticales[i][j].ocupada == True):
                    if(i+1 >= 4):
                        if(self.lineasVerticales[i-1][j].ocupada == False):
                            if(self.movimientoValidoH(i-1, j)): 
                                flag = self.pintaLinea(self.lineasHorizontales[i][j-1].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j-1].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                    else:
                        if(self.lineasHorizontales[i][j+1].ocupada == False):
                            if(self.movimientoValidoH(i, j+1)):
                                flag = self.pintaLinea(self.lineasHorizontales[i][j+1].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j+1].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                else:
                    if(self.movimientoValidoH(i, j)):
                                flag = self.pintaLinea(self.lineasHorizontales[i][j].get_coordenadas())
                                if(flag):
                                    x1,y1,x2,y2=self.lineasHorizontales[i][j].get_AllCoor()
                                    ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                    if(ban):
                                        return ban,2 #Regresa que si se completó un cuadrado
                                    else:
                                        return True,1
                    else:
                        if(self.movimientoValidoH(i, j+1)):
                                        flag = self.pintaLinea(self.lineasHorizontales[i][j+1].get_coordenadas())
                                        if(flag):
                                            x1,y1,x2,y2=self.lineasHorizontales[i][j+1].get_AllCoor()
                                            ban = self.checaSiSeCompletaCuadrado(x1,y1,x2,y2,jugador)
                                            if(ban):
                                                return ban,2 #Regresa que si se completó un cuadrado
                                            else:
                                                return True,1

        return False, 0

    def realizaMovimientoIA(self, jugador):
        #Busca cuadrados con tres lados
        if(not self.funcionDeCosto1(jugador)):
            flag, opc = self.funcionDeCosto2(jugador)
            if(flag == True and opc == 2):
                self.imprimirTablero()
                return True
            else:
                self.imprimirTablero()
                return False
        else:
            self.imprimirTablero()
            return True

    #Esta función se llama cuando queremos realizar un tiro Humano
    def realizaMovimiento(self, jugador):
        flag = True
        ban = False
        lineaOcupada = False
        while(not lineaOcupada):
            while(flag):
                x1, y1 = input("Ingrese las coordenadas del primer punto x y :").split()
                if((int(x1) >= 5 or int(x1) < 0) or (int(y1) >= 5 or int(y1) < 0)):
                    print("Coordenadas no permitidas, intente de nuevo")
                else:
                    flag = False
            flag = True
            while(flag):
                x2, y2 = input("Ingrese las coordenadas del segundo punto x y :").split()
                if((int(x2) >= 5 or int(x2) < 0) or (int(y2) >= 5 or int(y2) < 0) or (int(x1) == int(x2) and int(y1) == int(y2))):
                    print("Coordenadas no permitidas, intente de nuevo")
                else:
                    flag = False
            linea = [(int(x1),int(y1)),(int(x2),int(y2))]
            lineaOcupada = self.pintaLinea(linea)
            if(lineaOcupada == False):
                print("LOS PUNTOS INTRODUCIDOS YA HAN SIDO CONECTADOS | ESCOJA OTRO PAR DE PUNTOS")
                flag = True
            else:
                ban = self.checaSiSeCompletaCuadrado(int(x1),int(y1),int(x2),int(y2), jugador)
        self.imprimirTablero()
        return ban

    def checaSiSeCompletaCuadrado(self, x1, y1, x2, y2, jugador):
        ban, puntos, direccion, linea1, linea2 = self.compruebaCuadradoCompleto(x1,y1,x2,y2)
        if(ban):
            linea = [(0,0),(0,0)]
            if collections.Counter(linea2) == collections.Counter(linea):
                punto1, punto2 = linea1
                x1,y1 = punto1
                x2,y2 = punto2
                self.actualizaTablero(x1, y1, x2, y2,jugador.ficha)
            else:
                punto1, punto2 = linea1
                x1,y1 = punto1
                x2,y2 = punto2
                self.actualizaTablero(x1, y1, x2, y2,jugador.ficha)
                punto1, punto2 = linea2
                x1,y1 = punto1
                x2,y2 = punto2
                self.actualizaTablero(x1, y1, x2, y2,jugador.ficha)
            jugador.actualizaPuntaje(puntos)
        return ban

    def pintaLinea(self, linea):
        punto1 = linea[0]
        punto2 = linea[1]
        x1, y1 = punto1
        x2, y2 = punto2
        if x1 == x2: #Linea horizontal
             #Recorriendo horizontales
            for i in range(5):
                for j in range(4):
                    if(collections.Counter(self.lineasHorizontales[i][j].get_coordenadas()) == collections.Counter(linea) ):
                        if(self.lineasHorizontales[i][j].ocupada == False):
                            self.lineasHorizontales[i][j].activaLinea()
                            self.grid[x1+x2][(y1*4)+1] = '-'
                            self.grid[x1+x2][(y1*4)+2] = '-'
                            self.grid[x1+x2][(y1*4)+3] = '-'
                            return True
        else:
            #Recorriendo verticales
            for i in range(4):
                for j in range(5):
                    if(collections.Counter(self.lineasVerticales[i][j].get_coordenadas()) == collections.Counter(linea)):
                        if(self.lineasVerticales[i][j].ocupada == False):      
                            self.lineasVerticales[i][j].activaLinea()
                            self.grid[x1+x2][y1*4] = '|'
                            return True
        return False

    def compruebaCuadradoCompleto(self, x1, y1, x2, y2):
        #Primer caso
        #Verificar si es horizontal o vertical
        linea = [(0,0),(0,0)]
        if x1 == x2: #La línea es horizontal
            if ((x1-1) == -1): #La línea está en el borde superior del gird
                lineaArriba = [(x1,y1),(x2,y2)]
                lineaIzquierda = [(x1, y1),(x1+1,y1)]
                lineaDerecha = [(x2, y2),(x2+1,y2)]
                lineaAbajo = [(x1+1,y1),(x2+1,y2)]
                return (self.cuadradoCompleto(lineaArriba, lineaAbajo, lineaIzquierda, lineaDerecha),1,'Aba',lineaArriba, linea)
            elif((x1+1) >= 5): #La línea está en el borde inferior del gird
                lineaAbajo = [(x1,y1),(x2,y2)]
                lineaIzquierda = [(x1-1,y1),(x1, y1)]
                lineaDerecha = [(x2-1,y2),(x2, y2)]
                lineaArriba = [(x1-1,y1),(x2-1,y2)]
                return (self.cuadradoCompleto(lineaArriba, lineaAbajo, lineaIzquierda, lineaDerecha),1,'Arr',lineaArriba, linea)
            else: #La línea horizontal no se encuentra en los extremos superior o inferior del grid
                lineaMedio = [(x1,y1),(x2,y2)]

                lineaIzquierda_Arr = [(x1-1,y1),(x1, y1)]
                lineaDerecha_Arr = [(x2-1,y2),(x2, y2)]
                lineaArriba = [(x1-1,y1),(x2-1,y2)]
                
                lineaIzquierda_Aba = [(x1, y1),(x1+1,y1)]
                lineaDerecha_Aba = [(x2, y2),(x2+1,y2)]
                lineaAbajo = [(x1+1,y1),(x2+1,y2)]

                if(self.cuadradoCompleto(lineaArriba, lineaMedio, lineaIzquierda_Arr, lineaDerecha_Arr) == True and self.cuadradoCompleto(lineaMedio, lineaAbajo, lineaIzquierda_Aba, lineaDerecha_Aba) == True):
                    return True, 2, 'MAA',lineaArriba, lineaMedio, #Medio arriba y abajo, se rellenaron los dos cuadritos
                else:
                    if(self.cuadradoCompleto(lineaArriba, lineaMedio, lineaIzquierda_Arr, lineaDerecha_Arr)):
                        return True, 1, 'Arr', lineaArriba, linea
                    elif(self.cuadradoCompleto(lineaMedio, lineaAbajo, lineaIzquierda_Aba, lineaDerecha_Aba)):
                        return True, 1, 'Aba', lineaMedio, linea
        else: #La línea es vertical
            if ((y1-1) == -1): #La línea está en el borde superior del gird
                lineaIzquierda = [(x1,y1),(x2,y2)]
                lineaArriba = [(x1, y1),(x1,y1+1)]
                lineaAbajo = [(x2, y2),(x2,y2+1)]
                lineaDerecha = [(x1,y1+1),(x2,y2+1)]
                return (self.cuadradoCompleto(lineaArriba, lineaAbajo, lineaIzquierda, lineaDerecha),1,'Der',lineaArriba, linea)
            elif((y1+1) >= 5): #La línea está en el borde inferior del gird
                lineaDerecha = [(x1,y1),(x2,y2)]
                lineaArriba = [(x1, y1),(x1,y1-1)]
                lineaAbajo = [(x2, y2),(x2,y2-1)]
                lineaIzquierda = [(x1,y1-1),(x2,y2-1)]
                return (self.cuadradoCompleto(lineaArriba, lineaAbajo, lineaIzquierda, lineaDerecha),1,'Izq', lineaArriba, linea)
            else: #La línea horizontal no se encuentra en los extremos superior o inferior del grid
                print("Llega")
                lineaMedio = [(x1,y1),(x2,y2)]
                lineaArriba_Der = [(x1, y1),(x1,y1+1)]
                lineaAbajo_Der = [(x2, y2),(x2,y2+1)]
                lineaDerecha = [(x1,y1+1),(x2,y2+1)]

                lineaArriba_Izq = [(x1, y1),(x1,y1-1)]
                lineaAbajo_Izq = [(x2, y2),(x2,y2-1)]
                lineaIzquierda = [(x1,y1-1),(x2,y2-1)]
                if(self.cuadradoCompleto(lineaArriba_Izq, lineaAbajo_Izq, lineaIzquierda, lineaMedio) == True and self.cuadradoCompleto(lineaArriba_Der, lineaAbajo_Der, lineaMedio, lineaDerecha) == True):
                    return (True, 2, 'MID', lineaArriba_Izq, lineaArriba_Der) #Medio izquierda y derecha, se rellenaron los dos cuadritos
                else:
                    if(self.cuadradoCompleto(lineaArriba_Izq, lineaAbajo_Izq, lineaIzquierda, lineaMedio)):
                        return (True, 1, 'Izq', lineaArriba_Izq, linea)
                    elif(self.cuadradoCompleto(lineaArriba_Der, lineaAbajo_Der, lineaMedio, lineaDerecha)):
                        return (True, 1, 'Der', lineaArriba_Der, linea)
        return (False, 0, 'ND', linea, linea)
            
class Jugador:
    def __init__(self, ficha):
        self.ficha = ficha
        self.puntaje = 0

    def actualizaPuntaje(self, cantidad):
        self.puntaje = self.puntaje + cantidad

    def obtenPuntaje(self):
        return self.puntaje

class Linea:
    def __init__(self, x1, y1, x2, y2):
        self.ocupada = False
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.coordenadas = []
        self.coordenadas.append((x1,y1)) #Agregamos las coordenadas de los dos puntos a una lista
        self.coordenadas.append((x2,y2))

    def activaLinea(self):
        self.ocupada = True
    
    def get_AllCoor(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_coordenadas(self):
        return self.coordenadas #Regresa una lista


if __name__ == '__main__':
    print("Inicio")
    tablero = Tablero()
    tablero.iniciaJuego()
    jugador1 = Jugador('H')
    jugador2 = Jugador('M')
    jugadorActual = jugador1
    while(not tablero.finDelJuego()):
        print("Turno de: "+jugadorActual.ficha)
        flag = tablero.juega(jugadorActual)
        while(flag):
            print("Turno de: "+jugadorActual.ficha)
            flag = tablero.juega(jugadorActual)
        if(jugadorActual.ficha == 'H'):
            jugadorActual = jugador2
        else:
            jugadorActual = jugador1
        print(" --- PUNTAJES ---")
        print("Humano: ",jugador1.obtenPuntaje())
        print("Máquina: ",jugador2.obtenPuntaje())