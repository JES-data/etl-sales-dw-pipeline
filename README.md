ETL Sales Data Warehouse Pipeline (`SalesDW`)
================

- [Propuesta de valor (enfoque de
  consultoría)](#propuesta-de-valor-enfoque-de-consultoría)
- [Stack y estructura del proyecto](#stack-y-estructura-del-proyecto)
- [Puesta en marcha y ejecución](#puesta-en-marcha-y-ejecución)

## Propuesta de valor (enfoque de consultoría)

Este proyecto muestra cómo convertir datos operativos de ventas en un
modelo dimensional confiable (**`SalesDW`**) sobre **SQL Server 2022**
en Docker (puerto `1434`).

- **Calidad y confiabilidad:** limpieza, deduplicación, mapeo de claves
  carga hacia `Fact_Ventas`.
- **Trazabilidad:** registros rechazados aislados en `data/logs/` para
  auditar fallos de origen sin detener el proceso.
- **Reproducibilidad:** entorno contenerizado en Docker y variables
  sensibles protegidas en `.env` (excluidas de Git con `.gitignore`).

## Stack y estructura del proyecto

| Componente | Rol en el pipeline |
|:---|:---|
| SQL Server 2022 (Docker / WSL 2, puerto `1434`) | Motor del Data Warehouse `SalesDW` |
| `src/generate_sample_data.py` | Generación de datos de prueba en `data/raw/` |
| `src/etl_pipeline.py` | Limpieza, validaciones, logs en `data/logs/` y carga a `SalesDW` |
| `.env` y `.venv` | Credenciales y entorno Python local (ignorados en Git) |

## Puesta en marcha y ejecución

1.  Configurar `.env` a partir de `.env.example` con la contraseña `SA`,
    host `localhost`, puerto `1434`, usuario `sa` y base `SalesDW`.
2.  Activar el entorno virtual `.venv` e instalar dependencias de
    `requirements.txt`.
3.  Levantar SQL Server con `docker compose up -d`.
4.  Ejecutar `python src/generate_sample_data.py` y luego
    `python src/etl_pipeline.py`.
