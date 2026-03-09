import os
import json
import time
import random
from datetime import datetime
from google.cloud import pubsub_v1

# Configuración directa (Reemplaza con tu ID si es distinto)
PROJECT_ID = os.environ.get('PROJECT_ID', 'proyectofinal-mu-or-se')
TOPIC_ID = 'robots-stream'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

print(f"Conectado a Pub/Sub: {topic_path}")
print("Iniciando inyección de alta velocidad (10 msgs/segundo)...")

try:
    contador = 0
    while True:
        data = {
            "robot_id": f"R-PRO-{random.randint(10, 99)}",
            "timestamp": datetime.now().isoformat(),
            "bateria": round(random.uniform(20.0, 100.0), 1),
            "temp_cpu": random.randint(40, 90),
            "objeto": random.choice(["nada", "nada", "caja", "persona", "fuego"]),
            "modo": "streaming_directo"
        }
        
        # Publicación asíncrona directa (gRPC, no HTTP)
        data_str = json.dumps(data)
        publisher.publish(topic_path, data_str.encode("utf-8"))
        
        contador += 1
        if contador % 50 == 0:
            print(f"Enviados {contador} paquetes a velocidad luz...")
            
        time.sleep(0.1) # 10 mensajes por segundo
except KeyboardInterrupt:
    print("\nInyección detenida.")
