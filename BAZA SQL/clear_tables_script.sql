START TRANSACTION;

DELETE IGNORE FROM Users;
DELETE IGNORE FROM Students;
DELETE IGNORE FROM Administrators;
DELETE IGNORE FROM Assistants;
DELETE IGNORE FROM Infoboards;
DELETE IGNORE FROM Localizations;
DELETE IGNORE FROM Tutors;
DELETE IGNORE FROM Consultations;
DELETE IGNORE FROM ConsultationAssignments;

COMMIT;