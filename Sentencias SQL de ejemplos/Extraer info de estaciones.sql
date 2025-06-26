SELECT 
    STATIONS.ID,
    STATIONS.NAME,
    STATIONS.CITY,
    STATIONS.SHORT_NAME,
    json_extract(STATIONS.COORDINATES,'$.latitude') as LATITUD,
    json_extract(STATIONS.COORDINATES,'$.longitude') as LONGITUD
        
FROM STATIONS
