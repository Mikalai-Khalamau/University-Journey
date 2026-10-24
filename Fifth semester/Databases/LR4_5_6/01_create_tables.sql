DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;
DROP TABLE IF EXISTS audiences CASCADE;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS rating CASCADE;
DROP TABLE IF EXISTS lessons CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS study_load CASCADE;
DROP TABLE IF EXISTS prepods CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS type_study_load CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;

CREATE TABLE faculty (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE type_study_load (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE buildings (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(150)
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    faculty_id INTEGER
);

CREATE TABLE prepods (
    id INTEGER PRIMARY KEY,
    last_name VARCHAR(120) NOT NULL,
    first_name VARCHAR(120),
    faculty_id INTEGER
);

CREATE TABLE study_load (
    id VARCHAR(20) PRIMARY KEY,
    hours INTEGER CHECK (hours >= 0),
    subject_id INTEGER,
    type_study_id INTEGER
);

CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    head_group INTEGER,
    faculty_id INTEGER
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    last_name VARCHAR(60) NOT NULL,
    first_name VARCHAR(30),
    group_id INTEGER
);

CREATE TABLE audiences (
    id INTEGER PRIMARY KEY,
    number VARCHAR(10) NOT NULL,
    floor INTEGER,
    capacity INTEGER,
    building_id INTEGER
);

CREATE TABLE lessons (
    group_id INTEGER,
    prepod_id INTEGER,
    study_id VARCHAR(20),
    PRIMARY KEY (group_id, prepod_id, study_id)
);

CREATE TABLE rating (
    id INTEGER PRIMARY KEY,
    rating_date DATE NOT NULL,
    val INTEGER CHECK (is_absent = 'Y' OR val BETWEEN 4 AND 10),
    student_id INTEGER,
    study_id VARCHAR(20),
    prepod_id INTEGER,
    is_absent CHAR(1) DEFAULT 'N'
);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    inventory_num VARCHAR(30) UNIQUE,
    audience_id INTEGER
);

CREATE TABLE schedule (
    id INTEGER PRIMARY KEY,
    lesson_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    audience_id INTEGER,
    group_id INTEGER
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    prepod_id INTEGER
);

ALTER TABLE subjects ADD CONSTRAINT fk_subjects_faculty 
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE;

ALTER TABLE prepods ADD CONSTRAINT fk_prepods_faculty 
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE;

ALTER TABLE study_load ADD CONSTRAINT fk_study_subject 
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE;

ALTER TABLE study_load ADD CONSTRAINT fk_study_type 
    FOREIGN KEY (type_study_id) REFERENCES type_study_load(id) ON DELETE CASCADE;

ALTER TABLE groups ADD CONSTRAINT fk_groups_faculty 
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE;

ALTER TABLE students ADD CONSTRAINT fk_students_group 
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;

ALTER TABLE groups ADD CONSTRAINT fk_groups_head 
    FOREIGN KEY (head_group) REFERENCES students(id) ON DELETE SET NULL;

ALTER TABLE lessons ADD CONSTRAINT fk_lessons_group 
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;

ALTER TABLE lessons ADD CONSTRAINT fk_lessons_prepod 
    FOREIGN KEY (prepod_id) REFERENCES prepods(id) ON DELETE CASCADE;

ALTER TABLE lessons ADD CONSTRAINT fk_lessons_study 
    FOREIGN KEY (study_id) REFERENCES study_load(id) ON DELETE CASCADE;

ALTER TABLE rating ADD CONSTRAINT fk_rating_student 
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE;

ALTER TABLE rating ADD CONSTRAINT fk_rating_study 
    FOREIGN KEY (study_id) REFERENCES study_load(id) ON DELETE CASCADE;

ALTER TABLE rating ADD CONSTRAINT fk_rating_prepod 
    FOREIGN KEY (prepod_id) REFERENCES prepods(id) ON DELETE CASCADE;

ALTER TABLE audiences ADD CONSTRAINT fk_audiences_building 
    FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE;

ALTER TABLE equipment ADD CONSTRAINT fk_equipment_audience 
    FOREIGN KEY (audience_id) REFERENCES audiences(id) ON DELETE CASCADE;

ALTER TABLE schedule ADD CONSTRAINT fk_schedule_audience 
    FOREIGN KEY (audience_id) REFERENCES audiences(id) ON DELETE CASCADE;

ALTER TABLE schedule ADD CONSTRAINT fk_schedule_group 
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;

ALTER TABLE events ADD CONSTRAINT fk_events_prepod 
    FOREIGN KEY (prepod_id) REFERENCES prepods(id) ON DELETE CASCADE;