CREATE OR REPLACE VIEW precipitacao_diaria AS
SELECT 
    data,
    ROUND(MAX(COALESCE(chuva, 0))::numeric, 2) AS rain_max
FROM iot_diario
GROUP BY data
ORDER BY data;
