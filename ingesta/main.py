import json
import os
from google.cloud import pubsub_v1
import functions_framework

PROJECT_ID = os.environ.get('PROJECT_ID')
TOPIC_ID = os.environ.get('TOPIC_ID')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@functions_framework.http
def recibir_telemetria(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    try:
        request_json = request.get_json(silent=True)
        if request_json:
            data_str = json.dumps(request_json)
            future = publisher.publish(topic_path, data_str.encode("utf-8"))

            # ESTA ES LA LÍNEA MÁGICA: Obliga a la función a esperar a que Pub/Sub confirme
            future.result() 

            return ('OK', 200, headers)
        return ('Bad JSON', 400, headers)
    except Exception as e:
        print(f"Error grave: {e}")
        return (f'Error: {e}', 500, headers)
