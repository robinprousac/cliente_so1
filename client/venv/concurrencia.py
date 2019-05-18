import threading
import time
import logging
import http.client
#import cliente


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-s) %(message)s')


class Hilo1(threading.Thread):
    def __init__(self, nombre_hilo, solicitudes, url, port, data):
        threading.Thread.__init__(self, name=nombre_hilo, target=Hilo1.crear, args=(self, solicitudes, url, port, ))



    def solicitar(self, url, port):
        print("solicitando")
        #cad = "localhost"
        #puerto = 3000

        connection = http.client.HTTPConnection(url, port)
        connection.request("GET", line)
        response = connection.getresponse()
        print("Status: {} and reason: {}".format(response.status, response.reason))

        connection.close()

    def crear(self, solicitudes, url, port):
        cont = int(solicitudes)
        #print(cont)
        print(url)
        url_modificate = url.replace("/","")
        print(port)
        for i in range(cont):
            logging.debug("Consultando para el id " + str(solicitudes))
            self.solicitar(url_modificate, port)

        #time.sleep(2)
        return


