-- Easy E2: What are the titles of the articles that Martin Gröhe wrote in the
-- Theory of Computing Systems journal? (Sort in alphabetic order)

SELECT title,author,journal FROM journal_articles WHERE author LIKE '%Martin Grohe%' AND journal = 'Theory Comput. Syst.' ORDER BY title ASC; 