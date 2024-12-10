import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import paho.mqtt.client as mqtt
import time

# Konfigurasi broker MQTT
BROKER = '192.168.1.20'
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = 'app-20241210-led'

# Callback ketika berhasil terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Terhubung ke broker")
        client.subscribe(TOPIC)  # Berlangganan topic
    else:
        print(f"Gagal terhubung ke broker. Kode: {rc}")

# Callback ketika pesan diterima
def on_message(client, userdata, msg):
    print(f"Pesan diterima di topic '{msg.topic}': {msg.payload.decode()}")

# Callback ketika koneksi terputus
def on_disconnect(client, userdata, rc):
    print("Koneksi terputus. Mencoba menyambung kembali...")
    while True:
        try:
            client.reconnect()
            print("Berhasil menyambung kembali!")
            break
        except Exception as e:
            print(f"Gagal menyambung kembali: {e}")
            time.sleep(5)  # Tunggu sebelum mencoba lagi

def subscribe_to_topic():
    # Membuat client MQTT
    client = mqtt.Client()    
    
    try:
        # Mengatur callback
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # Menghubungkan ke broker
        try:
            client.connect(BROKER, PORT, 60)
        except Exception as e:
            print(f"Gagal menghubungkan ke broker: {e}")
            return

        # Menjaga client tetap berjalan untuk menerima pesan
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
   

if __name__ == "__main__":
    subscribe_to_topic()
