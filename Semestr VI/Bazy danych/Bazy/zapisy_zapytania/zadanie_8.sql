CREATE TABLE temp1 AS
    SELECT DISTINCT uzytkownik.kod_uz, semestr_id
    FROM uzytkownik JOIN wybor USING (kod_uz)
        JOIN grupa USING (kod_grupy)
        JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN przedmiot USING (kod_przed)
    WHERE nazwa = 'Algorytmy i struktury danych (M)';

CREATE TABLE temp2 AS
    SELECT kod_uz, COUNT(semestr_id)
    FROM temp1
    GROUP BY kod_uz;

SELECT COUNT(kod_uz)
FROM temp2
WHERE temp2.count = 2;

DROP TABLE temp1;
DROP TABLE temp2;