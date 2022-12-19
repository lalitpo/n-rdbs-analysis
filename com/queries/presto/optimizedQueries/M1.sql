-- Medium M1: How many articles were published in the SIGMOD conference
-- proceedings this year?
CREATE INDEX idx_booktitle_year ON conference_articles (booktitle, year); 
SELECT COUNT(*) FROM conference_articles WHERE booktitle = 'SIGMOD Conference' AND year = '2022'; 
