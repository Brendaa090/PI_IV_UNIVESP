CREATE TABLE IF NOT EXISTS iot_diario (
    data DATE NOT NULL,
    hora TIME NOT NULL,
    temperatura REAL,
    umidade REAL,
    chuva REAL
);
