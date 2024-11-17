-- cSpell: disable

-- Seed some users into the Users table
INSERT INTO Users (uuid, username, password_hash)
VALUES
  ('00000000-0000-0000-0000-000000000000', 'demo', '$argon2id$v=19$m=65536,t=3,p=4$HPOvTEERCj8GLDJnVHN08g$SQrZq5bIOoqxaqqjkYJT7tARXeHBnhzdt382VwwBKtI'),
  ('68c85e40-bbd8-40a1-8b7c-bd1b58bc6d0b', 'bigbenson16', '6eea9b7ef19179a06954edd0f6c05ceb'),
  ('4791e247-4793-4d39-a25b-4f187764773b', 'nartwart0003', 'b7e90aca313e1137f34b439a343cd933'),
  ('b792cde4-19ec-439e-8177-0589434e134b', 'taitaitai', '02c75fb22c75b23dc963c7eb91a062cc'),
  ('903ef56e-4b2c-4b33-9db0-34334c2ff648', 'cs4347guys', 'a2550eeab0724a691192ca13982e6ebd'),
  ('4c209efd-f156-44d9-b6ab-d96c0749864c', 'questcookie', 'a15f31d3578991b0d7734fc6179068e5')
ON CONFLICT (uuid) DO NOTHING;

-- Seed some statistics into the Statistics table
INSERT INTO Statistics (user_uuid, xp, wins, losses)
VALUES
  ('00000000-0000-0000-0000-000000000000', 104, 10, 2),
  ('68c85e40-bbd8-40a1-8b7c-bd1b58bc6d0b', 160, 5, 6),
  ('4791e247-4793-4d39-a25b-4f187764773b', 170, 6, 5),
  ('b792cde4-19ec-439e-8177-0589434e134b', 90, 4, 1),
  ('903ef56e-4b2c-4b33-9db0-34334c2ff648', 90, 3, 3),
  ('4c209efd-f156-44d9-b6ab-d96c0749864c', 20, 1, 0)
ON CONFLICT (user_uuid) DO NOTHING;

-- Seed some sessions into the Sessions table
INSERT INTO Sessions (user_uuid, token)
VALUES
  ('00000000-0000-0000-0000-000000000000', 'aa2979fd-a0a2-4a8d-9c20-8acc3259759b'),
  ('68c85e40-bbd8-40a1-8b7c-bd1b58bc6d0b', '6eaa99af-814f-4fc8-8c79-e2516c955af0'),
  ('4791e247-4793-4d39-a25b-4f187764773b', '29c6a90b-8777-4ae4-b167-99ff43562e2b'),
  ('b792cde4-19ec-439e-8177-0589434e134b', 'c85e9d39-8651-4014-b544-d7856fa9627a')
ON CONFLICT (user_uuid) DO NOTHING;

-- Seed some Tags into the Tags table
INSERT INTO Tags (id, name, description)
VALUES
  (1, 'Geography', 'Covers countries, capitals, continents, and landmarks.'),
  (2, 'Science', 'Includes physics, chemistry, biology, and environmental science.'),
  (3, 'History', 'Questions on historical events, important dates, and influential figures.'),
  (4, 'Literature', 'Famous books, authors, plays, and literary works.'),
  (5, 'Mathematics', 'Encompasses numbers, basic arithmetic, and mathematical concepts.'),
  (6, 'Art & Culture', 'Topics in art, famous paintings, cultural icons, and classical music.'),
  (7, 'Technology', 'Questions about inventions, computers, the internet, and tech advancements.'),
  (8, 'Nature', 'Encompasses animals, plants, ecosystems, and natural phenomena.'),
  (9, 'Space', 'Questions on planets, stars, galaxies, and space exploration.'),
  (10, 'General', 'Broad category for pop culture, everyday knowledge, and trivia.')
ON CONFLICT (id) DO NOTHING;

