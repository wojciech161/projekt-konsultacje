-- Database create script for MySQL
-- Author: Marcin Wojciechowski
-- Date: 12.03.2012

START TRANSACTION;

CREATE TABLE IF NOT EXISTS Users (
	user_ID int NOT NULL AUTO_INCREMENT,
	login varchar(50),
	lastLoginDate TIMESTAMP,
	type VARCHAR(15),
	CONSTRAINT userIDpk PRIMARY KEY (user_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Students (
	students_ID int NOT NULL AUTO_INCREMENT,
	name varchar(20),
	surname varchar(50),
	albumNumber int,
	faculty varchar(40),
	study_year int,
	major varchar(60),
	CONSTRAINT studentIDpk PRIMARY KEY (students_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Administrators (
	administrator_ID int NOT NULL AUTO_INCREMENT,
	name varchar(20),
	surname varchar(50),
	CONSTRAINT administratorsIDpk PRIMARY KEY (administrator_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Assistants (
	assistant_ID int NOT NULL AUTO_INCREMENT,
	name varchar(20),
	surname varchar(50),
	CONSTRAINT assistantIDpk PRIMARY KEY (assistant_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Tutors (
	tutor_ID int NOT NULL AUTO_INCREMENT,
	degree varchar(40),
	name varchar(20),
	surname varchar(50),
	institute varchar(50),
	phone varchar(20),
	email varchar(50),
	www varchar (60),
	localization_ID int NOT NULL,
	infoboard_ID int NOT NULL,
	CONSTRAINT tutorIDpk PRIMARY KEY (tutor_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ConsultationAssignments (
	students_ID int NOT NULL,
	consultations_ID int NOT NULL,
	tutor_ID int NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Consultations (
	consultations_ID int NOT NULL AUTO_INCREMENT,
	tutor_ID int NOT NULL,
	startHour time,
	endHour time,
	consultation_day varchar(15),
	weekType varchar(1),
	studentsLimit int,
	CONSTRAINT consultationIDpk PRIMARY KEY (consultations_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Localizations (
	localization_ID int NOT NULL AUTO_INCREMENT,
	room varchar(8),
	building varchar(8),
	CONSTRAINT localizationIDpk PRIMARY KEY (localization_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS InfoBoards (
	infoboard_ID int NOT NULL AUTO_INCREMENT,
	dateOfAdding TIMESTAMP,
	message varchar(300),
	CONSTRAINT infoboardIDpk PRIMARY KEY (infoboard_ID)
) ENGINE=InnoDB;

ALTER TABLE Students ADD CONSTRAINT StudentsUsers_fk
FOREIGN KEY (students_ID)
REFERENCES Users (user_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Administrators ADD CONSTRAINT AdministratorsUsers_fk
FOREIGN KEY (administrator_ID)
REFERENCES Users (user_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Assistants ADD CONSTRAINT AssistantsUsers_fk
FOREIGN KEY (assistant_ID)
REFERENCES Users (user_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Tutors ADD CONSTRAINT TutorsUsers_fk
FOREIGN KEY (tutor_ID)
REFERENCES Users (user_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Consultations ADD CONSTRAINT ConsultationsTutors_fk
FOREIGN KEY (tutor_ID)
REFERENCES Tutors (tutor_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE ConsultationAssignments ADD CONSTRAINT CAConsultations_fk1
FOREIGN KEY (consultations_ID)
REFERENCES Consultations (consultations_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE ConsultationAssignments ADD CONSTRAINT CAConsultations_fk2
FOREIGN KEY (tutor_ID)
REFERENCES Consultations (tutor_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE ConsultationAssignments ADD CONSTRAINT CAStudents_fk
FOREIGN KEY (students_ID)
REFERENCES Students (students_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Tutors ADD CONSTRAINT LocalizationsTutors_fk
FOREIGN KEY (localization_ID)
REFERENCES Localizations (localization_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

ALTER TABLE Tutors ADD CONSTRAINT IBTuturs_fk
FOREIGN KEY (infoboard_ID)
REFERENCES InfoBoards (infoboard_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

COMMIT;
