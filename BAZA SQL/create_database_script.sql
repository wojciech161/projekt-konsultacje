-- Database create script for MySQL
-- Author: Marcin Wojciechowski
-- Date: 12.03.2012

START TRANSACTION;

CREATE TABLE IF NOT EXISTS Users (
	user_ID int NOT NULL AUTO_INCREMENT,
	login varchar(50),
	lastLoginDate timestamp DEFAULT 0,
	type VARCHAR(15),
    
	CONSTRAINT users_PK PRIMARY KEY (user_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Students (
	student_ID int NOT NULL,
	name varchar(20),
	surname varchar(50),
	albumNumber int,
	faculty varchar(40),
	studyYear int,
	major varchar(60),
    
	CONSTRAINT students_PK PRIMARY KEY (student_ID),
  CONSTRAINT students_ID_FK FOREIGN KEY (student_ID) 
                         REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Administrators (
	administrator_ID int NOT NULL,
	name varchar(20),
	surname varchar(50),
    
	CONSTRAINT administrators_PK PRIMARY KEY (administrator_ID),
  CONSTRAINT administrators_ID_FK FOREIGN KEY (administrator_ID)
                          REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Assistants (
	assistant_ID int NOT NULL,
	name varchar(20),
	surname varchar(50),
    
	CONSTRAINT assistants_PK PRIMARY KEY (assistant_ID),
  CONSTRAINT assistants_ID_FK FOREIGN KEY (assistant_ID)
                          REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS InfoBoards (
	infoboard_ID int NOT NULL AUTO_INCREMENT,
	dateOfAdding timestamp DEFAULT 0,
	message varchar(300),
    
	CONSTRAINT infoboards_PK PRIMARY KEY (infoboard_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Localizations (
	localization_ID int NOT NULL AUTO_INCREMENT,
	room varchar(8),
	building varchar(8),
    
	CONSTRAINT localizationIDpk PRIMARY KEY (localization_ID)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Tutors (
	tutor_ID int NOT NULL,
	degree varchar(40),
	name varchar(20),
	surname varchar(50),
	institute varchar(50),
	phone varchar(20),
	email varchar(50),
	www varchar (60),
	localization_ID int,
	infoboard_ID int,
    
	CONSTRAINT tutors_PK PRIMARY KEY (tutor_ID),
  CONSTRAINT tutors_ID_FK FOREIGN KEY (tutor_ID)
                      REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT tutors_localization_ID_FK FOREIGN KEY (localization_ID)
                      REFERENCES Localizations(localization_id) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT tutors_infoboard_ID_FK FOREIGN KEY (infoboard_ID)
                      REFERENCES InfoBoards(infoboard_ID) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Consultations (
	consultation_ID int NOT NULL AUTO_INCREMENT,
	tutor_ID int NOT NULL,
	startHour time,
	endHour time,
	day varchar(15),
	weekType varchar(1),
	studentsLimit int,
  localization_ID int,
  
	CONSTRAINT consultations_PK PRIMARY KEY (consultation_ID),
  CONSTRAINT consultations_tutor_ID_FK FOREIGN KEY (tutor_ID)
                     REFERENCES Tutors(tutor_ID) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT consultations_localization_ID_FK FOREIGN KEY (localization_ID)
                     REFERENCES Localizations(localization_ID) ON DELETE CASCADE ON UPDATE CASCADE               
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ConsultationAssignments (
	student_ID int NOT NULL,
	consultation_ID int NOT NULL,
  day date NOT NULL,

  CONSTRAINT consultationAssignments_PK PRIMARY KEY (student_ID, consultation_ID),
  CONSTRAINT consultationAssignments_student_ID_FK FOREIGN KEY (student_ID)   
                      REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT consultationAssignments_consultation_ID_FK FOREIGN KEY (consultation_ID)   
                      REFERENCES Consultations(consultation_id) ON DELETE CASCADE ON UPDATE CASCADE                   
) ENGINE=InnoDB;

COMMIT;
