SELECT DISTINCT uzytkownik.kod_uz, uzytkownik.imie, uzytkownik.nazwisko
FROM uzytkownik JOIN grupa g1 USING (kod_uz)
    LEFT JOIN (SELECT kod_uz, imie, nazwisko
               FROM uzytkownik JOIN grupa USING (kod_uz)
               WHERE rodzaj_zajec='s') g2 ON g1.kod_uz = g2.kod_uz
WHERE g1.rodzaj_zajec = 'w'
    AND g2.kod_uz is NULL;