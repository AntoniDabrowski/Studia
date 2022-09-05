WITH query1 AS
    (SELECT uzytkownik.kod_uz, imie, nazwisko, przedmiot.nazwa, MIN(semestr_id), MAX(semestr_id)
    FROM uzytkownik JOIN wybor USING (kod_uz)
        JOIN grupa USING (kod_grupy)
        JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN przedmiot USING (kod_przed)
        JOIN semestr USING (semestr_id)
    GROUP BY uzytkownik.kod_uz, imie, nazwisko, przedmiot.nazwa
    HAVING przedmiot.nazwa LIKE 'Algorytmy i struktury danych%'
        OR przedmiot.nazwa LIKE 'Matematyka dyskretna%')
SELECT DISTINCT q1.kod_uz, q1.imie, q1.nazwisko
FROM query1 q1 JOIN query1 q2 ON q1.kod_uz = q2.kod_uz
WHERE q1.nazwa LIKE 'Algorytmy i struktury danych%'
    AND q2.nazwa LIKE 'Matematyka dyskretna%' 
    AND q1.min < q2.max;
