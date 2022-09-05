SELECT array_to_string(ARRAY[nested.imie, nested.nazwisko], ' ')
FROM
    (SELECT imie, nazwisko, data
    FROM uzytkownik JOIN wybor USING (kod_uz)
        JOIN grupa USING (kod_grupy)
        JOIN przedmiot_semestr USING (kod_przed_sem)
        JOIN przedmiot USING (kod_przed)
        JOIN semestr USING (semestr_id)
    WHERE przedmiot.nazwa = 'Matematyka dyskretna (M)'
        AND semestr.nazwa = 'Semestr zimowy 2017/2018'
        AND rodzaj_zajec = 'w'
    ORDER BY data ASC LIMIT 1) as nested;