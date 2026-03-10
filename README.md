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
'''
## 💡 Valor Comercial y Casos de Uso
El procesamiento de telemetría en tiempo real no es solo un reto técnico, sino una ventaja competitiva. Esta arquitectura permite:
* **Mantenimiento Predictivo:** Monitoreo en vivo de la temperatura del CPU y niveles de batería para evitar fallas mecánicas en operación.
* **Prevención de Incidentes:** Alertas inmediatas mediante visión computarizada sobre obstáculos críticos (personas, fuego), minimizando riesgos físicos y daños al equipo.
* **Escalabilidad Operativa:** Capacidad de gestionar flotas de cientos de robots simultáneamente sin saturar los servidores, gracias al desacoplamiento de la ingesta y el procesamiento.

## 🛠️ Justificación de Servicios GCP
[cite_start]Para cumplir con los requerimientos de Cloud Computing y Ciencia de Datos [cite: 4][cite_start], se seleccionaron las siguientes herramientas administradas de GCP:
* **Cloud Functions:** Se utiliza como un endpoint serverless (`main.py`) altamente escalable para recibir los payloads HTTP de los robots, cobrando solo por milisegundo de ejecución.
* **Cloud Pub/Sub:** Actúa como el amortiguador (buffer) principal (`robots-stream`). Desacopla la ingesta rápida del procesamiento analítico, garantizando que no se pierdan paquetes (cero pérdida de datos) durante picos de tráfico extremo.
* **Cloud Dataflow (Apache Beam):** Permite el procesamiento continuo en modo *streaming* puro (`pipeline.py`). Transforma y limpia los datos en tiempo real antes de almacenarlos.
* **BigQuery:** Seleccionado como Data Warehouse (`robot_analytics.telemetria`) por su capacidad nativa de ingestar datos en streaming e integrarse nativamente con Looker Studio para visualización en vivo.

## 🚀 Desafíos Técnicos Resueltos
[cite_start]Durante el desarrollo, abordamos retos de alta dificultad técnica:
1. **Garantía de Entrega (Streaming):** En la Cloud Function (`main.py`), implementamos una espera síncrona (`future.result()`) sobre la publicación asíncrona de Pub/Sub. Esto garantiza que el frontend solo reciba un "HTTP 200 OK" si el mensaje fue persistido exitosamente en el bus de mensajes.
2. **Pruebas de Estrés y Alta Velocidad:** Para validar la arquitectura, no nos limitamos a la interfaz web. Se desarrolló un inyector gRPC (`robot_directo.py`) que publica ráfagas de alta velocidad de forma asíncrona, simulando el comportamiento de una flota robótica masiva bajo estrés.

## ⚙️ Guía de Ejecución Local

### 1. Requisitos Previos
* Cuenta activa en GCP y Google Cloud CLI autenticado (`gcloud auth application-default login`).
* Python 3.9+ instalado.

### 2. Instalación
[cite_start]Clona el repositorio e instala las dependencias necesarias[cite: 96]:
```bash
git clone [https://github.com/Sepu2002/ProyectoFinalGVD_mu_or_se.git](https://github.com/Sepu2002/ProyectoFinalGVD_mu_or_se.git)
cd ProyectoFinalGVD_mu_or_se
pip install -r requirements.txt
