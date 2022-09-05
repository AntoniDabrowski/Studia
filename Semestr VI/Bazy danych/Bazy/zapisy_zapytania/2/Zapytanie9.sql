WITH bazy AS 
    (SELECT DISTINCT wybor.kod_uz
    FROM semestr JOIN przedmiot_semestr USING (semestr_id)
        JOIN przedmiot USING (kod_przed)
        JOIN grupa USING (kod_przed_sem)
        JOIN wybor USING (kod_grupy)
    WHERE semestr.nazwa = 'Semestr letni 2016/2017'
        AND przedmiot.nazwa = 'Bazy danych'
        AND rodzaj_zajec = 'w'),
sieci AS
    (SELECT DISTINCT wybor.kod_uz
    FROM semestr JOIN przedmiot_semestr USING (semestr_id)
        JOIN przedmiot USING (kod_przed)
        JOIN grupa USING (kod_przed_sem)
        JOIN wybor USING (kod_grupy)
    WHERE semestr.nazwa = 'Semestr letni 2016/2017'
        AND przedmiot.nazwa = 'Sieci komputerowe'
        AND rodzaj_zajec = 'w')
SELECT COUNT(*)
FROM (
(SELECT * 
FROM bazy LEFT JOIN sieci USING (kod_uz)
WHERE sieci.kod_uz is NULL)

UNION

(SELECT * 
FROM bazy RIGHT JOIN sieci USING (kod_uz)
WHERE bazy.kod_uz is NULL)) F;