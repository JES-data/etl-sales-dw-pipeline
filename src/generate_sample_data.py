import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_data(num_clientes: int = 15, num_ventas: int = 100, seed: int = 42):
    rng = random.Random(seed)

    segmentos = ["Minorista", "Mayorista", "Corporativo"]
    ciudades = ["CABA", "Rosario", "Cordoba", "Mendoza", "La Plata"]
    productos = [
        ("SKU-001", "Notebook Pro 14", "Electronica", 1200.00),
        ("SKU-002", "Monitor 27 IPS", "Electronica", 350.50),
        ("SKU-003", "Teclado Mecanico", "Accesorios", 95.00),
        ("SKU-004", "Mouse Inalambrico", "Accesorios", 45.00),
        ("SKU-005", "Silla Ergonomica", "Oficina", 420.00),
    ]

    clientes = []
    for i in range(1, num_clientes + 1):
        clientes.append({
            "cliente_id": f"CLI-{i:03d}",
            "nombre_cliente": f"Cliente {i:03d}",
            "segmento": rng.choice(segmentos),
            "ciudad": rng.choice(ciudades),
        })
    clientes_df = pd.DataFrame(clientes)
    clientes_df.to_csv(RAW_DIR / "clientes_raw.csv", index=False)

    fecha_base = datetime(2026, 1, 1)
    ventas = []
    for i in range(1, num_ventas + 1):
        cli_id = rng.choice(clientes_df["cliente_id"].tolist())
        sku, prod_nombre, categoria, precio = rng.choice(productos)
        fecha_str = (fecha_base + timedelta(days=rng.randint(0, 300))).strftime("%Y-%m-%d")
        cantidad = rng.randint(1, 10)
        precio_str = f"{precio:.2f}"
        venta_id = f"VTA-{i:04d}"

        # Inyectar ~10% de casos inválidos para probar rejected_rows.csv y motivo_rechazo
        anomalia = rng.random()
        if anomalia < 0.02:
            cantidad = 0
        elif anomalia < 0.04:
            cantidad = -2
        elif anomalia < 0.06:
            fecha_str = "fecha_rota"
        elif anomalia < 0.08:
            precio_str = ".00"
        elif anomalia < 0.10 and i > 2:
            venta_id = f"VTA-{i - 1:04d}"  # Duplicado intencional

        ventas.append({
            "venta_id": venta_id,
            "cliente_id": cli_id,
            "producto_sku": sku,
            "nombre_producto": prod_nombre,
            "categoria": categoria,
            "fecha": fecha_str,
            "cantidad": cantidad,
            "precio_unitario": precio_str,
        })

    pd.DataFrame(ventas).to_csv(RAW_DIR / "ventas_raw.csv", index=False)


if __name__ == "__main__":
    generate_data(num_clientes=15, num_ventas=100)