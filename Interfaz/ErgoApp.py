#Proyecto de SIGA
#Grupo 3

##Desarrollado por:
##Itala Latorre Dueñas
##72577402

from tkinter import *
import tkinter.messagebox as box
from PIL import ImageTk
from tkinter import filedialog

class ErgoMetric(Tk):
    def __init__(self):
        super().__init__()

        self.title("Ergo Metric App")
        self.geometry('400x400')
        self.iconbitmap('ergo.ico')
        self.resizable(0,0)
        
        self.fondoo='gray'
        self.colorbtt='white'
        
        self.configure(bg=self.fondoo)
        
        #menu
        self.mymenu=Menu(self)
        self.config(menu=self.mymenu)
        filemenu = Menu(self.mymenu)
        editmenu = Menu(self.mymenu)
        helpmenu = Menu(self.mymenu)
        
        self.mymenu.add_cascade(label="Archivo", menu=filemenu)
        self.mymenu.add_cascade(label="Editar", menu=editmenu)
        self.mymenu.add_cascade(label="Ayuda", menu=helpmenu)

        #self.filemenu = Menu(self.mymenu, tearoff=0)
        #self.editmenu = Menu(self.mymenu, tearoff=0)
        #self.helpmenu = Menu(self.mymenu, tearoff=0)
        
        filemenu = Menu(self.mymenu, tearoff=0)
        filemenu.add_command(label="Nuevo")
        filemenu.add_command(label="Abrir")
        filemenu.add_command(label="Guardar")
        filemenu.add_command(label="Cerrar")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.quit)
        
        editmenu = Menu(self.mymenu, tearoff=0)
        editmenu.add_command(label="Cortar")
        editmenu.add_command(label="Copiar")
        editmenu.add_command(label="Pegar")

        helpmenu = Menu(self.mymenu, tearoff=0)
        helpmenu.add_command(label="Ayuda")
        helpmenu.add_separator()
        helpmenu.add_command(label="Acerca de...")

        #icono de ventana
        #self.iconphoto(False,PhotoImage(file='ergo.ico'))

        #variables string
        self.varmodo = StringVar()
        self.varmodo.set('RULA')
        self.modo=''
        self.varss = StringVar()
        self.varss.set('')
        

        #imagenes
        self.back = ImageTk.PhotoImage(file='back1.png')
        self.restar = ImageTk.PhotoImage(file='restar1.png')
        self.KsT = ImageTk.PhotoImage(file='ErgoMetricAPP.png')
    
    
        #barra lateral izquierda del interfaz
        self.lateralI=Frame(self,bg=self.fondoo,width=100, height=500)
        self.lateralI.grid(row=0,column=2,columnspan=6,rowspan=12,sticky='ns')
        
        self.titulo=Label(self.lateralI,image=self.KsT,bg=self.fondoo)
        self.titulo.grid(row=0,column=2,columnspan=3,rowspan=2,sticky='we')
        
        self.LabName=Label(self.lateralI,text='Nombre: ',font = ('Hightower text', 12,'bold'), bg=self.fondoo,justify=RIGHT)
        self.LabName.grid(row=3,column=2,columnspan=3,sticky='w')
        
        self.EntryName=Entry(self.lateralI,width=30,fg='red',justify=RIGHT)
        self.EntryName.grid(column=2,row=4,columnspan=3,sticky='w')

        self.LabLastName=Label(self.lateralI,text='Apellido: ',font = ('Hightower text', 12,'bold'), bg=self.fondoo,justify=RIGHT)
        self.LabLastName.grid(row=5,column=2,columnspan=3,sticky='w')

        self.EntryLastName=Entry(self.lateralI,width=30,fg='black',justify=RIGHT)
        self.EntryLastName.grid(column=2,row=6,columnspan=3,sticky='w')
        
        self.LabAge=Label(self.lateralI,text='Edad: ',font = ('Hightower text', 12,'bold'), bg=self.fondoo,justify=RIGHT)
        self.LabAge.grid(row=7,column=2,columnspan=3,sticky='w')

        self.EntryAge=Entry(self.lateralI,width=30,fg='black',justify=RIGHT)
        self.EntryAge.grid(column=2,row=8,columnspan=3,sticky='w')
        
        self.LabPeso=Label(self.lateralI,text='Peso: ',font = ('Hightower text', 12,'bold'), bg=self.fondoo,justify=RIGHT)
        self.LabPeso.grid(row=9,column=2,columnspan=3,sticky='w')

        self.EntryPeso=Entry(self.lateralI,width=30,fg='black',justify=LEFT)
        self.EntryPeso.grid(column=2,row=10,columnspan=3,sticky='w')
        
        
        #barra lateral de datos de la tabla
        self.lateral=Frame(self,bg=self.fondoo,width=100, height=500)
        self.lateral.grid(row=3,column=9,columnspan=3,rowspan=12,sticky='ns')

        self.Binstru=Button(self.lateral,text='Instrucciones', font = ('Hightower text', 12,'bold'), bg = self.colorbtt,command=self.indicaciones)
        self.Binstru.grid(row=3,column=9,columnspan=3,sticky='we',padx=10,pady=3)

        self.l2=Label(self.lateral,text='Tipo:',justify=LEFT,font = ('Hightower text', 12,'bold'), bg=self.fondoo)
        self.l2.grid(row=4,column=9,columnspan=3,sticky='w',padx=10,pady=3)
        
        ####TIPO DE EVALUACION
        self.r1=Radiobutton(self.lateral, text="REBA",variable=self.varmodo,value='REBA',state=DISABLED,bg=self.fondoo,font = ('Hightower text', 12,'bold'), command=self.selectModo)
        self.r1.grid(row=5,column=9,columnspan=3,sticky='w',padx=20,pady=3)
        
        self.r2=Radiobutton(self.lateral, text="RULA",variable=self.varmodo,value='RULA',state=NORMAL,bg=self.fondoo,font = ('Hightower text', 12,'bold'), command=self.selectModo)
        self.r2.grid(row=6,column=9,columnspan=3,sticky='w',padx=20,pady=3)
        
        self.r3=Radiobutton(self.lateral, text="OWAS",variable=self.varmodo,value='OWAS',state=DISABLED,bg=self.fondoo,font = ('Hightower text', 12,'bold'), command=self.selectModo)
        self.r3.grid(row=7,column=9,columnspan=3,sticky='w',padx=20,pady=3)
        
        self.r4=Radiobutton(self.lateral, text="NIOSH",variable=self.varmodo,value='NIOSH',state=DISABLED,bg=self.fondoo,font = ('Hightower text', 12,'bold'), command=self.selectModo)
        self.r4.grid(row=8,column=9,columnspan=3,sticky='w',padx=20,pady=3)


        self.fileO=Button(self.lateral,text='.',command=self.files)
        self.fileO.grid(row=9,column=9,sticky='w',padx=20,pady=3)

        self.label1=Label(self.lateral, text='Subir Video', bg=self.fondoo)
        self.label1.grid(row=9,column=10,columnspan=3,sticky='w',padx=20,pady=3)


        self.Bback=Button(self,image=self.back, bg = self.colorbtt,state=DISABLED,command=self.backone)
        self.Bback.grid(row=0,column=9,sticky='we')#,padx=5,pady=5)
        self.Brstar=Button(self,image=self.restar, bg = self.colorbtt,state=DISABLED,command=self.reinicio)
        self.Brstar.grid(row=0,column=10,sticky='we')#,padx=5,pady=5)

        self.mainloop()
        
        
    

    def files(self):
        self.filename=filedialog.askopenfilename(initialdir="D:\Coding\ErgoMetric",title='Select File',filetypes=(('mp4 files','*.mp4'),('all files','*.*')))


    def selectModo(self):   #selecciona el modo de juego
        self.modo=self.varmodo.get()

    def indicaciones(self):   
        box.showinfo( "Instructivo","1. Ingreso los datos del evaluado\n2. Seleccionar el tipo de evaluación\n3. Añadir el video grabado\n4. Esperar el analisis\n5. Revisar los resultados")
        

    def reinicio(self):
        return

    def backone(self):
        return



