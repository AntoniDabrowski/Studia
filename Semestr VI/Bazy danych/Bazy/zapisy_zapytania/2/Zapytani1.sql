(SELECT DISTINCT kod_uz, imie, nazwisko
FROM uzytkownik JOIN grupa USING (kod_uz)
WHERE rodzaj_zajec = 'w')
EXCEPT
(SELECT DISTINCT kod_uz, imie, nazwisko
FROM uzytkownik JOIN grupa USING (kod_uz)
WHERE rodzaj_zajec = 's');