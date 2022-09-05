WITH query AS
    (SELECT semestr_id, kod_przed_sem, kod_uz, imie, nazwisko
    FROM semestr JOIN przedmiot_semestr USING (semestr_id)
        JOIN grupa USING (kod_przed_sem)
        JOIN uzytkownik USING (kod_uz)
    WHERE rodzaj_zajec = 'w')

SELECT DISTINCT imie, nazwisko
FROM semestr JOIN przedmiot_semestr USING (semestr_id)
    JOIN grupa USING (kod_przed_sem)
    JOIN query USING (semestr_id, kod_przed_sem, kod_uz)
GROUP BY semestr_id, kod_uz, imie, nazwisko, kod_przed_sem
HAVING COUNT(rodzaj_zajec) >= 3
ORDER BY 1,2;
