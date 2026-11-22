# ETL Sales Data Warehouse Pipeline

Pipeline ETL en Python y SQL Server 2022 (Docker en el puerto 1434) para cargar ventas en el data warehouse SalesDW dentro de JES-data, con limpieza, deduplicacion, registro de rechazos en data/logs/ y carga en Fact_Ventas.

## Estructura
- src/generate_sample_data.py: genera datos de prueba en data/raw/ con casos borde.
- src/etl_pipeline.py: limpia, valida, registra rechazos y hace upsert en Fact_Ventas.
- .env.example y .gitignore: plantilla de variables y exclusion de .env y .venv.
- docker-compose.yml: servicio de SQL Server 2022 en el puerto 1434.
