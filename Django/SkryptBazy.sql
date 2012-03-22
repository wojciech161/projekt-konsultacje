BEGIN;
CREATE TABLE `consultations_users` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `login` varchar(50) NOT NULL,
    `last_login_date` datetime NOT NULL
)
;
CREATE TABLE `consultations_students` (
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
ALTER TABLE `consultations_students` ADD CONSTRAINT `student_ID_id_refs_id_7730a2dc` FOREIGN KEY (`student_ID_id`) REFERENCES `consultations_users` (`id`);
CREATE TABLE `consultations_administrators` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `administrator_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `consultations_administrators` ADD CONSTRAINT `administrator_ID_id_refs_id_13a35d7c` FOREIGN KEY (`administrator_ID_id`) REFERENCES `consultations_users` (`id`);
CREATE TABLE `consultations_assistants` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `assistant_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `consultations_assistants` ADD CONSTRAINT `assistant_ID_id_refs_id_73696dd9` FOREIGN KEY (`assistant_ID_id`) REFERENCES `consultations_users` (`id`);
CREATE TABLE `consultations_infoboards` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date_of_adding` datetime NOT NULL,
    `message` varchar(300) NOT NULL
)
;
CREATE TABLE `consultations_localizations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `room` varchar(8) NOT NULL,
    `building` varchar(8) NOT NULL
)
;
CREATE TABLE `consultations_tutors` (
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
ALTER TABLE `consultations_tutors` ADD CONSTRAINT `tutor_ID_id_refs_id_2fbbb1bb` FOREIGN KEY (`tutor_ID_id`) REFERENCES `consultations_users` (`id`);
ALTER TABLE `consultations_tutors` ADD CONSTRAINT `localization_ID_id_refs_id_4b238d2b` FOREIGN KEY (`localization_ID_id`) REFERENCES `consultations_localizations` (`id`);
ALTER TABLE `consultations_tutors` ADD CONSTRAINT `infoboard_ID_id_refs_id_b1bfd77f` FOREIGN KEY (`infoboard_ID_id`) REFERENCES `consultations_infoboards` (`id`);
CREATE TABLE `consultations_consultations` (
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
ALTER TABLE `consultations_consultations` ADD CONSTRAINT `localization_ID_id_refs_id_ccbdf76f` FOREIGN KEY (`localization_ID_id`) REFERENCES `consultations_localizations` (`id`);
ALTER TABLE `consultations_consultations` ADD CONSTRAINT `tutor_ID_id_refs_id_53b68a33` FOREIGN KEY (`tutor_ID_id`) REFERENCES `consultations_tutors` (`id`);
CREATE TABLE `consultations_consultationassignments` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `student_ID_id` integer NOT NULL,
    `consultation_ID_id` integer NOT NULL,
    `day` datetime NOT NULL
)
;
ALTER TABLE `consultations_consultationassignments` ADD CONSTRAINT `consultation_ID_id_refs_id_6c13cb60` FOREIGN KEY (`consultation_ID_id`) REFERENCES `consultations_consultations` (`id`);
ALTER TABLE `consultations_consultationassignments` ADD CONSTRAINT `student_ID_id_refs_id_b093e067` FOREIGN KEY (`student_ID_id`) REFERENCES `consultations_students` (`id`);
COMMIT;
