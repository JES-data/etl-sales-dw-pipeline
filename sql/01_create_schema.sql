IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SalesDW')
BEGIN
    CREATE DATABASE SalesDW;
END
GO

USE SalesDW;
GO

IF OBJECT_ID('dbo.Fact_Ventas', 'U') IS NOT NULL DROP TABLE dbo.Fact_Ventas;
IF OBJECT_ID('dbo.Dim_Cliente', 'U') IS NOT NULL DROP TABLE dbo.Dim_Cliente;
IF OBJECT_ID('dbo.Dim_Producto', 'U') IS NOT NULL DROP TABLE dbo.Dim_Producto;
IF OBJECT_ID('dbo.Dim_Fecha', 'U') IS NOT NULL DROP TABLE dbo.Dim_Fecha;
GO

CREATE TABLE dbo.Dim_Cliente (
    cliente_sk INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id VARCHAR(20) NOT NULL UNIQUE,
    nombre_cliente VARCHAR(120) NOT NULL,
    segmento VARCHAR(50) NOT NULL,
    ciudad VARCHAR(80) NOT NULL
);

CREATE TABLE dbo.Dim_Producto (
    producto_sk INT IDENTITY(1,1) PRIMARY KEY,
    producto_sku VARCHAR(30) NOT NULL UNIQUE,
    nombre_producto VARCHAR(120) NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL
);

CREATE TABLE dbo.Dim_Fecha (
    fecha_sk INT PRIMARY KEY, -- formato YYYYMMDD
    fecha DATE NOT NULL UNIQUE,
    anio SMALLINT NOT NULL,
    mes TINYINT NOT NULL,
    nombre_mes VARCHAR(20) NOT NULL,
    trimestre TINYINT NOT NULL
);

CREATE TABLE dbo.Fact_Ventas (
    venta_sk BIGINT IDENTITY(1,1) PRIMARY KEY,
    venta_id VARCHAR(30) NOT NULL UNIQUE,
    cliente_sk INT NOT NULL FOREIGN KEY REFERENCES dbo.Dim_Cliente(cliente_sk),
    producto_sk INT NOT NULL FOREIGN KEY REFERENCES dbo.Dim_Producto(producto_sk),
    fecha_sk INT NOT NULL FOREIGN KEY REFERENCES dbo.Dim_Fecha(fecha_sk),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL,
    total_venta DECIMAL(14,2) NOT NULL,
    fecha_carga DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
