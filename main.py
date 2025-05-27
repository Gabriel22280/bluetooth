from machine import Pin, I2C
from time import sleep
from BLE import BLEUART
import bluetooth
import ssd1306

# Inicializa BLE UART
nombre = "ESP32BLUE"
ble = bluetooth.BLE()
ble.active(True)
miusart = BLEUART(ble, nombre)

# Inicializa OLED SSD1306 (por I2C en pines GPIO 21 y 22)
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


# Función que se ejecuta cuando se recibe un mensaje desde la PC
def on_rx(data):
    mensaje = data.decode().strip()
    print("PC dijo:", mensaje)

    display.fill(0)
    display.text("PC:", 0, 0, 1)
    display.text(mensaje, 0, 16, 1)
    display.show()
    
    miusart.write("ESP32 recibio: " + mensaje + "\r\n")
    sleep(3)
    display.fill(0)
    display.show()

print("Ahora está activo:", ble.active())
# Registrar la función al IRQ de BLEUART
miusart.irq(on_rx)

print("ESP32 BLE UART activo")


# verificar direccion MAC
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