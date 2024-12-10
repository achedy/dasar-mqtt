import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import paho.mqtt.client as mqtt
import time

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = 'app-20241210-led'

def on_disconnect(client, userdata, rc):
    print("Koneksi ke broker terputus. Mencoba menyambung kembali...")
    while True:
        try:
            client.reconnect()
            print("Berhasil menyambung kembali!")
            break
        except Exception as e:
            print(f"Gagal menyambung kembali: {e}")
            time.sleep(5)  # Tunggu sebelum mencoba lagi

def publish_message():
    client = mqtt.Client()

    # Menambahkan callback untuk menangani diskoneksi
    client.on_disconnect = on_disconnect

    try:
        # Menghubungkan ke broker
        client.connect(BROKER, PORT, 60)
        client.loop_start()

        while True:
            # Meminta input pesan dari pengguna
            message = input("Kirim pesan (1 untuk nyalakan LED, 0 untuk matikan LED): ")
            if message not in ['0', '1']:
                print("Hanya boleh mengirim '1' atau '0'")
                continue

            # Mengirim pesan ke topik
            client.publish(TOPIC, message)
            print(f"Pesan '{message}' dikirim ke topik '{TOPIC}'")
            time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        print("\nProgram dihentikan.")
        
   
if __name__ == '__main__':
    publish_message()
