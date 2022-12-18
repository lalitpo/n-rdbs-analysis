-- Easy E2: What are the titles of the articles that Martin Gröhe wrote in the
-- Theory of Computing Systems journal? (Sort in alphabetic order)
SELECT title FROM journal_articles WHERE author = 'Martin Gröhe' ORDER BY title ASC;
