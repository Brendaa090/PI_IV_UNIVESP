CREATE OR REPLACE VIEW temp_media_diaria AS
SELECT 
    data,
    ROUND(AVG(temperatura)::numeric, 2) AS temperatura_media
FROM iot_diario
GROUP BY data
ORDER BY data;
