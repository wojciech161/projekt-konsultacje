INSERT INTO Users (user_ID, login, type)
VALUES (1, 'jkowalski', 'student'), (2, 'jnowak', 'tutor'), (3, 'kabacki', 'student'),
       (4, 'ametycki', 'student'), (5, 'topolski', 'student'), (6, 'mdebin', 'student'),
       (7, 'dasist', 'assistant'), (8, 'madmin', 'administrator'), (9, 'lopek', 'tutor'),
       (10, 'aabacki', 'tutor'), (11, 'aporywek', 'student'), (12, 'mopanek', 'tutor');
   
INSERT INTO Students (student_ID, name, surname, albumNumber, faculty, studyYear, major)
VALUES (1, 'Jan', 'Kowalski', 112233, 'EKA', 3, 'INF'),
       (3, 'Kazimierz', 'Abacki', 112244, 'EKA', 3, 'AIR'),
       (4, 'Adam', 'Metycki', 112255, 'EKA', 2, 'INF'),
       (5, 'Tomasz', 'Opolski', 112266, 'EKA', 1, 'AIR'),
       (6, 'Mariusz', 'Debin', 112277, 'EKA', 3, 'EIT'),
       (11, 'Amadeusz', 'Porywek', 112288, 'EKA', 4, 'TIN');
   
INSERT INTO Administrators (administrator_ID, name, surname)
VALUES (8, 'Marek', 'Admin');

INSERT INTO Assistants (assistant_ID, name, surname)
VALUES (7, 'Daria', 'Asist');

INSERT INTO InfoBoards (infoboard_ID, message)
VALUES (1, 'Pilna wiadomosc infoboard nr 1'), (2, 'Pilna wiadomosc infoboard nr 2'),
       (3, 'Pilna wiadomosc infoboard nr 3'), (4, 'Pilna wiadomosc infoboard nr 4');
    
INSERT INTO Localizations (localization_ID, room, building)
VALUES (1, '016', 'C3'), (2, '224', 'C3'), (3, '40', 'C4'), (4, '305', 'C3');

INSERT INTO Tutors (tutor_ID, degree, name, surname, institute, phone, 
                    email, www, localization_ID, infoboard_ID)
VALUES (2, 'dr inz.', 'Jan', 'Nowak', 'ZAK', '071-321-22-22', 'Jan.Nowak@pwr.wroc.pl', NULL, 1, 1),
(9, 'dr inz.', 'Leopold', 'Opek', 'ZSK', '071-321-21-21', 'Leopold.Opek@pwr.wroc.pl', NULL, 2, 2),
(10, 'dr inz.', 'Adam', 'Abacki', 'IIAR', NULL, 'Adam.Abacki@pwr.wroc.pl', 'www.aabacki.pl', 3, 3),
(12, 'prof.', 'Marian', 'Opanek', 'ZAK', '071-323-33-61', 'Marian.Opanek@pwr.wroc.pl', NULL, 4, 4);

INSERT INTO Consultations (consultation_ID, tutor_ID, startHour, endHour, 
                           day, weekType, studentsLimit, localization_ID)
VALUES (1, 2, '09:15:00', '11:15:00', 'Poniedzialek', 'A', 15, 1),
       (2, 2, '09:15:00', '11:15:00', 'Wtorek', 'A', 15, 1),
       (3, 9, '11:15:00', '13:15:00', 'Czwartek', 'A', 15, 2),
       (4, 9, '15:15:00', '17:15:00', 'Wtorek', 'A', 15, 2),
       (5, 10, '13:15:00', '15:15:00', 'Sroda', 'A', 15, 3),
       (6, 10, '17:15:00', '19:15:00', 'Piatek', 'A', 15, 3),
       (7, 12, '09:15:00', '11:15:00', 'Poniedzialek', 'A', 15, 4),
       (8, 12, '15:15:00', '17:15:00', 'Czwartek', 'A', 15, 4);
       
INSERT INTO ConsultationAssignments (student_ID, consultation_ID, day)
VALUES (1, 1, '2012-03-12'), (3, 1, '2012-03-12'), (4, 2, '2012-03-13'), (5, 2, '2012-03-13');
       
