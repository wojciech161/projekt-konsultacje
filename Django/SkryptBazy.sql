BEGIN;
CREATE TABLE `consultations_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `login` varchar(50) NOT NULL,
    `last_login_date` datetime,
    `typ` varchar(15) NOT NULL
)
;
CREATE TABLE `consultations_student` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `student_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL,
    `album_number` integer NOT NULL,
    `faculty` varchar(40),
    `study_year` integer,
    `major` varchar(60)
)
;
ALTER TABLE `consultations_student` ADD CONSTRAINT `student_ID_id_refs_id_eb0b6ca` FOREIGN KEY (`student_ID_id`) REFERENCES `consultations_user` (`id`);
CREATE TABLE `consultations_administrator` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `administrator_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `consultations_administrator` ADD CONSTRAINT `administrator_ID_id_refs_id_5bf5dfca` FOREIGN KEY (`administrator_ID_id`) REFERENCES `consultations_user` (`id`);
CREATE TABLE `consultations_assistant` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `assistant_ID_id` integer NOT NULL,
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL
)
;
ALTER TABLE `consultations_assistant` ADD CONSTRAINT `assistant_ID_id_refs_id_7d319b79` FOREIGN KEY (`assistant_ID_id`) REFERENCES `consultations_user` (`id`);
CREATE TABLE `consultations_infoboard` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date_of_adding` datetime NOT NULL,
    `message` varchar(300)
)
;
CREATE TABLE `consultations_localization` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `room` varchar(8) NOT NULL,
    `building` varchar(8) NOT NULL
)
;
CREATE TABLE `consultations_tutor` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tutor_ID_id` integer NOT NULL,
    `degree` varchar(40),
    `name` varchar(20) NOT NULL,
    `surname` varchar(50) NOT NULL,
    `institute` varchar(50) NOT NULL,
    `phone` varchar(20),
    `email` varchar(50) NOT NULL,
    `www` varchar(60),
    `localization_ID_id` integer NOT NULL,
    `infoboard_ID_id` integer NOT NULL
)
;
ALTER TABLE `consultations_tutor` ADD CONSTRAINT `localization_ID_id_refs_id_c848e499` FOREIGN KEY (`localization_ID_id`) REFERENCES `consultations_localization` (`id`);
ALTER TABLE `consultations_tutor` ADD CONSTRAINT `tutor_ID_id_refs_id_a8937665` FOREIGN KEY (`tutor_ID_id`) REFERENCES `consultations_user` (`id`);
ALTER TABLE `consultations_tutor` ADD CONSTRAINT `infoboard_ID_id_refs_id_77c84a0d` FOREIGN KEY (`infoboard_ID_id`) REFERENCES `consultations_infoboard` (`id`);
CREATE TABLE `consultations_consultation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tutor_ID_id` integer NOT NULL,
    `start_hour` datetime NOT NULL,
    `end_hour` datetime NOT NULL,
    `day` varchar(15) NOT NULL,
    `week_type` varchar(1) NOT NULL,
    `students_limit` integer,
    `localization_ID_id` integer NOT NULL
)
;
ALTER TABLE `consultations_consultation` ADD CONSTRAINT `localization_ID_id_refs_id_ab94da9b` FOREIGN KEY (`localization_ID_id`) REFERENCES `consultations_localization` (`id`);
ALTER TABLE `consultations_consultation` ADD CONSTRAINT `tutor_ID_id_refs_id_16147b69` FOREIGN KEY (`tutor_ID_id`) REFERENCES `consultations_tutor` (`id`);
CREATE TABLE `consultations_consultationassignment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `student_ID_id` integer NOT NULL,
    `consultation_ID_id` integer NOT NULL,
    `day` datetime NOT NULL
)
;
ALTER TABLE `consultations_consultationassignment` ADD CONSTRAINT `student_ID_id_refs_id_e2ac55c3` FOREIGN KEY (`student_ID_id`) REFERENCES `consultations_student` (`id`);
ALTER TABLE `consultations_consultationassignment` ADD CONSTRAINT `consultation_ID_id_refs_id_9b95c80e` FOREIGN KEY (`consultation_ID_id`) REFERENCES `consultations_consultation` (`id`);
COMMIT;
