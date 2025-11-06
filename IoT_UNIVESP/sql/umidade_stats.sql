CREATE OR REPLACE VIEW umidade_stats AS
SELECT 
    data,
    MAX(umidade) AS hum_max,
    MIN(umidade) AS hum_min
FROM 
    clima_br
GROUP BY 
    data
ORDER BY 
    data;
