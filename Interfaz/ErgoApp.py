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
import cv2
import imutils

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
                            bg=self.fondooB, command=self.videoclick)
        self.bVideo.grid(row=4, column=2, columnspan=3, rowspan=1, sticky='e')

        self.bRegis = Button(self.frame1, text='Registro', font=('Hightower text', 40,'bold'), padx=90, pady=25,
                             bg=self.fondooB,command=self.regisclick)
        self.bRegis.grid(row=3, column=5, columnspan=3, rowspan=4, sticky='e')


    def democlick(self):
        self.frame1.destroy()
        #mostrar video

    def videoclick(self):
        self.frame1.destroy()

        self.frame2 = Frame(self, bg=self.fondoo, width=200, height=560)
        self.frame2.grid(row=0, column=2, columnspan=6, rowspan=12, sticky='nswe')

        self.cap = None

        self.btnIniciar = Button(self.frame2, text="Iniciar", width=45, command=self.iniciar)
        self.btnIniciar.grid(column=0, row=0, padx=5, pady=5)

        self.btnFinalizar = Button(self.frame2, text="Finalizar", width=45, command=self.finalizar)
        self.btnFinalizar.grid(column=1, row=0, padx=5, pady=5)

        self.btnAnalizar = Button(self.frame2, text="Analizar", width=45, command=self.analizarv)
        self.btnAnalizar.grid(column=2, row=0, padx=5, pady=5)

        self.lblVideo = Label(self.frame2)
        self.lblVideo.grid(column=0, row=1, columnspan=3)

    def analizarv(self):
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

        self.LabPAnBrazoD = Label(self.frame3, text='Puntaje antebrazo: ', font=('Hightower text', 20, 'bold'),
                                  bg=self.fondoo)
        self.LabPAnBrazoD.grid(row=6, column=1, columnspan=2, sticky='w', padx=20, pady=10)


        #izquierdo
        self.LabPBrazoI = Label(self.frame3, text='Puntaje brazo: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPBrazoI.grid(row=3, column=10, columnspan=2, sticky='w', padx=20, pady=10)

        self.LabPAnBrazoI = Label(self.frame3, text='Puntaje antebrazo: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPAnBrazoI.grid(row=6, column=10, columnspan=2, sticky='w', padx=20, pady=10)

        #cuello
        self.LabPCuello = Label(self.frame3, text='Puntaje cuello: ', font=('Hightower text', 20, 'bold'),
                                  bg=self.fondoo)
        self.LabPCuello.grid(row=10, column=5, columnspan=3, sticky='W', pady=10)

        #puntaje total
        self.LabPtotal = Label(self.frame3, text='PUNTAJE TOTAL: ', font=('Hightower text', 20, 'bold'),
                                bg=self.fondoo)
        self.LabPtotal.grid(row=12, column=5, columnspan=3, sticky='W', pady=20)

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
        self.visualizar()

    def visualizar(self):
        #global cap
        if self.cap is not None:
            self.ret, self.frame = self.cap.read()
            if self.ret == True:
                self.frame = imutils.resize(self.frame, width=640)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                self.im = Image.fromarray(self.frame)
                self.img = ImageTk.PhotoImage(image=self.im)

                self.lblVideo.configure(image=self.img)
                self.lblVideo.image = self.img
                self.lblVideo.after(10, self.visualizar)
            else:
                self.lblVideo.image = ""
                self.cap.release()


    def finalizar(self):
        #global cap
        self.cap.release()
        #aqui debe estar el analisis del video


    def restar(self):
        self.destroy()
        self.pagprin()

    def info(self):
        box.showinfo("Instructivo",
                     "1. Elegir si será Demo o Video\n2. Registrar los datos"
                     "\n3. Esperar el analisis\n4. Revisar los resultados")

