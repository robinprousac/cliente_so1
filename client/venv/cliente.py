from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.ttk import *
import datetime
import threading
import time
import logging
import http.client
import random

line = ""
lineas = []

solicitudesok = 0
solicitudeserror = 0
total_solicitudes = 0
total_progress = 0
progreso = 0

bandera = 0

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-s) %(message)s')


class Hilo1(threading.Thread):
    def __init__(self, nombre_hilo, solicitudes, url, port, data):
        threading.Thread.__init__(self, name=nombre_hilo, target=Hilo1.crear, args=(self, solicitudes, url, port, ))



    def solicitar(self, url, port):

        global solicitudesok
        global solicitudeserror
        global total_progress

        tam_lines = len(lineas)
        num_random = random.randint(0,tam_lines-1)
        line = lineas[num_random]

        peticion = line.replace("\n","")
        peticion_final = peticion.replace(" ", "%20")
        peticion_hoysi = peticion_final.replace("#", "%23")
        connection = http.client.HTTPConnection(url, port)
        connection.request("GET", peticion_hoysi)
        response = connection.getresponse()
        print("Status: {} and reason: {}".format(response.status, response.reason))

        #cont = 0
        if int(response.status) == 200:
            solicitudesok = solicitudesok + 1
            total_progress = total_progress + 1
        else:
            solicitudeserror = solicitudeserror + 1
            total_progress = total_progress + 1

        #print(solicitudesok)
        connection.close()

    def crear(self, solicitudes, url, port):
        cont = int(solicitudes)
        url_modificate = url.replace("/","")
        print(url_modificate)
        print(port)
        for i in range(cont):
            logging.debug("Consultando para el id " + str(solicitudes))
            self.solicitar(url_modificate, port)

        #time.sleep(2)
        return


def progreso():
    global progreso
    global total_solicitudes
    global total_progress

    progress['maximum'] = 100
    cont = 0
    print(total_progress)
    print(total_solicitudes)

    while 1==1:

        #progreso = total_solicitudes-total_progress/total_solicitudes
        time.sleep(1)
        progress['value'] = cont
        progress.update()
        cont= cont + 1
        #print(progreso)

        print("aver pues :"+str(total_progress))

        if 100 == cont:
            progress['value'] = 0
            progress.update()
            break



window = Tk()

window.title("Traffic Simulator")

window.geometry('750x500')



etiqueta = Label(window, text="Ingresa los parametros y opciones para enviar el trafico")
etiqueta.grid(column=1, row=0)

lbl = Label(window, text="URL:      ")
lbl.grid(column=0, row=1)

txt = Entry(window, width=30)
txt.grid(column=1, row=1)


lblc = Label(window, text="Concurrencias:   ")
lblc.grid(column=0, row=2)

txtc = Entry(window, width=30)
txtc.grid(column=1, row=2)

lbls = Label(window, text="Solicitudes: ")
lbls.grid(column=0, row=3)

txts = Entry(window, width=30)
txts.grid(column=1, row=3)

lblt = Label(window, text="Timeout:   ")
lblt.grid(column=0, row=5)

lblt = Label(window, text="                        ")
lblt.grid(column=0, row=6)


combo = Combobox(window)
combo['values'] = ("tiempo...",1, 2, 3, 4, 5, 6)

combo.current(0)  # set the selected item

combo.grid(column=1, row=5)


lblt1 = Label(window, text="                        ")
lblt1.grid(column=0, row=9)

lblt2 = Label(window, text="                        ")
lblt2.grid(column=0, row=12)

txtarea = scrolledtext.ScrolledText(window, width=50, height=15)

txtarea.grid(column=1, row=13)


lblp = Label(window, text="Progreso...")
lblp.grid(column=0, row=11)

progress = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate')
progress.grid(column=1, row=11)






def ejecutar():



    global bandera
    global solicitudeserror
    global solicitudesok




    if bandera == 0:
        txtarea.insert(INSERT, "Por favor abra primero el archivo de parametros!!! \n\n")
    else:
        url = txt.get()
        urlsplit = url.split(":");
        print(urlsplit)


        urlfinal = urlsplit[1]
        port = urlsplit[2]


        print("url=     " + urlfinal)
        print("port=    " + port)

        solicitudes = txts.get()
        print("solicitues = " + solicitudes)
        total_solicitudes = solicitudes
        #solicitudesok = 0


        concurrencia = txtc.get()
        print("concurrencia = "+concurrencia)

        c = int(concurrencia)
        solicitud_hilo = int(solicitudes) / c

        my_objects = []

        hilop = threading.Thread(target=progreso)
        hilop.start()
        #hilop.join()

        for i in range(c):
            my_objects.append(Hilo1("hilo"+str(i), solicitud_hilo, urlfinal, port, ""))

        for obj in my_objects:
            obj.start()


        txtarea.insert(INSERT, "Total de solicitudes => "+ str(total_solicitudes)+"\n")
        txtarea.insert(INSERT, "Total de solicitudes OK => " + str(solicitudesok) + "\n")

        solicitudeserror = 0
        solicitudesok = 0






def leer():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    f = open(filename, "r")
    f1 = f.readlines()
    for x in f1:
        lineas.append(x)

    print(lineas)

    global bandera

    bandera = 1










btn = Button(window, text="Ejecutar", command=ejecutar)

btn.grid(column=1, row=8)


lblarchivo = Label(window, text="Parametros: ")
lblarchivo.grid(column=0, row=4)

archivo = Button(window, text="abrir", command=leer)
archivo.grid(column=1, row=4)





window.mainloop()










