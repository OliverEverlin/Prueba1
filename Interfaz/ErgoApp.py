#Proyecto de SIGA
#Grupo 3

##Desarrollado por:
##Itala Latorre Dueñas
##72577402

from tkinter import *
import tkinter.messagebox as box
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import time
import cv2
import imutils
import PoseModule as pm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ErgoMetric(Tk):
    def __init__(self):
        super().__init__()

        self.pagprin()

        self.mainloop()


    def pagprin(self):
        self.title("Ergo Metric App")
        self.geometry('1000x1000')  #400x400 originalmente
        self.iconbitmap('ergo.ico')
        #self.resizable(0,0)
        
        self.fondoo='gray'
        self.fondooB='#727171'
        self.colorbtt='white'
        
        self.configure(bg=self.fondoo)
        
        #menu
        self.mymenu=Menu(self)
        self.config(menu=self.mymenu)
        self.filemenu = Menu(self.mymenu)
        self.helpmenu = Menu(self.mymenu)
        
        self.mymenu.add_cascade(label="Archivo", menu=self.filemenu)
        self.mymenu.add_cascade(label="Ayuda", menu=self.helpmenu)

        #self.filemenu = Menu(self.mymenu, tearoff=0)
        #self.helpmenu = Menu(self.mymenu, tearoff=0)
        
        #self.filemenu = Menu(self.filemenu, tearoff=0)
        self.filemenu.add_command(label="Reiniciar",command=self.restar)
        #self.filemenu.add_command(label="Abrir")
        #self.filemenu.add_command(label="Guardar")
        #self.filemenu.add_command(label="Cerrar")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.quit)

        #self.helpmenu = Menu(self.mymenu, tearoff=0)
        #self.helpmenu.add_command(label="Ayuda")
        #self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Info",command=self.info)

        #icono de ventana
        #self.iconphoto(False,PhotoImage(file='ergo.ico'))

        #variables string
        self.varmodo = StringVar()
        self.varmodo.set('RULA')
        self.modo=''
        self.varss = StringVar()
        self.varss.set('')

        self.detector = pm.poseDetector()
        self.count = 0

        #self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        

        #imagenes
        self.KsT = ImageTk.PhotoImage(file='ErgoMetricAPP (1).png')
        self.regispng = ImageTk.PhotoImage(file='ErgoMetricAPP.png')
        self.actor = ImageTk.PhotoImage(file='human1.png')


        self.defframe1()
        #self.mainloop()

    def defframe1(self):
        #frame general de demo mas video
        self.frame1=Frame(self,bg=self.fondoo,width=200, height=560)
        self.frame1.grid(row=0,column=2,columnspan=6,rowspan=12,sticky='nswe')
        
        self.titulo=Label(self.frame1,image=self.KsT,bg=self.fondoo)
        self.titulo.grid(row=0,column=1,columnspan=8,rowspan=2,sticky='we',padx=200,pady=100)
        
        self.bDemo=Button(self.frame1,text='Demo',font=('Hightower text', 40,'bold'),padx=90,pady=25,
                          bg=self.fondooB,command=self.democlick)
        self.bDemo.grid(row=3,column=2,columnspan=3,rowspan=1,sticky='e')

        self.bVideo = Button(self.frame1, text='Video', font=('Hightower text', 40, 'bold'), padx=90, pady=25,
                            bg=self.fondooB, command=self.iniciar)
        self.bVideo.grid(row=4, column=2, columnspan=3, rowspan=1, sticky='e')

        self.bRegis = Button(self.frame1, text='Registro', font=('Hightower text', 40,'bold'), padx=90, pady=25,
                             bg=self.fondooB,command=self.regisclick)
        self.bRegis.grid(row=3, column=5, columnspan=3, rowspan=4, sticky='e')


    def democlick(self):
        self.frame1.destroy()
        #mostrar video
        cap = cv2.VideoCapture('PoseVideos/curls.mp4')  # Poner el nombre de la carpeta del video que usarás
        # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        pTime = 0
        detector = pm.poseDetector()
        count = 0
        dir = 0  # 1 para cuando sube, 0 para cuando baja

        # Definicion de listas -----------------------------------------------
        pandasl = []
        filas = []
        angulos = []
        punto_angulos = []

        # Determinare el grupo A
        ## Puntuación del brazo
        estiramiento = []
        punto_estiramiento = []
        antebrazoD = []
        punto_antebrazoD = []
        antebrazoI = []
        punto_antebrazoI = []

        while True:
            # img = cv2.imread("PoseVideos/curls1.jpg")
            success, img = cap.read()

            # IF: Como filtro de valores atípicos
            if img is not None:
                img = detector.findPose(img, False)
                # success, img = cap.read()
                # img = detector.findPose(img)
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:

                    # Angulo de brazo respecto al torso (puntuaciones)
                    angBDT = detector.findAngle(img, 14, 12, 24)

                    pBDT = 0  # Puntuacion del brazo
                    if (angBDT < 20):
                        pBDT = 1
                    elif (angBDT < 45):
                        pBDT = 2
                    elif (angBDT < 90):
                        pBDT = 3
                    else:
                        pBDT = 4

                    pp = 0
                    # +1 Hombro elevado,
                    LargeD = detector.findDistance(img, 12, 24)
                    LargeBrazo = detector.findDistance(img, 12, 14)
                    # print(LargeD)
                    if LargeD > LargeBrazo * 1.05:
                        pp = pp + 1
                    # +1 brazo rotado
                    vector_cuerpo = detector.findVector(img, 12, 11)
                    vector_plano_mano = np.cross(detector.findVector(img, 16, 20), detector.findVector(img, 18, 16))
                    dif = abs(vector_cuerpo[2] - vector_plano_mano[2])
                    if dif > 50:
                        pp = pp + 1
                    # +1 brazos abducidos
                    # d = detector.finddistance(img,24,12,14)
                    # if d > 300:
                    #    pp = pp + 1
                    # - 1 apoyo en el punto

                    # Angulo de antebrazos (puntuaciones)
                    # Derecha
                    angD = detector.findAngle(img, 12, 14, 16)
                    # Izquierda
                    angI = detector.findAngle(img, 11, 13, 15)
                    if angD > 60 and angD < 100:
                        pAntebrazoD = 1
                    else:
                        pAntebrazoD = 2

                    if angI > 60 and angI < 100:
                        pAntebrazoI = 1
                    else:
                        pAntebrazoI = 2

                    per = np.interp(angI, (30, 160), (100, 0))
                    bar = np.interp(angI, (30, 160), (100, 650))  # el minimo y el maximo son diferentes para open cv
                    # print(int(angI),per)

                # Estimación de FPS
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 255, 255), 5)

                # Reajuste de tamaños: si la imagen sale muy grande o pequeña solo cambia el valor de la escala
                escala = 0.3
                width, height, _ = img.shape
                alto = int(width * escala)
                ancho = int(height * escala)
                img = cv2.resize(img, (ancho, alto))
                cv2.imshow("Image", img)
                cv2.waitKey(1)

                count += 1

                # Almacenamiento de datos: Se alamacena all en una lista
                filas.append(count)
                pandasl.append(1)
                estiramiento.append(int(LargeD))
                punto_estiramiento.append(int(pp))
                angulos.append(int(angBDT))
                punto_angulos.append(int(pBDT))
                antebrazoD.append(int(angD))
                antebrazoI.append(int(angI))
                punto_antebrazoD.append(int(pAntebrazoD))
                punto_antebrazoI.append(int(pAntebrazoI))
                # time.sleep(0.5)
            else:
                ##Se filtrará este valor después
                pandasl.append(-10)
                break

        # Termina el bucle ----------------------------------

        ##Post procesado
        # Analizo los estiramientos
        print("POST")

        # +1 Hombro elevado, brazo rotado, brazos abducidos
        # for i in range(len(estiramiento)):
        #    print(estiramiento[i])
        # Almacenamiento para analizis de datos
        # with open("2.csv", "w", newline="") as archivo:
        #     writer = csv.writer(archivo)
        #     writer.writerow([filas, pandasl,estiramiento])

        # Crear un objeto DataFrame

        ##Impresión de numero de valores tomados
        print("Se crea el DF")
        # print(len(filas))
        # #print(len(pandasl))
        # print(len(angulos))
        # print(len(punto_angulos))
        # print(len(estiramiento))
        # print(len(punto_estiramiento))
        # print(len(antebrazoD))
        # print(len(punto_antebrazoD))
        # print(len(antebrazoI))
        # print(len(punto_antebrazoI))
        # Se almacenan las listas en el DF
        df = pd.DataFrame({
            "Columna_1": filas,
            # "Columna 2": pandasl,
            "Columna_3": angulos,
            "Columna_4": punto_angulos,
            "Columna_5": estiramiento,
            "columna_6": punto_estiramiento,
            "Columna_7": antebrazoD,
            "Columna_8": punto_antebrazoD,
            "Columna_9": antebrazoI,
            "Columna_10": punto_antebrazoI
        })

        # Guardar el DataFrame en un archivo CSV
        df.to_csv("4.csv")
        print(df)
        # - apoyo en el punto

        # graficas puntos angulos
        print("Debería comenzar a graficar")
        puntos_a = df["Columna_4"].value_counts()
        puntos_a.plot.pie()
        df.plot(kind="scatter", x='Columna_1', y='Columna_4')
        plt.show()

        # graficas puntos estiramiento
        # puntos_b=df["Columna_6"].value_counts()
        # puntos_b.plot.pie()
        # df.plot(kind = "scatter", x = 'Columna 1', y = 'Columna 6')

        # graficas puntos antebrazo D e I
        puntos_c = df["Columna_8"].value_counts()
        puntos_c.plot.pie()
        df.plot(kind="scatter", x='Columna_1', y='Columna_8')
        plt.show()

        puntos_d = df["Columna_10"].value_counts()
        puntos_d.plot.pie()
        df.plot(kind="scatter", x='Columna_1', y='Columna_10')
        plt.show()


    def videoclick(self):
        self.frame1.destroy()

        self.frame2 = Frame(self, bg=self.fondoo, width=200, height=560)
        self.frame2.grid(row=0, column=2, columnspan=6, rowspan=12, sticky='nswe')

        self.cap = None

        self.btnIniciar = Button(self.frame2, text="Iniciar", width=45, command=self.iniciar)
        self.btnIniciar.grid(column=0, row=0, padx=5, pady=5)

        self.btnFinalizar = Button(self.frame2, text="Finalizar", width=45, command=self.finalizar)
        self.btnFinalizar.grid(column=1, row=0, padx=5, pady=5)

        #self.btnAnalizar = Button(self.frame2, text="Analizar", width=45, command=self.analizarv)
        #self.btnAnalizar.grid(column=2, row=0, padx=5, pady=5)

        self.lblVideo = Label(self.frame2)
        self.lblVideo.grid(column=0, row=1, columnspan=3)

    def analizarv(self):
        self.PBRder=0
        self.PBRizq=0
        self.PABRder=0
        self.PABRizq=0
        self.PCuello=0
        self.PTOTAL=0

        #self.ppoint = Toplevel()
        #self.ppoint.title('Registro')
        #self.ppoint.geometry('1000x1000')
        #self.ppoint.iconbitmap('ergo.ico')
        #self.ppoint.configure(bg=self.fondoo)

        self.frame3 = Frame(self, bg=self.fondoo, width=300, height=600)
        self.frame3.grid(row=0, column=0, columnspan=12, rowspan=15, sticky='nswe')

        self.Labtitle = Label(self.frame3, text='Puntajes', font=('Hightower text', 50, 'bold'),
                                   bg=self.fondoo)
        self.Labtitle.grid(row=0, column=1, columnspan=12, sticky='we', padx=200, pady=30)

        self.actim = Label(self.frame3, image=self.actor, bg=self.fondoo)
        self.actim.grid(row=1, column=4, columnspan=4, rowspan=8, sticky='we', padx=50, pady=20)

        #derecho
        self.LabPBrazoD = Label(self.frame3, text='Puntaje brazo: ', font=('Hightower text', 20, 'bold'),
                              bg=self.fondoo)
        self.LabPBrazoD.grid(row=3, column=1, columnspan=2, sticky='w', padx=20, pady=10)

        self.PBrazoD = Label(self.frame3, text=str(self.PBRder), font=('Hightower text', 20, 'bold'),
                                       bg=self.fondoo)
        self.PBrazoD.grid(row=4, column=1, columnspan=2, sticky='wE', padx=20, pady=10)


        self.LabPAnBrazoD = Label(self.frame3, text='Puntaje antebrazo: ', font=('Hightower text', 20, 'bold'),
                                  bg=self.fondoo)
        self.LabPAnBrazoD.grid(row=6, column=1, columnspan=2, sticky='w', padx=20, pady=10)
        self.PAnBrazoD = Label(self.frame3, text=str(self.PABRder),
                                         font=('Hightower text', 20, 'bold'),
                                         bg=self.fondoo)
        self.PAnBrazoD.grid(row=7, column=1, columnspan=2, sticky='wE', padx=20, pady=10)


        #izquierdo
        self.LabPBrazoI = Label(self.frame3, text='Puntaje brazo: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPBrazoI.grid(row=3, column=10, columnspan=2, sticky='w', padx=20, pady=10)
        self.PBrazoI = Label(self.frame3, text=str(self.PBRizq), font=('Hightower text', 20, 'bold'),
                                       bg=self.fondoo)
        self.PBrazoI.grid(row=4, column=10, columnspan=2, sticky='wE', padx=20, pady=10)


        self.LabPAnBrazoI = Label(self.frame3, text='Puntaje antebrazo: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPAnBrazoI.grid(row=6, column=10, columnspan=2, sticky='w', padx=20, pady=10)
        self.PAnBrazoI = Label(self.frame3, text=str(self.PABRizq),
                                         font=('Hightower text', 20, 'bold'),
                                         bg=self.fondoo)
        self.PAnBrazoI.grid(row=7, column=10, columnspan=2, sticky='wE', padx=20, pady=10)

        #cuello
        self.LabPCuello = Label(self.frame3, text='Puntaje cuello: ', font=('Hightower text', 20, 'bold'),
                                  bg=self.fondoo)
        self.LabPCuello.grid(row=10, column=5, columnspan=3, sticky='W', pady=10)
        self.PCuelloT = Label(self.frame3, text=str(self.PCuello), font=('Hightower text', 20, 'bold'),
                                       bg=self.fondoo)
        self.PCuelloT.grid(row=11, column=5, columnspan=3, sticky='WE', pady=10)

        #puntaje total
        self.LabPtotal = Label(self.frame3, text='PUNTAJE TOTAL: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPtotal.grid(row=12, column=5, columnspan=3, sticky='W', pady=20)
        self.Ptotal = Label(self.frame3, text=str(self.PTOTAL), font=('Hightower text', 20, 'bold'),
                                      bg=self.fondoo)
        self.Ptotal.grid(row=13, column=5, columnspan=3, sticky='WE', pady=20)



    def regisclick(self):
        #self.frame1.destroy()
        self.regis = Toplevel()
        self.regis.title('Registro')
        self.regis.geometry('300x500')
        self.regis.iconbitmap('ergo.ico')
        self.regis.configure(bg=self.fondoo)

        # barra lateral izquierda del interfaz
        self.regis.lateralI = Frame(self.regis, bg=self.fondoo, width=100, height=500)
        self.regis.lateralI.grid(row=0, column=2, columnspan=6, rowspan=12, sticky='ns')

        self.regis.titulo = Label(self.regis.lateralI, image=self.regispng, bg=self.fondoo)
        self.regis.titulo.grid(row=0, column=2, columnspan=3, rowspan=2, sticky='we',padx=20,pady=10)

        self.regis.LabName = Label(self.regis.lateralI, text='Nombre: ', font=('Hightower text', 12, 'bold'), bg=self.fondoo,
                             justify=RIGHT)
        self.regis.LabName.grid(row=3, column=2, columnspan=3, sticky='w',padx=20,pady=10)

        self.regis.EntryName = Entry(self.regis.lateralI, width=30, fg='red', justify=RIGHT)
        self.regis.EntryName.grid(column=2, row=4, columnspan=3, sticky='w',padx=30)

        self.regis.LabLastName = Label(self.regis.lateralI, text='Apellido: ', font=('Hightower text', 12, 'bold'), bg=self.fondoo,
                                 justify=RIGHT)
        self.regis.LabLastName.grid(row=5, column=2, columnspan=3, sticky='w',padx=20,pady=10)

        self.regis.EntryLastName = Entry(self.regis.lateralI, width=30, fg='black', justify=RIGHT)
        self.regis.EntryLastName.grid(column=2, row=6, columnspan=3, sticky='w',padx=30)

        self.regis.LabAge = Label(self.regis.lateralI, text='Edad: ', font=('Hightower text', 12, 'bold'), bg=self.fondoo,
                            justify=RIGHT)
        self.regis.LabAge.grid(row=7, column=2, columnspan=3, sticky='w',padx=20,pady=10)

        self.regis.EntryAge = Entry(self.regis.lateralI, width=30, fg='black', justify=RIGHT)
        self.regis.EntryAge.grid(column=2, row=8, columnspan=3, sticky='w',padx=30)

        self.regis.LabAges = Label(self.regis.lateralI, text=' años', font=('Hightower text', 12, 'bold'),
                                  bg=self.fondoo,
                                  justify=RIGHT)
        self.regis.LabAges.grid(row=8, column=5,sticky='w', pady=10)

        self.regis.LabPeso = Label(self.regis.lateralI, text='Peso: ', font=('Hightower text', 12, 'bold'), bg=self.fondoo,
                             justify=RIGHT)
        self.regis.LabPeso.grid(row=9, column=2, columnspan=3, sticky='w',padx=20,pady=10)

        self.regis.EntryPeso = Entry(self.regis.lateralI, width=30, fg='black', justify=LEFT)
        self.regis.EntryPeso.grid(column=2, row=10, columnspan=3, sticky='w',padx=30)

        self.bAceptar = Button(self.regis.lateralI, text='Registrar', font=('Hightower text', 20, 'bold'), padx=5, pady=5,
                            bg=self.fondooB, command=self.regisAclick)
        self.bAceptar.grid(row=12, column=2, columnspan=3, rowspan=2, sticky='e',padx=50,pady=40)

    def regisAclick(self):
        #guardar datos para registro
        self.regis.destroy()

    def iniciar(self):
        #global self.cap
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.analizarv()
        self.visualizar()



    def visualizar(self):
        #global cap

        while self.cap is not None:
            success, img = self.cap.read()

            # IF: Como filtro de valores atípicos
            if img is not None:
                img = self.detector.findPose(img, False)
                lmList = self.detector.findPosition(img, False)

                # SI se encontró un cuerpo se procesará y mostrará esa data
                if len(lmList) != 0:
                    # CALCULO BRAZO--------------------------------------------------------
                    # Angulo de brazo respecto al torso (puntuaciones)

                    # DERECHA ---------------------------
                    BRder = abs(self.detector.findAngle3D(img, 14, 12, 24))
                    self.PBRder = self.detector.brazoPuntuation(BRder)

                    # IZQUIERDA ---------------------------
                    BRizq = abs(self.detector.findAngle3D(img, 13, 11, 23))
                    self.PBRizq = self.detector.brazoPuntuation(BRizq)

                    # CALCULO ANTEBRAZOS ---------------------------------------------------------------
                    # DERECHA ---------------------------
                    ABRder = abs(self.detector.findAngle3D(img, 12, 14, 16))
                    self.PABRder = self.detector.anteBrazoPuntuation(BRder)

                    # IZQUIERDA ---------------------------
                    ABRizq = abs(self.detector.findAngle3D(img, 11, 13, 15))
                    self.PABRizq = self.detector.anteBrazoPuntuation(BRizq)

                    # CALCULO CUELLO ---------------------------------------------------------------
                    # Promediacion
                    head = []
                    budy = []
                    head = self.detector.promDot(img, 7, 8)
                    budy = self.detector.promDot(img, 23, 24)
                    cuello = self.detector.promDot(img, 11, 12)

                    ANGcuello = (self.detector.findAngle3DbyVectors(img, head, cuello, budy, draw=True))
                    self.PCuello = self.detector.cuelloPuntuation(ANGcuello)

                    # PUNTAJE TOTAL
                    self.TOTAL = self.PBRder + self.PBRizq + self.PABRder + self.PABRizq + self.PCuello
                    # Todos estos valores impresos en el forms

                    self.PBrazoD['text'] = str(self.PBRder)
                    self.PBrazoI['text'] = str(self.PBRizq)
                    self.PAnBrazoD['text'] = str(self.PABRder)
                    self.PAnBrazoI['text'] = str(self.PABRizq)
                    self.PCuelloT['text'] = str(self.PCuello)
                    self.Ptotal['text'] = str(self.PTOTAL)

                # Reajuste de tamaños: si la imagen sale muy grande o pequeña solo cambia el valor de la escala
                escala = 1
                width, height, _ = img.shape
                alto = int(width * escala)
                ancho = int(height * escala)
                img = cv2.resize(img, (ancho, alto))
                cv2.imshow("Image", img)
                cv2.waitKey(1)

                self.count += 1

            else:
                ##En caso haya un error, se mantiene el valor anterior
                pass


    def finalizar(self):
        #global cap
        self.cap.release()
        self.ppoint.destroy()


    def restar(self):
        self.destroy()
        self.pagprin()

    def info(self):
        box.showinfo("Instructivo",
                     "1. Elegir si será Demo o Video\n2. Registrar los datos"
                     "\n3. Esperar el analisis\n4. Revisar los resultados")

