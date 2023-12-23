import dht
import machine
from machine import Pin, Timer
from umqtt.robust import MQTTClient
import network
import time

# Configurações do Wi-Fi
SSID = "CHACON_2G"
PASSWORD = "33245566"

# Configurações MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "sensor/dht11"

# Configurações do pino do sensor DHT11
DHT_PIN = 4  

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Conectando ao Wi-Fi...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
        print("Conectado ao Wi-Fi")

def connect_mqtt():
    client = MQTTClient("micro_dht11", MQTT_BROKER)
    while True:
        try:
            client.connect()
            print("Conectado ao broker MQTT")
            return client
        except OSError as e:
            print("Erro de conexão MQTT. Tentando novamente em 10 segundos...")
            time.sleep(10)
            machine.reset()

def read_dht11():
    dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

def publish_mqtt(client, temperature, humidity):
    payload = "Temperatura: {}°C, Umidade: {}%".format(temperature, humidity)
    client.publish(MQTT_TOPIC, payload)
    print("Publicado no tópico MQTT:", payload)

def main():
    connect_wifi()

    while True:
        try:
            mqtt_client = connect_mqtt()
            temperature, humidity = read_dht11()
            publish_mqtt(mqtt_client, temperature, humidity)
            time.sleep(10)  # Aguarda 10 segundos antes de ler novamente
        except Exception as e:
            print("Erro:", str(e))
            time.sleep(10)  # Aguarda 10 segundos antes de tentar novamente

if __name__ == "__main__":
    main()
