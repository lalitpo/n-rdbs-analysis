# Who is the publisher of PODS conference proceedings ?
E1 = """
FT.SEARCH proceedings "@booktitle:'PODS'"
"""

# What are the titles of the articles that Martin Gröhe wrote in the Theory of Computing Systems journal? (Sort in alphabetic order)
E2 = """
FT.SEARCH journal_articles "@author:'Grohe' @journal:(Theor* Comput* Sys*)" RETURN 1 title SORTBY title
"""

# How many articles were published in the SIGMOD conference proceedings this year?
M1 = """
FT.SEARCH c_article "@booktitle:'SIGMOD' @year:2022" RETURN 1 key
"""

# M2: How many articles were published in the oldest journal, and what is its title?
# This uses lua scripting at an atomic level
M2 = """
-- Get the minimum year
local min_year = redis.call("ZRANGEBYSCORE", "year:articles", "-inf", "+inf", "LIMIT", 0, 1)
min_year = tonumber(min_year[1])

-- Get the set of articles with the minimum year
local articles_set = "year:" .. min_year .. ":articles"
local articles = redis.call("SMEMBERS", articles_set)

-- Get the titles of the articles
local titles = {}
for i = 1, #articles do
  local title = redis.call("HGET", "journal_articles", articles[i], "title")
  table.insert(titles, title)
end

-- Return the count of articles and the titles
return { #articles, titles }
"""
