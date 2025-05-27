import asyncio
import threading
from bleak import BleakClient, BleakScanner
import tkinter as tk

ESP32_ADDRESS = "D4:8A:FC:C7:AD:A2"

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

client = None

def handle_rx(_, data):
    global texto
    print(f"[ESP32 ➡️ PC] {data.decode().strip()}")
    texto.config(text=data.decode().strip())

async def connect_ble():
    global client
    client = BleakClient(ESP32_ADDRESS)
    await client.connect()
    if client.is_connected:
        print("✅ Conectado al ESP32 BLE")
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
    else:
        print("❌ No se pudo conectar")

async def send_message():
    if client and client.is_connected:
        await client.write_gatt_char(UART_RX_CHAR_UUID, b"Mensaje Python\n")
        print("[PC ➡️ ESP32] Mensaje enviado")

def on_button_click():
    asyncio.run_coroutine_threadsafe(send_message(), loop)

def start_ble_loop():
    asyncio.run_coroutine_threadsafe(connect_ble(), loop)

async def escanear():
    dispositivos = await BleakScanner.discover()
    for d in dispositivos:
        print(d.name, d.address)

asyncio.run(escanear())

# Crear ventana
ventana = tk.Tk()
ventana.title("BLE UART PC <-> ESP32")
ventana.geometry("400x200")

# Botón para enviar datos
boton = tk.Button(ventana, text="Enviar a ESP32", command=on_button_click)
boton.pack(pady=20)

texto = tk.Label(ventana, text=" ")
texto.pack(pady=20)

# Lanzar el event loop de asyncio en segundo plano
loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()

# Conectar automáticamente al iniciar
start_ble_loop()

# Ejecutar la GUI
ventana.mainloop()