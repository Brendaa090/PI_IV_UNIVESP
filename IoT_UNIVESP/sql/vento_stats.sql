CREATE OR REPLACE VIEW vento_stats AS
SELECT 
    data,
    MAX(velocidade_vento) AS vento_max,
    ROUND(AVG(velocidade_vento), 2) AS vento_medio
FROM 
    clima_br
GROUP BY 
    data
ORDER BY 
    data;
