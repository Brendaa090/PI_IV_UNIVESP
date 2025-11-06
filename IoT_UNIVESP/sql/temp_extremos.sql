CREATE OR REPLACE VIEW temp_extremos AS
SELECT 
    data,
    MAX(temperatura) AS temp_max,
    MIN(temperatura) AS temp_min
FROM 
    clima_br
GROUP BY 
    data
ORDER BY 
    data;
