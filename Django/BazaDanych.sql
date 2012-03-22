BEGIN;
CREATE TABLE `polls_users` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `login` varchar(50) NOT NULL,
    `last_login_date` datetime NOT NULL
)
;
CREATE TABLE `polls_students` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `student_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL,
    `album_number` integer NOT NULL,
    `faculty` varchar(40) NOT NULL,
    `study_year` integer NOT NULL,
    `major` varchar(60) NOT NULL
)
;
ALTER TABLE `polls_students` ADD CONSTRAINT `student_ID_id_refs_id_8508d164` FOREIGN KEY (`student_ID_id`) REFERENCES `polls_users` (`id`);
CREATE TABLE `polls_administrators` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `administrator_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `polls_administrators` ADD CONSTRAINT `administrator_ID_id_refs_id_ffaa100c` FOREIGN KEY (`administrator_ID_id`) REFERENCES `polls_users` (`id`);
CREATE TABLE `polls_assistants` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `assistant_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `polls_assistants` ADD CONSTRAINT `assistant_ID_id_refs_id_b78ccc79` FOREIGN KEY (`assistant_ID_id`) REFERENCES `polls_users` (`id`);
CREATE TABLE `polls_infoboards` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date_of_adding` datetime NOT NULL,
    `message` varchar(300) NOT NULL
)
;
CREATE TABLE `polls_localizations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `room` varchar(8) NOT NULL,
    `building` varchar(8) NOT NULL
)
;
CREATE TABLE `polls_tutors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tutor_ID_id` integer NOT NULL,
    `degree` varchar(40) NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL,
    `institute` varchar(50) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `email` varchar(50) NOT NULL,
    `www` varchar(60) NOT NULL,
    `localization_ID_id` integer NOT NULL,
    `infoboard_ID_id` integer NOT NULL
)
;
ALTER TABLE `polls_tutors` ADD CONSTRAINT `localization_ID_id_refs_id_2dc3582b` FOREIGN KEY (`localization_ID_id`) REFERENCES `polls_localizations` (`id`);
ALTER TABLE `polls_tutors` ADD CONSTRAINT `infoboard_ID_id_refs_id_6747a8c1` FOREIGN KEY (`infoboard_ID_id`) REFERENCES `polls_infoboards` (`id`);
ALTER TABLE `polls_tutors` ADD CONSTRAINT `tutor_ID_id_refs_id_2b31ec4b` FOREIGN KEY (`tutor_ID_id`) REFERENCES `polls_users` (`id`);
CREATE TABLE `polls_consultations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tutor_ID_id` integer NOT NULL,
    `start_hour` datetime NOT NULL,
    `end_hour` datetime NOT NULL,
    `day` varchar(15) NOT NULL,
    `week_type` varchar(1) NOT NULL,
    `students_limit` integer NOT NULL,
    `localization_ID_id` integer NOT NULL
)
;
ALTER TABLE `polls_consultations` ADD CONSTRAINT `localization_ID_id_refs_id_2482ad41` FOREIGN KEY (`localization_ID_id`) REFERENCES `polls_localizations` (`id`);
ALTER TABLE `polls_consultations` ADD CONSTRAINT `tutor_ID_id_refs_id_1d95b2cd` FOREIGN KEY (`tutor_ID_id`) REFERENCES `polls_tutors` (`id`);
CREATE TABLE `polls_consultationassignments` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `student_ID_id` integer NOT NULL,
    `consultation_ID_id` integer NOT NULL,
    `day` datetime NOT NULL
)
;
ALTER TABLE `polls_consultationassignments` ADD CONSTRAINT `consultation_ID_id_refs_id_887a4a30` FOREIGN KEY (`consultation_ID_id`) REFERENCES `polls_consultations` (`id`);
ALTER TABLE `polls_consultationassignments` ADD CONSTRAINT `student_ID_id_refs_id_88bd66c7` FOREIGN KEY (`student_ID_id`) REFERENCES `polls_students` (`id`);
COMMIT;