-- Seed some Questions into the Questions table
INSERT INTO Questions (id, question, difficulty, option1, option2, option3, option4)
VALUES
  (1, 'What is the capital of France?', 1, 'Paris', 'Berlin', 'Madrid', 'Rome'),
  (2, 'Which planet is known as the Red Planet?', 1, 'Mars', 'Earth', 'Jupiter', 'Venus'),
  (3, 'Who wrote "Romeo and Juliet"?', 2, 'William Shakespeare', 'Charles Dickens', 'Mark Twain', 'Jane Austen'),
  (4, 'What is the largest mammal on Earth?', 2, 'Blue Whale', 'Elephant', 'Giraffe', 'Polar Bear'),
  (5, 'What is the smallest prime number?', 1, '2', '1', '3', '5'),
  (6, 'Which gas is most abundant in Earth''s atmosphere?', 3, 'Nitrogen', 'Oxygen', 'Carbon Dioxide', 'Hydrogen'),
  (7, 'Who painted the Mona Lisa?', 2, 'Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 'Claude Monet'),
  (8, 'In which year did World War II end?', 3, '1945', '1941', '1950', '1963'),
  (9, 'How many continents are there on Earth?', 1, '7', '5', '6', '8'),
  (10, 'What is the currency of Japan?', 1, 'Yen', 'Yuan', 'Won', 'Rupee'),
  (11, 'Which element has the atomic number 1?', 1, 'Hydrogen', 'Helium', 'Oxygen', 'Nitrogen'),
  (12, 'Who developed the theory of relativity?', 2, 'Albert Einstein', 'Isaac Newton', 'Galileo Galilei', 'Nikola Tesla'),
  (13, 'The Statue of Liberty was a gift from which country?', 2, 'France', 'Germany', 'Canada', 'United Kingdom'),
  (14, 'What is the best natural substance on Earth?', 2, 'Gold', 'Iron', 'Diamond', 'Quartz'),
  (15, 'Which planet has the most moons?', 3, 'Saturn', 'Earth', 'Jupiter', 'Mars'),
  (16, 'How many bones are in the human body?', 2, '206', '201', '195', '210'),
  (17, 'Which ocean is the largest?', 1, 'Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'),
  (18, 'What is the longest river in the world?', 3, 'Amazon River', 'Nile River', 'Yangtze River', 'Mississippi River'),
  (19, 'Who was the first man to walk on the moon?', 2, 'Neil Armstrong', 'Buzz Aldrin', 'Michael Collins', 'Yuri Gagarin'),
  (20, 'What does DNA stand for?', 3, 'Deoxyribonucleic Acid', 'Dinucleic Acid', 'Deoxynucleotide Acid', 'Deoxyribose Acid'),
  (21, 'What is the hardest natural substance on Earth?', 1, 'Diamond', 'Gold', 'Iron', 'Quartz'),
  (22, 'Which country is known as the Land of the Rising Sun?', 2, 'Japan', 'China', 'South Korea', 'Thailand'),
  (23, 'What is the largest planet in our solar system?', 1, 'Jupiter', 'Saturn', 'Earth', 'Neptune'),
  (24, 'What is the smallest country in the world by land area?', 1, 'Vatican City', 'Monaco', 'Nauru', 'San Marino'),
  (25, 'Which famous scientist developed the laws of motion?', 2, 'Isaac Newton', 'Albert Einstein', 'Galileo Galilei', 'Nikola Tesla'),
  (26, 'What is the main ingredient in guacamole?', 1, 'Avocado', 'Tomato', 'Cucumber', 'Onion'),
  (27, 'What is the capital of Canada?', 3, 'Ottawa', 'Toronto', 'Vancouver', 'Montreal'),
  (28, 'What is the national animal of Australia?', 2, 'Kangaroo', 'Koala', 'Emu', 'Platypus'),
  (29, 'Which element is the most abundant in the Earth''s crust?', 1, 'Oxygen', 'Silicon', 'Iron', 'Aluminum'),
  (30, 'What is the tallest mountain in the world?', 2, 'Mount Everest', 'K2', 'Mount Kilimanjaro', 'Mount Fuji'),
  (31, 'What year did the Titanic sink?', 1, '1912', '1900', '1920', '1898'),
  (32, 'Which ocean is the smallest?', 3, 'Arctic Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Pacific Ocean'),
  (33, 'Who invented the lightbulb?', 1, 'Thomas Edison', 'Nikola Tesla', 'Alexander Graham Bell', 'Benjamin Franklin'),
  (34, 'Which animal is known for its black and white stripes?', 2, 'Zebra', 'Tiger', 'Giraffe', 'Panda'),
  (35, 'In what year did the United States declare independence?', 3, '1776', '1789', '1790', '1800'),
  (36, 'What is the currency of the United Kingdom?', 1, 'Pound Sterling', 'Euro', 'Dollar', 'Yen'),
  (37, 'What is the longest-running TV show in the U.S.?', 2, 'The Simpsons', 'Friends', 'The Office', 'Seinfeld'),
  (38, 'Who was the first woman to fly solo across the Atlantic Ocean?', 1, 'Amelia Earhart', 'Bessie Coleman', 'Sally Ride', 'Harriet Quimby'),
  (39, 'What is the chemical symbol for gold?', 2, 'Au', 'Ag', 'Pb', 'Fe'),
  (40, 'Which famous artist is known for cutting off part of his own ear?', 3, 'Vincent van Gogh', 'Pablo Picasso', 'Claude Monet', 'Salvador Dalí')
ON CONFLICT (id) DO NOTHING;

-- Seed some Question_Tags into the Question_Tags table
INSERT INTO Question_Tags (question_id, tag_id)
VALUES
  (1, 1),
  (2, 2),
  (2, 9),
  (3, 4),
  (4, 2),
  (4, 8),
  (5, 5),
  (6, 2),
  (7, 6),
  (8, 3),
  (9, 1),
  (10, 1),
  (11, 2),
  (12, 2),
  (12, 8),
  (13, 3),
  (14, 2),
  (14, 8),
  (15, 9),
  (16, 2),
  (17, 1),
  (18, 8),
  (18, 10),
  (19, 2),
  (19, 3),
  (20, 2),
  (21, 2),
  (22, 1),
  (23, 9),
  (24, 1),
  (25, 2),
  (26, 10),
  (27, 1),
  (28, 8),
  (29, 2),
  (30, 1),
  (31, 3),
  (32, 1),
  (33, 2),
  (34, 8),
  (35, 3),
  (36, 1),
  (37, 10),
  (38, 3),
  (39, 2),
  (40, 6)
ON CONFLICT (question_id, tag_id) DO NOTHING;
