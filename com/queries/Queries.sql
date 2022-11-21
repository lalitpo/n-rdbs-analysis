-- Easy E1: Who is the publisher of the PODS conference proceedings?
SELECT publisher
FROM conference_proceedings
WHERE title like '%PODS%';

-- Easy E2: What are the titles of the articles that Martin Gröhe wrote in the
-- Theory of Computing Systems journal? (Sort in alphabetic order)
SELECT title
FROM journal_articles
WHERE journal like '%Theory of Computing Systems%';

-- Medium M1: How many articles were published in the SIGMOD conference
-- proceedings this year?


-- Medium M2: How many articles were published in the oldest journal, and
-- what is its title?


-- Medium M3: What was the median amount of articles published for each
-- year of the CIDR conference.


-- Medium M4: In which year did the SIGMOD conference have the most
-- papers with over 10 authors?


-- Medium M5: Who were the most frequent editors for the PODS conference?

-- How many times were they an editor?


-- Medium M6: For the researcher(s) with the most overall (conference & journal)
-- publications: to how many different conferences did they publish?


-- Hard
-- H1: For each researcher that published to the ICDT conference in 2020:
-- Who was their most frequently occurring co-author (conference & journal)?

-- How many times did they collaborate?


-- Hard H2: Compute the Erdős number (Erdös in DBLP) of Dan Suciu (c.f., explanation below).


-- Bonus B1: Invent an interesting query that incorporates a cyclic join.


-- Bonus B2: Create your own recursive query that illustrates something useful.

