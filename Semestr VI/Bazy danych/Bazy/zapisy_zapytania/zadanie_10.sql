SELECT COUNT(kod_grupy)
FROM grupa JOIN przedmiot_semestr USING (kod_przed_sem)
    JOIN semestr USING (semestr_id)
    JOIN przedmiot USING (kod_przed)
WHERE semestr.nazwa = 'Semestr zimowy 2017/2018'
    AND rodzaj_zajec in ('c','C')
    AND przedmiot.nazwa = 'Logika dla informatyków';