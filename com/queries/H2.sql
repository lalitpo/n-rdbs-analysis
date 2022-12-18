-- Hard H2: Compute the Erdős number (Erdös in DBLP) of Dan Suciu (c.f., explanation below).
WITH RECURSIVE cte (author, distance) AS (
    SELECT 'Paul Erdős', 0
    UNION ALL
    SELECT a.author, c.distance + 1
    FROM cte AS c
    JOIN (
        SELECT author, SPLIT_PART(author, ',', 1) AS co_author
        FROM (
            SELECT author FROM conference_articles
            UNION ALL
            SELECT author FROM journal_articles
        ) AS publications
    ) AS a
    ON c.author = a.co_author
    WHERE a.author <> 'Paul Erdős'
)
SELECT distance
FROM cte
WHERE author = 'Dan Suciu';
