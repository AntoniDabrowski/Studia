CREATE TABLE tbl AS
    SELECT data
    FROM uzytkownik JOIN wybor USING (kod_uz)
        JOIN grupa USING (kod_grupy)
        JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN przedmiot USING (kod_przed)
        JOIN semestr USING (semestr_id)
    WHERE przedmiot.nazwa = 'Matematyka dyskretna (M)'
        AND semestr.nazwa = 'Semestr zimowy 2017/2018'
        AND rodzaj_zajec = 'w';

SELECT date_trunc('days',MAX(data)-MIN(data) + interval '1 day')
FROM tbl;    

DROP TABLE "tbl";