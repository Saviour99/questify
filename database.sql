CREATE DATABASE IF NOT EXISTS quizz_info;

USE quizz_info;

CREATE TABLE IF NOT EXISTS `Q&A_Table` (
    `source_file_id` INT NOT NULL,
    `question_id` INT NOT NULL AUTO_INCREMENT,
    `question` VARCHAR(300) NOT NULL,
    `option_a` VARCHAR(100) NOT NULL,
    `option_b` VARCHAR(100) NOT NULL,
    `option_c` VARCHAR(100) NOT NULL,
    `option_d` VARCHAR(100) NOT NULL,
    `answer` VARCHAR(100) NOT NULL,
    `file_name` VARCHAR(100) NOT NULL,
    `timestamp` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`question_id`)
);
