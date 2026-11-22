from pathlib import Path
import pandas as pd

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

clientes = pd.DataFrame([
    {"cliente_id": "CLI-001", "nombre_cliente": "  Distribuidora Sur SA ", "segmento": "Mayorista", "ciudad": "Buenos Aires"},
    {"cliente_id": "CLI-002", "nombre_cliente": "Comercial Norte", "segmento": "Minorista", "ciudad": "Córdoba"},
    {"cliente_id": "CLI-003", "nombre_cliente": "TecnoAndes SRL", "segmento": "Corporativo", "ciudad": "Mendoza"},
    {"cliente_id": "CLI-004", "nombre_cliente": "  Mercado del Plata  ", "segmento": "Minorista", "ciudad": "La Plata"},
    {"cliente_id": "CLI-002", "nombre_cliente": "Comercial Norte", "segmento": "Minorista", "ciudad": "Córdoba"},
])

ventas = pd.DataFrame([
    # Casos válidos (distintos formatos y precios)
    {"venta_id": "VTA-1001", "cliente_id": "CLI-001", "producto_sku": "PRD-A1", "nombre_producto": "Notebook Pro 14", "categoria": "Tecnología", "fecha": "2026-10-05", "cantidad": "2", "precio_unitario": ".00"},
    {"venta_id": "VTA-1002", "cliente_id": "CLI-002", "producto_sku": "PRD-B2", "nombre_producto": "Monitor 24 IPS", "categoria": "Tecnología", "fecha": "12/10/2026", "cantidad": "3", "precio_unitario": "310.50"},
    {"venta_id": "VTA-1005", "cliente_id": "CLI-004", "producto_sku": "PRD-D4", "nombre_producto": "Teclado Mecánico", "categoria": "Accesorios", "fecha": "2026-11-02", "cantidad": "5", "precio_unitario": ",200.50"},
    {"venta_id": "VTA-1006", "cliente_id": "CLI-003", "producto_sku": "PRD-A1", "nombre_producto": "Notebook Pro 14", "categoria": "Tecnología", "fecha": "15/11/2026", "cantidad": "1", "precio_unitario": "1250.00"},
    # Duplicado exacto de VTA-1001
    {"venta_id": "VTA-1001", "cliente_id": "CLI-001", "producto_sku": "PRD-A1", "nombre_producto": "Notebook Pro 14", "categoria": "Tecnología", "fecha": "2026-10-05", "cantidad": "2", "precio_unitario": ".00"},
    # Casos inválidos (deben ir a rejected_rows.csv)
    {"venta_id": "VTA-1003", "cliente_id": "CLI-003", "producto_sku": "PRD-C3", "nombre_producto": "Silla Ergonómica", "categoria": "Oficina", "fecha": "2026-10-18", "cantidad": "-1", "precio_unitario": "420.00"},
    {"venta_id": "VTA-1004", "cliente_id": "CLI-001", "producto_sku": "PRD-A1", "nombre_producto": "Notebook Pro 14", "categoria": "Tecnología", "fecha": "fecha_rota", "cantidad": "1", "precio_unitario": "1250.00"},
    {"venta_id": "VTA-1007", "cliente_id": "CLI-999", "producto_sku": "PRD-B2", "nombre_producto": "Monitor 24 IPS", "categoria": "Tecnología", "fecha": "2026-11-10", "cantidad": "2", "precio_unitario": "310.50"},
    {"venta_id": "VTA-1008", "cliente_id": "CLI-002", "producto_sku": "PRD-E5", "nombre_producto": "Mouse Inalámbrico", "categoria": "Accesorios", "fecha": "2026-11-12", "cantidad": "0", "precio_unitario": "45.00"},
])

clientes.to_csv(raw_dir / "clientes_raw.csv", index=False)
ventas.to_csv(raw_dir / "ventas_raw.csv", index=False)
print("Set ampliado de CSVs generado en data/raw/")
