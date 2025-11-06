-- DROP das views antigas, se existirem
DROP VIEW IF EXISTS temp_media_diaria;
DROP VIEW IF EXISTS temp_extremos;
DROP VIEW IF EXISTS umidade_stats;
DROP VIEW IF EXISTS vento_stats;
DROP VIEW IF EXISTS precipitacao_diaria;

-- 1️⃣ Temperatura Média Diária
CREATE OR REPLACE VIEW temp_media_diaria AS
SELECT
    DATE(timestamp) AS data,
    AVG(temperature_avg) AS temp_media
FROM weather_readings
WHERE temperature_avg IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);

-- 2️⃣ Extremos de Temperatura
CREATE OR REPLACE VIEW temp_extremos AS
SELECT
    DATE(timestamp) AS data,
    MAX(temperature_max) AS temp_max,
    MIN(temperature_min) AS temp_min
FROM weather_readings
WHERE temperature_max IS NOT NULL AND temperature_min IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);

-- 3️⃣ Umidade Máxima e Mínima
CREATE OR REPLACE VIEW umidade_stats AS
SELECT
    DATE(timestamp) AS data,
    MAX(humidity_max) AS hum_max,
    MIN(humidity_min) AS hum_min
FROM weather_readings
WHERE humidity_max IS NOT NULL AND humidity_min IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);

-- 4️⃣ Estatísticas de Vento
CREATE OR REPLACE VIEW vento_stats AS
SELECT
    DATE(timestamp) AS data,
    MAX(wind_max) AS vento_max,
    AVG(wind_avg) AS vento_medio
FROM weather_readings
WHERE wind_max IS NOT NULL AND wind_avg IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);

-- 5️⃣ Precipitação Diária
CREATE OR REPLACE VIEW precipitacao_diaria AS
SELECT
    DATE(timestamp) AS data,
    MAX(rain_max) AS rain_max
FROM weather_readings
WHERE rain_max IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);
