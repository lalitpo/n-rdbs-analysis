# E1: Who is the publisher of PODS conference proceedings ?
E1 = """
GRAPH.QUERY dblp "MATCH (b:book {booktitle:'PODS'})<-[:published_in]-(c:conferences)-[:published_by]->(p:publisher) RETURN p.name"
"""

# What are the titles of the articles that Martin Gröhe wrote in the Theory of Computing Systems journal? (Sort in alphabetic order)
E2 = """
GRAPH.QUERY dblp "MATCH (j:journal {journal: 'Theor. Comput. Sci.'})<-[:published_in]-(a:j_articles)-[:written_by]->(b:author {name:'Martin Grohe'}) RETURN a ORDER BY a.title ASC"
"""

# How many articles were published in the SIGMOD conference proceedings this year?
M1 = """
GRAPH.QUERY dblp "MATCH (:journal {journal: 'SIGMOID'})<-[:published_in]-(a:j_articles)-[:written_year]->(:author {year:2022}) RETURN COUNT(a)"
"""

# M2: How many articles were published in the oldest journal, and what is its title?
M2 = """
GRAPH.QUERY dblp "MATCH (y:year)<-[:published_year]-(a:j_articles) WITH MIN(y) AS min_year MATCH (y:year)<-[:published_year]-(a:j_articles)-[:published_in]->(j:journal) WHERE y = min_year RETURN COUNT(a), j.journal LIMIT 1"
"""

# M3:  What was the median amount of articles published for each year of the CIDR conference.
M3 = """
GRAPH.QUERY dblp "MATCH (:journal {journal: 'CIDR'})<-[:published_in]-(:j_articles)-[:written_year]->(y:year) WITH y.year AS year, COUNT(a) AS count RETURN year, count ORDER BY year ASC"
"""

# M4: In which year did the SIGMOD conference have the most papers with over 10 authors?
M4 = """
GRAPH.QUERY dblp "MATCH (:journal {journal: 'SIGMOID'})<-[:published_in]-(a:j_articles)-[:written_by]->(auth:author) WITH a, COUNT(auth) AS count ORDER BY count DESC WHERE count > 10 MATCH (a)-[:written_year]->(y:year) RETURN y.year, count LIMIT 1"
"""

# M5: Who were the most frequent editors for the PODS conference? How many times were they an editor?
M5 = """
GRAPH.QUERY dblp "MATCH (:book {booktitle:'PODS'})<-[:published_in]-(a:conferences)-[:edited_by]->(e:editor) WITH e, COUNT(a) AS count ORDER BY count DESC RETURN e.name, count LIMIT 1"
"""

# M6:

# H1:

# H2:
