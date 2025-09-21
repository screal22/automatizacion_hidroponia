import paho.mqtt.client as mqtt
from datetime import datetime
from app.extensions import db
from app.models import EstadoBomba

# Configuración de HiveMQ (broker público o tu instancia)
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "hidroponia/bomba/estado"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    msg_decodificado = msg.payload.decode("utf-8").split('/')
    print(f"Mensaje recibido en {msg.topic}: {msg_decodificado}")

    # Partimos el mensaje en estado y tiempo_llenado
    estado = msg_decodificado[0]
    tiempo_llenado = msg_decodificado[1]

    nuevo_registro = EstadoBomba(
        estado=estado,
        tiempo_llenado=tiempo_llenado
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    print(f"Estado {estado} guardado en la base de datos.")

def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client
