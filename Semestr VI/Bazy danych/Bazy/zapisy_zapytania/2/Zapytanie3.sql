SELECT DISTINCT u1.kod_uz, u1.imie, u1.nazwisko
FROM grupa g JOIN uzytkownik u1 ON g.kod_uz = u1.kod_uz
    JOIN wybor ON g.kod_grupy = wybor.kod_grupy
GROUP BY g.kod_grupy, u1.kod_uz, u1.imie, u1.nazwisko
HAVING COUNT(DISTINCT wybor.kod_uz) > max_osoby
ORDER BY u1.kod_uz;