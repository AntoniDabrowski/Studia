SELECT nested.semestr_id
FROM 
    (SELECT semestr_id, COUNT(rodzaj)
    FROM przedmiot JOIN przedmiot_semestr USING (kod_przed)
    WHERE rodzaj='o'
    GROUP BY semestr_id
    ORDER BY count LIMIT 1) as nested;