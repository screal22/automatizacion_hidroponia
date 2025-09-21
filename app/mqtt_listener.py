import paho.mqtt.client as mqtt
from app.extensions import db
from app.models import EstadoBomba
from dotenv import load_dotenv
import os

# Carga de variables de entorno
load_dotenv()

# Configuración de MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "test.mosquitto.org")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", 'hidroponia/valvula/estado')
print('Configuración MQTT:', MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)

def start_mqtt_listener(app):
    app.logger.info(f'Configuración MQTT: {MQTT_BROKER}, {MQTT_PORT}, {MQTT_TOPIC}')

    def on_connect(client, userdata, flags, rc):
        print("Conectado al broker MQTT con código:", rc)
        client.subscribe(MQTT_TOPIC)

    def on_message(client, userdata, msg):
        msg_decodificado = msg.payload.decode("utf-8").split('/')
        print(f"Mensaje recibido en {msg.topic}: {msg_decodificado}")
        app.logger.info(f"Mensaje recibido en {msg.topic}: {msg_decodificado}")

        # Partimos el mensaje en estado y tiempo_llenado
        estado = msg_decodificado[0]
        tiempo_llenado = msg_decodificado[1]

        nuevo_registro = EstadoBomba(
            estado=estado,
            tiempo_llenado=tiempo_llenado
        )
        with app.app_context():
            db.session.add(nuevo_registro)
            db.session.commit()

        print(f"Estado {estado} guardado en la base de datos")
        app.logger.info(f"Estado {estado} guardado en la base de datos")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client
