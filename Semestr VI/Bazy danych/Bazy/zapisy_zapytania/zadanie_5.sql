SELECT COUNT (DISTINCT kod_uz)
FROM grupa JOIN przedmiot_semestr USING (kod_przed_sem)
    JOIN semestr USING (semestr_id)
    JOIN przedmiot USING (kod_przed)
WHERE rodzaj_zajec in ('c','C')
    AND rodzaj = 'o'
    AND semestr.nazwa LIKE '%zimowy%';