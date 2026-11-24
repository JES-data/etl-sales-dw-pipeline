# ETL Sales Data Warehouse Pipeline

![Data Engineering](https://img.shields.io/badge/Data%20Engineering-Project-blue)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-CC2927?logo=microsoftsqlserver&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Orchestration-2496ED?logo=docker&logoColor=white)
![ETL](https://img.shields.io/badge/ETL-Automation-success)
![Data Warehouse](https://img.shields.io/badge/Data%20Warehouse-Business%20Intelligence-orange)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white)

![Repo Size](https://img.shields.io/github/repo-size/JES-data/etl-sales-dw-pipeline)
![Last Commit](https://img.shields.io/github/last-commit/JES-data/etl-sales-dw-pipeline)

Proyecto de ingeniería de datos que implementa un pipeline ETL (Extract, Transform, Load) utilizando Python, Docker y SQL Server.

El sistema procesa datos comerciales, aplica reglas de limpieza y calidad, y carga la información en un entorno preparado para análisis y generación de indicadores. La solución se ejecuta íntegramente en contenedores Docker, permitiendo un despliegue reproducible y simplificando la configuración del entorno.

---

## Arquitectura

![ETL Sales Data Warehouse Pipeline Architecture](docs/images/architecture.png)
---

## Objetivo

Este proyecto simula un escenario de análisis comercial donde los datos de ventas requieren limpieza, transformación e integración antes de ser utilizados para reporting y análisis de negocio.

El objetivo es demostrar cómo automatizar un flujo de procesamiento de datos utilizando herramientas ampliamente utilizadas en proyectos de ingeniería de datos.


## Technology Stack

- Python & Pandas
- SQL Server
- Docker & Docker Compose
- Git & GitHub


## Funcionalidades

- Extracción de datos comerciales.
- Limpieza y validación de información.
- Transformación de datos para análisis.
- Carga automatizada en SQL Server.
- Ejecución mediante contenedores Docker.
- Base preparada para Data Warehousing y Business Intelligence.

---

## Resultados

Este proyecto demuestra la implementación práctica de:

- Procesos ETL.
- Ingeniería de Datos.
- Automatización con Python.
- Limpieza y calidad de datos.
- SQL Server.
- Docker y Docker Compose.
- Diseño de soluciones orientadas al análisis de información.

---

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/JES-data/etl-sales-dw-pipeline.git
```

### Acceder al proyecto

```bash
cd etl-sales-dw-pipeline
```

### Levantar el entorno

```bash
docker compose up --build
```

### Verificar contenedores

```bash
docker ps
```

---

## Casos de Uso

La arquitectura implementada puede adaptarse a escenarios como:

- Automatización de cargas de datos.
- Consolidación de información comercial.
- Procesamiento de ventas.
- Integración de fuentes de datos.
- Alimentación de Data Warehouses.
- Preparación de datos para Power BI.
- Soluciones de Business Intelligence para PyMEs.

---

## Sobre JES Data

**JES Data** desarrolla soluciones de ingeniería de datos, automatización de procesos ETL, análisis de datos y Business Intelligence para ayudar a organizaciones a transformar datos en información útil para la toma de decisiones.

---

## Autor

### Juan Eduardo Shifres

Founder @ JES Data

- LinkedIn: https://www.linkedin.com/in/juan-shifres/
- GitHub: https://github.com/JES-data
- Sitio Web: https://jesdata.com.ar

---

## Licencia

Proyecto publicado con fines educativos, demostrativos y de portfolio profesional.