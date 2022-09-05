SELECT przedmiot.nazwa, COUNT(DISTINCT uzytkownik.kod_uz)
FROM przedmiot JOIN przedmiot_semestr USING (kod_przed)
    JOIN grupa USING (kod_przed_sem)
    JOIN wybor USING (kod_grupy)
    LEFT JOIN uzytkownik ON uzytkownik.kod_uz = wybor.kod_uz
WHERE rodzaj = 'k'
GROUP BY przedmiot.nazwa;