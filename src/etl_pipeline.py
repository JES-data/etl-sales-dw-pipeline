import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1434")
DB_NAME = os.getenv("DB_NAME", "SalesDW")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASS = os.getenv("MSSQL_SA_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
LOG_DIR = BASE_DIR / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_engine():
    connection_url = URL.create(
        "mssql+pyodbc",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )
    return create_engine(connection_url, fast_executemany=True)


def clean_price(val):
    if pd.isna(val):
        return None
    cleaned = str(val).replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_date_safe(val):
    if pd.isna(val):
        return pd.NaT
    parsed = pd.to_datetime(str(val).strip(), format="mixed", dayfirst=True, errors="coerce")
    return parsed


def run_etl():
    clientes_df = pd.read_csv(RAW_DIR / "clientes_raw.csv", dtype=str)
    ventas_df = pd.read_csv(RAW_DIR / "ventas_raw.csv", dtype=str)

    # 1. Limpieza de clientes y deduplicación
    clientes_df["cliente_id"] = clientes_df["cliente_id"].str.strip()
    clientes_df["nombre_cliente"] = clientes_df["nombre_cliente"].str.strip()
    clientes_df["segmento"] = clientes_df["segmento"].str.strip()
    clientes_df["ciudad"] = clientes_df["ciudad"].str.strip()
    clientes_clean = clientes_df.dropna(subset=["cliente_id", "nombre_cliente"]).drop_duplicates(
        subset=["cliente_id"], keep="first"
    ).copy()

    # 2. Limpieza y validación de ventas
    ventas_df["venta_id"] = ventas_df["venta_id"].str.strip()
    ventas_df["cliente_id"] = ventas_df["cliente_id"].str.strip()
    ventas_df["producto_sku"] = ventas_df["producto_sku"].str.strip()
    ventas_df["nombre_producto"] = ventas_df["nombre_producto"].str.strip()
    ventas_df["categoria"] = ventas_df["categoria"].str.strip()
    ventas_df["precio_num"] = ventas_df["precio_unitario"].apply(clean_price)
    ventas_df["cantidad_num"] = pd.to_numeric(ventas_df["cantidad"].str.strip(), errors="coerce")
    ventas_df["fecha_dt"] = ventas_df["fecha"].apply(parse_date_safe)

    ventas_dedup = ventas_df.drop_duplicates(subset=["venta_id"], keep="first").copy()

    valid_mask = (
        ventas_dedup["venta_id"].notna()
        & ventas_dedup["cliente_id"].isin(clientes_clean["cliente_id"])
        & ventas_dedup["producto_sku"].notna()
        & ventas_dedup["fecha_dt"].notna()
        & ventas_dedup["cantidad_num"].notna()
        & (ventas_dedup["cantidad_num"] > 0)
        & ventas_dedup["precio_num"].notna()
        & (ventas_dedup["precio_num"] > 0)
    )

    rejected_df = ventas_dedup[~valid_mask].copy()
    if not rejected_df.empty:
        rejected_df.drop(columns=["precio_num", "cantidad_num", "fecha_dt"], errors="ignore").to_csv(
            LOG_DIR / "rejected_rows.csv", index=False
        )

    valid_df = ventas_dedup[valid_mask].copy()
    valid_df["cantidad_int"] = valid_df["cantidad_num"].astype(int)
    valid_df["total_venta"] = (valid_df["cantidad_int"] * valid_df["precio_num"]).round(2)
    valid_df["fecha_sk"] = valid_df["fecha_dt"].dt.strftime("%Y%m%d").astype(int)

    engine = get_engine()

    with engine.begin() as conn:
        # Upsert Dim_Cliente
        for _, row in clientes_clean.iterrows():
            conn.execute(
                text("""
                    IF EXISTS (SELECT 1 FROM dbo.Dim_Cliente WHERE cliente_id = :cliente_id)
                        UPDATE dbo.Dim_Cliente
                        SET nombre_cliente = :nombre_cliente, segmento = :segmento, ciudad = :ciudad
                        WHERE cliente_id = :cliente_id
                    ELSE
                        INSERT INTO dbo.Dim_Cliente (cliente_id, nombre_cliente, segmento, ciudad)
                        VALUES (:cliente_id, :nombre_cliente, :segmento, :ciudad)
                """),
                {
                    "cliente_id": row["cliente_id"],
                    "nombre_cliente": row["nombre_cliente"],
                    "segmento": row["segmento"],
                    "ciudad": row["ciudad"],
                },
            )

        # Upsert Dim_Producto
        productos_clean = valid_df.drop_duplicates(subset=["producto_sku"], keep="first")
        for _, row in productos_clean.iterrows():
            conn.execute(
                text("""
                    IF EXISTS (SELECT 1 FROM dbo.Dim_Producto WHERE producto_sku = :producto_sku)
                        UPDATE dbo.Dim_Producto
                        SET nombre_producto = :nombre_producto, categoria = :categoria, precio_unitario = :precio_unitario
                        WHERE producto_sku = :producto_sku
                    ELSE
                        INSERT INTO dbo.Dim_Producto (producto_sku, nombre_producto, categoria, precio_unitario)
                        VALUES (:producto_sku, :nombre_producto, :categoria, :precio_unitario)
                """),
                {
                    "producto_sku": row["producto_sku"],
                    "nombre_producto": row["nombre_producto"],
                    "categoria": row["categoria"],
                    "precio_unitario": float(row["precio_num"]),
                },
            )

        # Upsert Dim_Fecha
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
        }
        fechas_clean = valid_df.drop_duplicates(subset=["fecha_sk"], keep="first")
        for _, row in fechas_clean.iterrows():
            dt = row["fecha_dt"]
            conn.execute(
                text("""
                    IF NOT EXISTS (SELECT 1 FROM dbo.Dim_Fecha WHERE fecha_sk = :fecha_sk)
                        INSERT INTO dbo.Dim_Fecha (fecha_sk, fecha, anio, mes, nombre_mes, trimestre)
                        VALUES (:fecha_sk, :fecha, :anio, :mes, :nombre_mes, :trimestre)
                """),
                {
                    "fecha_sk": int(row["fecha_sk"]),
                    "fecha": dt.date(),
                    "anio": int(dt.year),
                    "mes": int(dt.month),
                    "nombre_mes": meses[int(dt.month)],
                    "trimestre": int(dt.quarter),
                },
            )

        # Mapas de surrogate keys
        cli_map = dict(conn.execute(text("SELECT cliente_id, cliente_sk FROM dbo.Dim_Cliente")).fetchall())
        prd_map = dict(conn.execute(text("SELECT producto_sku, producto_sk FROM dbo.Dim_Producto")).fetchall())

        # Upsert Fact_Ventas
        for _, row in valid_df.iterrows():
            conn.execute(
                text("""
                    IF EXISTS (SELECT 1 FROM dbo.Fact_Ventas WHERE venta_id = :venta_id)
                        UPDATE dbo.Fact_Ventas
                        SET cliente_sk = :cliente_sk,
                            producto_sk = :producto_sk,
                            fecha_sk = :fecha_sk,
                            cantidad = :cantidad,
                            precio_unitario = :precio_unitario,
                            total_venta = :total_venta
                        WHERE venta_id = :venta_id
                    ELSE
                        INSERT INTO dbo.Fact_Ventas (
                            venta_id, cliente_sk, producto_sk, fecha_sk, cantidad, precio_unitario, total_venta
                        )
                        VALUES (
                            :venta_id, :cliente_sk, :producto_sk, :fecha_sk, :cantidad, :precio_unitario, :total_venta
                        )
                """),
                {
                    "venta_id": row["venta_id"],
                    "cliente_sk": cli_map[row["cliente_id"]],
                    "producto_sk": prd_map[row["producto_sku"]],
                    "fecha_sk": int(row["fecha_sk"]),
                    "cantidad": int(row["cantidad_int"]),
                    "precio_unitario": float(row["precio_num"]),
                    "total_venta": float(row["total_venta"]),
                },
            )

    print(f"ETL completado. Filas válidas cargadas: {len(valid_df)} | Filas rechazadas: {len(rejected_df)}")


if __name__ == "__main__":
    run_etl()
