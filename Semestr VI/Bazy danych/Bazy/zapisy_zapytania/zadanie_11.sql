SELECT semestr_id, COUNT(kod_przed)
FROM przedmiot_semestr JOIN przedmiot USING (kod_przed)
WHERE rodzaj='o'
GROUP BY semestr_id
ORDER BY count LIMIT 1;