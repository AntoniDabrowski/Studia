CREATE TABLE zapisy_16_17 AS
    SELECT data
    FROM wybor JOIN grupa USING (kod_grupy)
        JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN semestr USING (semestr_id)
    WHERE nazwa = 'Semestr zimowy 2016/2017';

SELECT to_char(MIN(data),'YYYY/MM/DD'),to_char(MAX(data),'YYYY/MM/DD')
FROM zapisy_16_17;

DROP TABLE zapisy_16_17;