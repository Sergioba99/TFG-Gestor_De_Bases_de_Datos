SELECT 
    *
FROM 
    SERVICE
    
WHERE SERVICE.ID IN (
SELECT 
    AUX_SERVICE.SERVICE_ID
FROM
    AUX_SERVICE
WHERE 
    AUX_SERVICE.TEST_ID = (SELECT TESTS.ID 
                           FROM TESTS
                           WHERE TESTS.NAME = 'supply_03216_60000_2025-06-02_2025-06-16'))