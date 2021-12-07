import cv2     #Procesamiento de imagenes
from tkinter import *   #Interfaz
import sounddevice as sd  #Reproducir sonido
import soundfile as sf   #Leer sonido
import threading as th   #Gestionar operaciones paralelas
import time      #Saber cuando finaliza los audios



def jugar():
    #Inicializamos ciertos parametros
    global cap, nov, contador, rostro, jugadores

    #Contador de jugadores
    contador = 0

    #Extraemos el numero de jugadores
    jugadores = entrada.get()
    jugadores = int(jugadores)


    #Deteccion de rostro
    rostro =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #Realizamos la videocaptura
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    #Llamamos al metodo de deteccion de movimiento
    mov = cv2.createBackgroundSubtractorKNN(history=50,dist2Threshold=2500, detectShadows=False)

    #Deshabilitamos OpenCL
    cv2.ocl.setUseOpenCL(False)

    #Funcion de audio
    def audio(archivo):
        global hilo, inicio
        inicio = time.time()
        #Leemos el audio
        data, fs = sf.read(archivo)
        #Reproduccion del audio
        sd.play(data, fs)

    #Funcion para preguntar si termino el audio
    def check2(hilo):
        fin = time.time()
        tiempo = int(fin - inicio)
        #Print (tiempo)
        if tiempo > 6:
            Verde()

    #Funcion para preguntar si termino el audio
    def check(hilo):
        fin = time.time()
        tiempo = int(fin - inicio)
        #Print (tiempo)
        if tiempo > 6:
            Roja()
    
    #Funcion luz Roja
    def Roja():
        #Declaramos variables globales
        global jugadores, contador, dis

        #Declaramos variable para disminuir jugadores
        dis = 0

        #Asignamos un hilo para reproducir el sonido
        archivo = 'Roja.wav'
        hilo = th.Thread(target=audio,args=(archivo,))
        hilo.start()

        #Creamos nuestro while True
        while True:
            check2(hilo)
            #Lectura de la videocaptura
            ret, frame = cap.read()

            #Aplicamos un filtro Gaussiano
            filtro = cv2.GaussianBlur(frame,(31,31),0)
        
            #Aplicamos el metodo de deteccion de movimiento
            mascara = mov.apply(filtro)
            
            #Creamos una copia
            copy = mascara.copy()

            #Buscamos los contornos
            contornos, jerarquia = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #Mostrar los jugadores restantes
            cv2.putText(frame, f"JUGADORES RESTANTES: {str(jugadores)} ", (150,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),2)

            #Dibujar los contornos
            for con in contornos:
                #Borramos los contornos pequeños
                if cv2.contourArea(con) < 5000:
                    continue

                #Obtener las coordenadas del contorno
                (x, y, an, al) = cv2.boundingRect(con)




                #Detectamos el rostro
                copia = frame.copy()
                gris = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
                caras = rostro.detectMultiScale(gris, 1.3,5)

                #Detecto el rostro del jugador que perdio
                for (x2, y2, an, al) in caras:
                    #Dibujamos el rectangulo en el rostro
                    cv2.rectangle(frame, (x2,y2), (x2 + an, y2 + al), (0,0,255), 2)

                    #Escribimos jugador eliminado
                    cv2.putText(frame, f"JUGADOR {str(contador)} ELIMINADO", (x2 - 70, y2 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0 , 255),2)

                    #Numero de jugadores muertos
                    muerte = len(caras)

                    #Disminuimos el contador
                    if dis == 0:
                        contador = contador + muerte

                        #Disminuimos el numero de jugadoreS restantes
                        jugadores = jugadores - muerte

                        #Cambiamos la llave
                        dis = 1

                        if jugadores <= 0:
                            #Cerramos el juego
                            cerrar()
                
            # Mostramos los frames
            cv2.imshow("ESTATE ATENTO", frame)

            # Condicion para romper el while
            t = cv2.waitKey(1)
            if t == 27:
                cerrar()

    #Funcion luz verde
    def Verde():
        #Asignamos un hilo para reproducir el sonido
        archivo = "Verde.wav"
        hilo = th.Thread(target = audio, args = (archivo, ))
        hilo.start()

        #Creamos nuestro while True
        while True:
            check(hilo)
            #Lectura de la videocaptura
            ret,frame = cap.read()

            #Aplicamos un filtro Gaussiano
            filtro = cv2.GaussianBlur(frame, (31,31), 0)
            
            #Aplicamos el metodo de deteccion de movimiento
            mascara = mov.apply(filtro)
                
            #Creamos una copia
            copy = mascara.copy()

            #Buscamos los contornos
            contornos, jerarquia = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #Mostrar los jugadores restantes
            cv2.putText(frame, f"JUGADORES RESTANTES: {str(jugadores)} ", (150,50), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 2)

            #Dibujar los contornos
            for con in contornos:
                #Borramos los contornos pequeños
                if cv2.contourArea(con) < 5000:
                    continue

                #Obtener las coordenadas del contorno
                (x, y, an, al) = cv2.boundingRect(con)

                #Dibujamos el rectangulo
                cv2.rectangle(frame, (x,y), (x + an, y + al), (0,255,0), 2)

            # Mostramos los frames
            cv2.imshow("ESTATE ATENTO", frame)

            # Condicion para romper el while
            t = cv2.waitKey(1)
            if t == 27:
                cerrar()
        
    Verde()

def cerrar():
    #Cerramos la ventana
    cv2.destroyAllWindows()
    cap.release()

    # Mostramos la pantalla FinaL
    global pantalla2
    pantalla2 = Toplevel()
    pantalla2.title("BEAWARE")
    pantalla2.geometry("1280x720")
    imagen2 = PhotoImage(file="Fin.png")

    # Creamos la plantilla para diseñar cambios en ella
    plantilla2 = Canvas(pantalla2, width=1280, height=720)

    fondo = Label(pantalla2, image=imagen2)
    fondo.place(x=0, y=0, relwidth = 1, relheight = 1)

    plantilla2.pack()

    pantalla2.mainloop()


def pantalla_principal():
    global pantalla, entrada
    pantalla = Tk()
    pantalla.title("BEAWARE")    #Titulo de la pantalla
    pantalla.geometry("1280x720")             #Dimension de la pantalla
    imagen = PhotoImage(file="Fondo.png")     #Leemos la imagen de fondo

    #Creamos a plantilla para diseñar sobre ella
    plantilla1 = Canvas(pantalla, width=1280, height=720)
    plantilla1.pack(fill="both", expand=True)
    plantilla1.create_image(0,0, image = imagen, anchor = "nw")

    #Imagen Boton 1
    img1 = PhotoImage(file="Jugar.png")
    #Imagen Boton 2
    img2 = PhotoImage(file="Cerrar.png")

    #Creamos los botones

    #Boton 1
    boton1 = Button(pantalla, text="JUGAR", height="40", width="300", command = jugar, image = img1)
    boton1pla = plantilla1.create_window(310,580, anchor="nw", window=boton1)

    #Boton 2
    boton2 = Button(pantalla, text="CERRAR", height="40", width="300", command = cerrar, image = img2)
    boton2pla = plantilla1.create_window(705,580, anchor="nw", window=boton2)

    #Entrada de numero de jugadores
    jugadores = StringVar()
    entrada = Entry(pantalla, textvariable=jugadores)
    entradapla = plantilla1.create_window(595,650, anchor="nw", window=entrada)

    pantalla.mainloop()

pantalla_principal()
