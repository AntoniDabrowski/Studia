SELECT COUNT(DISTINCT nazwa) 
FROM grupa JOIN przedmiot_semestr USING (kod_przed_sem)
    JOIN przedmiot USING (kod_przed)
WHERE rodzaj_zajec='e'
    AND rodzaj = 'o';