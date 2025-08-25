SELECT description
FROM crime_scene_reports
WHERE month = 7
  AND day = 28
  AND street = "Humphrey Street";

SELECT transcript
FROM interviews
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND transcript LIKE "%bakery%";

SELECT suspect_id
FROM crime_scene_reports
WHERE month = 7
  AND day = 28
  AND street = "Humphrey Street";

SELECT *
FROM people
WHERE id = 1;

SELECT *
FROM flights
WHERE departure_city = "Fiftyville"
  AND departure_date >= '2024-07-28';

SELECT *
FROM flights_passengers
WHERE flight_id = 10;

SELECT *
FROM people
WHERE id IN (
    SELECT passenger_id
    FROM flights_passengers
    WHERE flight_id = 10
      AND passenger_id != 1
);

SELECT destination_city
FROM flights
WHERE id = 10;

SELECT
    thief.name AS thief_name,
    flight.destination_city AS escape_city,
    accomplice.name AS accomplice_name
FROM crime_scene_reports AS report
JOIN people AS thief
    ON thief.id = report.suspect_id
JOIN flights AS flight
    ON flight.departure_date >= '2024-07-28'
    AND flight.departure_city = "Fiftyville"
JOIN flights_passengers AS fp
    ON fp.flight_id = flight.id
JOIN people AS accomplice
    ON accomplice.id = fp.passenger_id
WHERE report.month = 7
  AND report.day = 28
  AND report.street = "Humphrey Street"
  AND accomplice.id != thief.id;