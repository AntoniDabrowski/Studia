WITH query AS
    (SELECT kod_grupy, COUNT(DISTINCT wybor.kod_uz)
    FROM grupa JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN semestr USING (semestr_id)
        JOIN wybor USING (kod_grupy)
    WHERE nazwa = 'Semestr letni 2016/2017'
        AND rodzaj_zajec = 'w'
    GROUP BY kod_grupy)
SELECT AVG(count)
FROM query;