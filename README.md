# 🚀 Pipeline de Analítica de Alta Velocidad (Streaming) en GCP

Este repositorio contiene el código fuente y la configuración de una arquitectura de Big Data en tiempo real construida sobre Google Cloud Platform (GCP). El sistema simula, ingesta, procesa y visualiza telemetría robótica con latencia de sub-segundos.

## 🏗 Arquitectura del Proyecto

El flujo de datos está diseñado para garantizar alta disponibilidad y procesamiento en *streaming* sin pérdida de paquetes:

1. **Generación de Datos:** Interfaz Web (`index.html`) para pruebas interactivas y Script gRPC (`robot_directo.py`) para pruebas de estrés masivo.
2. **Ingesta Serverless:** Cloud Functions (`main.py`) que recibe los payloads HTTP y los transfiere asíncronamente.
3. **Buzón de Mensajería:** Google Cloud Pub/Sub actúa como *buffer* (desacoplando la ingesta del procesamiento).
4. **Procesamiento Streaming:** Apache Beam ejecutado en Cloud Dataflow (`pipeline.py`) transforma y limpia los datos en ventanas de tiempo real.
5. **Data Warehouse & BI:** BigQuery almacena la telemetría procesada para ser consumida en vivo por un Dashboard en Looker Studio.



## 📂 Estructura del Repositorio

El proyecto cumple con las mejores prácticas de configuración e implementa archivos modulares:

```text
/
├── .env                    # (Ignorado en git) Variables de entorno locales y secretos
├── .gitignore              # Archivos excluidos del control de versiones
├── config.yaml             # Configuración global de la infraestructura GCP
├── requirements.txt        # Dependencias de Python necesarias
├── README.md               # Documentación principal
│
├── /frontend               
│   └── index.html          # Interfaz de usuario para simular telemetría visualmente
│
├── /ingesta                
│   ├── main.py             # Google Cloud Function (Receptor HTTP -> Pub/Sub)
│   └── robot_directo.py    # Inyector masivo vía gRPC para simular carga extrema
│
└── /procesamiento          
    └── pipeline.py         # Job de Apache Beam (Dataflow) para transformación en streaming