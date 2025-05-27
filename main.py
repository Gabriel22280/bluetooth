from machine import Pin, I2C, TouchPad
from time import sleep
from BLE import BLEUART
import bluetooth
import ssd1306
import _thread

# TouchPad
tp = TouchPad(Pin(4))

# Inicializa BLE UART
nombre = "ESP32BLUE"
ble = bluetooth.BLE()
ble.active(True)
miusart = BLEUART(ble, nombre)

# Pantalla OLED SSD1306
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Mensaje inicial
display.poweron()
display.fill(0)
display.text("ESP32 BLE activo", 0, 20, 1)
display.show()
sleep(2)
display.fill(0)
display.show()

# borrar mensajes recibidos desde python
mensaje_en_pantalla = False

def borrar_pantalla_luego():
    global mensaje_en_pantalla
    sleep(3)
    display.fill(0)
    display.show()
    mensaje_en_pantalla = False

# Función que se ejecuta cuando se recibe un mensaje desde la PC
def on_rx(data):
    global mensaje_en_pantalla
    mensaje = data.decode().strip()
    print("PC dijo:", mensaje)

    display.fill(0)
    display.text("PC:", 0, 10, 1)
    display.text(mensaje, 0, 20, 1)
    display.show()

    if not mensaje_en_pantalla:
        mensaje_en_pantalla = True
        _thread.start_new_thread(borrar_pantalla_luego, ())

    #miusart.write("ESP32 recibio: " + mensaje + "\r\n")
    
# Configuracion inicial
print("Ahora esta activo:", ble.active())
miusart.irq(on_rx)
print("ESP32 BLE UART activo")

# Función de enviar mensaje al tocar el TouchPad
def detectar_toque():
    while True:
        if tp.read() < 150:
            print("Toque detectado")
            miusart.write("ESP32: Se detecta un toque\n")
            sleep(0.5)

# Corre en un segundo núcleo
_thread.start_new_thread(detectar_toque, ())


# verificar direccion MAC (Solo para configuracion de pruebaBT.py)
'''
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

# Obtener la MAC (segunda parte de la tupla)
_, mac_bytes = ble.config('mac')

# Convertir a cadena hexadecimal con separadores
mac_str = ':'.join('%02X' % b for b in mac_bytes)

print("Dirección MAC Bluetooth:", mac_str)
'''