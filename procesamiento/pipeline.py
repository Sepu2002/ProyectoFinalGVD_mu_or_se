import argparse
import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery

# Esquema de BigQuery para que Beam sepa cómo escribir
table_schema = 'robot_id:STRING, timestamp:STRING, bateria:FLOAT, temp_cpu:INTEGER, objeto:STRING, modo:STRING'

class ParseJson(beam.DoFn):
    """Convierte bytes de PubSub a diccionario Python"""
    def process(self, element):
        try:
            row = json.loads(element.decode('utf-8'))
            yield row
        except Exception:
            logging.error("Error parseando JSON")

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_subscription', required=True)
    parser.add_argument('--output_table', required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True # MODO STREAMING ACTIVADO

    with beam.Pipeline(options=pipeline_options) as p:
        
        # 1. Leer de Pub/Sub
        messages = (
            p 
            | "Leer PubSub" >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription)
            | "Parsear JSON" >> beam.ParDo(ParseJson())
        )

        # 2. Filtrar o Transformar (Opcional: aquí podrías filtrar solo peligros)
        # Por ahora pasamos todo para que veas datos en la demo.
        
        # 3. Escribir a BigQuery
        messages | "Escribir a BigQuery" >> WriteToBigQuery(
            known_args.output_table,
            schema=table_schema,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
        
        # (Opcional) Rama paralela: Escribir a Cloud Storage (Archivos texto)
        # messages | "Escribir a GCS" >> beam.io.WriteToText("gs://TU_BUCKET/output")

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
