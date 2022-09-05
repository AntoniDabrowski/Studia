-- BEGIN TRANSACTION;

-- CREATE TABLE firma (
--     kod_firmy SERIAL PRIMARY KEY,
--     nazwa TEXT NOT NULL,
--     adres TEXT NOT NULL,
--     kontakt TEXT NOT NULL
-- );

-- INSERT INTO firma (nazwa,adres,kontakt) VALUES 
-- ('SNS', 'Wrocław', 'H.Kloss'),
-- ('BIT', 'Kraków', 'R.Bruner'),
-- ('MIT', 'Berlin', 'J.Kos');

-- CREATE TABLE oferta_praktyki (
--     kod_oferty SERIAL PRIMARY KEY,
--     kod_firmy INT NOT NULL REFERENCES firma(kod_firmy),
--     semestr_id INT REFERENCES semestr(semestr_id),
--     liczba_miejsc INT
-- );

-- INSERT INTO oferta_praktyki (kod_firmy, semestr_id, liczba_miejsc)
-- SELECT kod_firmy, semestr_id, 3
-- FROM firma, semestr
-- WHERE firma.nazwa='SNS'
--     AND semestr.nazwa = 'Semestr letni 2017/2018';

-- INSERT INTO oferta_praktyki (kod_firmy, semestr_id, liczba_miejsc)
-- SELECT kod_firmy, semestr_id, 2
-- FROM firma, semestr
-- WHERE firma.nazwa='MIT'
--     AND semestr.nazwa = 'Semestr letni 2017/2018';

-- CREATE TABLE praktyki (
--     student INT,
--     opiekun INT REFERENCES  klucz obcy do tabeli pracownik,
--     oferta - kod oferty i klucz obcy do tabeli oferta_praktyki.
-- );

-- CREATE TABLE praktyki
-- (student int NOT NULL REFERENCES uzytkownik(kod_uz),
-- opiekun int REFERENCES uzytkownik(kod_uz),
-- oferta int NOT NULL REFERENCES oferta_praktyki(kod_oferty));

-- CREATE TABLE virtual_table (
--     v_id SERIAL PRIMARY KEY,
--     v1 INT NOT NULL,
--     v2 INT REFERENCES semestr(semestr_id)
-- );

-- ALTER TABLE virtual_table
--     ADD CONSTRAINT fk_uzytkownik_kod_uz
--     FOREIGN KEY (v1) REFERENCES uzytkownik(kod_uz);

BEGIN TRANSACTION;

INSERT INTO praktyki(student,oferta)
SELECT kod_uz,kod_oferty
FROM uzytkownik s,oferta_praktyki o
WHERE kod_uz =
 (SELECT MAX(kod_uz) FROM uzytkownik WHERE
  semestr BETWEEN 6 AND 10 AND kod_uz NOT IN
  (SELECT student FROM praktyki))
 AND
 kod_oferty =
 (SELECT MAX(kod_oferty) FROM oferta_praktyki
  WHERE liczba_miejsc > 0 AND semestr_id =
        (SELECT MAX(semestr_id) FROM semestr));

UPDATE oferta_praktyki SET liczba_miejsc = liczba_miejsc - 1
WHERE kod_oferty =

   (SELECT MAX(kod_oferty) FROM oferta_praktyki
   WHERE liczba_miejsc > 0 AND semestr_id =
      (SELECT MAX(semestr_id) FROM semestr));

COMMIT;
-- COMMIT;