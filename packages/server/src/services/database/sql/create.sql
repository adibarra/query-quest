-- cSpell: disable

-- Table that holds all trivia questions and relevant metadata
CREATE TABLE IF NOT EXISTS Questions(
  id SERIAL NOT NULL,
  question VARCHAR(500) NOT NULL,
  difficulty SMALLINT NOT NULL,
  option1 VARCHAR(50) NOT NULL,
  option2 VARCHAR(50) NOT NULL,
  option3 VARCHAR(50) DEFAULT NULL,
  option4 VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (id)
);

-- Table that holds information about user accounts
CREATE TABLE IF NOT EXISTS Users(
  uuid CHAR(36) NOT NULL,
  username VARCHAR(16) UNIQUE NOT NULL,
  password_hash VARCHAR(100) NOT NULL,
  PRIMARY KEY (uuid)
);

-- Table that keeps track of logged in users
CREATE TABLE IF NOT EXISTS Sessions(
  user_uuid CHAR(36) NOT NULL,
  token CHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (user_uuid),
  FOREIGN KEY (user_uuid)
    REFERENCES users(uuid)
    ON DELETE CASCADE
);

-- Table that keeps track of user trivia statistics
CREATE TABLE IF NOT EXISTS Statistics (
  user_uuid CHAR(36) NOT NULL,
  xp BIGINT DEFAULT 0 NOT NULL,
  wins INT DEFAULT 0 NOT NULL,
  losses INT DEFAULT 0 NOT NULL,
  PRIMARY KEY (user_uuid),
  FOREIGN KEY (user_uuid)
    REFERENCES users(uuid)
    ON DELETE CASCADE
);

-- Table that holds information about trivia questions tags
CREATE TABLE IF NOT EXISTS Tags(
  id SERIAL NOT NULL,
  name VARCHAR(16) UNIQUE NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

-- Junction table used to associate tags with questions
CREATE TABLE IF NOT EXISTS Question_Tags (
  question_id BIGINT NOT NULL,
  tag_id BIGINT NOT NULL,
  PRIMARY KEY (question_id, tag_id),
  FOREIGN KEY (question_id)
    REFERENCES Questions(id)
    ON DELETE CASCADE,
  FOREIGN KEY (tag_id)
    REFERENCES Tags(id)
    ON DELETE CASCADE
);
