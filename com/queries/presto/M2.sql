-- Medium M2: How many articles were published in the oldest journal, and
-- what is its title?
SELECT COUNT(*) AS num_articles, title FROM journal_articles WHERE year = (SELECT MIN(year) FROM journal_articles) GROUP BY title; 
