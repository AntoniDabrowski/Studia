SELECT nazwa, COUNT (DISTINCT wybor.kod_uz)
FROM przedmiot JOIN przedmiot_semestr USING (kod_przed)
    JOIN grupa USING (kod_przed_sem)
    JOIN wybor USING (kod_grupy)
GROUP BY nazwa, rodzaj, rodzaj_zajec
HAVING rodzaj = 'p'
    AND rodzaj_zajec = 'w'
ORDER BY count DESC LIMIT 1;