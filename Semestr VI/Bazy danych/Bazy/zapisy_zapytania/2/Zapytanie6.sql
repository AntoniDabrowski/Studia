WITH query1 AS
    (SELECT semestr_id, MIN(data)
    FROM semestr JOIN przedmiot_semestr USING (semestr_id)
        JOIN grupa USING (kod_przed_sem)
        JOIN wybor USING (kod_grupy)
        JOIN uzytkownik ON wybor.kod_uz = uzytkownik.kod_uz
    WHERE semestr.nazwa LIKE 'Semestr letni%'
    GROUP BY semestr_id)
SELECT DISTINCT semestr_id, imie, nazwisko
FROM query1 JOIN wybor ON min = data
    JOIN uzytkownik USING (kod_uz)
ORDER BY 1,2,3;