import rp2
import network
import machine
import socket
import time
from picozero import Pot, LED
from time import sleep


ap = network.WLAN(network.AP_IF)
ap.config(essid="pico_wearables", password='inovlabs')
ap.active(True)

PowerLED = machine.Pin('LED', machine.Pin.OUT)
PowerLED.on()

led = LED(0) # pin onde está ligado o LED
led.on

def get_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(10)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()

        r = str(cl.recv(1024))
        request = r # Copia os dados recebidos no socket.
      
        valor = 8 # Valor inicial
        BuscaValor = request.find("quantity") # Encontra a localização da primeira ocorrência da palavra "quantity"
        if BuscaValor > 0:
            BuscaValor = request[BuscaValor + 9 : BuscaValor + 12] # 
#            print("BuscaValor:", BuscaValor)
            valor = int(BuscaValor)
            
            bpm = valor
            beat = 60/bpm
            print("beat = ", beat)    
            brighter_time = beat / 2 # Spend half a beat getting brighter
            dimmer_time = beat / 2 # Spend half a beat getting dimmer
            led.pulse(brighter_time, dimmer_time, wait=False) # Pulsa o led
       
        print("valor:", valor)
        

#        print(r)
        stateis = str(bpm) + " BPM"
        response = get_file("index.html") % stateis
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
#        print('Connection closed')
#        PowerLED.off()