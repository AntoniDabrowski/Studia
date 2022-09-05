SELECT string_agg(DISTINCT nazwa,', ' ORDER BY nazwa)
FROM uzytkownik JOIN grupa USING (kod_uz)
    JOIN przedmiot_semestr USING (kod_przed_sem)
    JOIN przedmiot USING (kod_przed)
WHERE nazwisko = 'Rychlikowski';