import json
import numpy as np
import textwrap
import datetime


print("Program started")

with open('article.json', 'r') as f:
  articleData = json.load(f)

print("Article readed from Json")

insertQueries = []

initialInsert = """
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER SCHEMA public OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE IF NOT EXISTS public.journel_articles (
    key character varying,
    title character varying,
    year character varying,
    journal character varying,
    number character varying,
    volume character varying
);


ALTER TABLE public.journel_articles OWNER TO admin;
"""

insertQueries.append(initialInsert)


print("insert started",datetime.datetime.now())

for index, data in enumerate(articleData):
  insertJournalArticle = """
  INSERT INTO public.journel_articles (key, title, year, journal, number, volume) VALUES ('{key}', '{title}', '{year}', '{journal}', '{number}', '{volume}');
  """.format(key=data.get("key"), title=data.get("title").replace("'", ""), year=data.get("year"),
             journal=data.get("journal").replace("'", ""), number=data.get("number"), volume=data.get("volume"))
  insertQueries.append(textwrap.dedent(insertJournalArticle).replace("\n", ""))
  if index % 100000 == 0:
    print("data inserted each ->",index,datetime.datetime.now())


print("insert end",datetime.datetime.now())

endInsert = """
REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
"""

insertQueries.append(endInsert)

with open("list.txt", 'w') as file:
  file.write('\n'.join(insertQueries))

np.savetxt('articleInsert.sql', insertQueries,  fmt="%s")
print("succesfully saved",datetime.datetime.now())