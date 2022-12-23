import os
import time
import glob
import logging
import prestodb
import redis

import random
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmarking")

QUERIES = [f"E{x}" for x in range(1, 3)] + [f"M{x}" for x in range(1, 7)] + [f"H{x}" for x in range(1, 3)] + [f"B{x}" for x in range(1, 3)]
RUN_AMOUNT = 30


def run_presto_test(query, conn):
    cur = conn.cursor()
    start_time = time.process_time()
    cur.execute(query)
    cur.fetchone()
    end_time = time.process_time()
    return end_time - start_time


def run_presto_benchmark():
    with open("com/queries/presto/allQueries.sql") as f:
        sql_scripts = f.read().split(";")

    logger.info("running %d sql scripts", len(sql_scripts))
    query_timings = {}
    presto_db_conn = prestodb.dbapi.connect(host='localhost',
                                            port=8080,
                                            user='lalit',
                                            catalog='postgres',
                                            schema='public')

    for _ in range(RUN_AMOUNT):
        for script_name, script in zip(QUERIES, sql_scripts):
            if script_name not in query_timings:
                query_timings[script_name] = []
            query_timings[script_name].append(run_presto_test(script, presto_db_conn))

    for script_name, timings in query_timings.items():
        logger.info(f"{script_name}: {sum(timings) / len(timings)}")

    plt.boxplot(query_timings.values())
    plt.xticks(range(1, len(query_timings) + 1), query_timings.keys(), rotation=90)
    plt.title("Query Latency (Presto, avg. over 30 runs)")
    plt.ylabel("Latency (s)")
    plt.xlabel("Query")
    plt.show()


def run_redis_test(query, conn):
    start_time = time.process_time()
    conn.execute_command("GRAPH.QUERY", "dblp", query)
    end_time = time.process_time()
    return end_time - start_time


def run_redis_benchmark():
    Q = [
        "MATCH (b:book {booktitle:'PODS'})<-[:published_in]-(c:conferences)-[:published_by]->(p:publisher) RETURN p.name",
        "MATCH (j:journal {journal: 'Theor. Comput. Sci.'})<-[:published_in]-(a:j_articles)-[:written_by]->(b:author {name:'Martin Grohe'}) RETURN a ORDER BY a.title ASC",
        "MATCH (:journal {journal: 'SIGMOID'})<-[:published_in]-(a:j_articles)-[:written_year]->(:author {year:2022}) RETURN COUNT(a)",
        "MATCH (y:year)<-[:published_year]-(a:j_articles) WITH MIN(y) AS min_year MATCH (y:year)<-[:published_year]-(a:j_articles)-[:published_in]->(j:journal) WHERE y = min_year RETURN COUNT(a), j.journal LIMIT 1",
        "MATCH (:journal {journal: 'CIDR'})<-[:published_in]-(a:j_articles)-[:written_year]->(y:year) WITH y.year AS year, COUNT(a) AS count RETURN year, count ORDER BY year ASC",
        "MATCH (:journal {journal: 'SIGMOID'})<-[:published_in]-(a:j_articles)-[:written_by]->(auth:author) WITH a, COUNT(auth) AS count ORDER BY count DESC WHERE count > 10 MATCH (a)-[:written_year]->(y:year) RETURN y.year, count LIMIT 1",
        "MATCH (:book {booktitle:'PODS'})<-[:published_in]-(a:conferences)-[:edited_by]->(e:editor) WITH e, COUNT(a) AS count ORDER BY count DESC RETURN e.name, count LIMIT 1",
        "MATCH (a:author)-[:written_by]->(j:j_articles) WITH a, COUNT(j) AS count ORDER BY count DESC LIMIT 1 MATCH (a)-[:written_by]->(j:j_articles)-[:published_in]->(c:conferences) RETURN COUNT(DISTINCT c) LIMIT 1",
        "MATCH (:journal {journal: 'ICDT'})<-[:published_in]-(a:j_articles)-[:written_year]->(:author {year:2020}) WITH a MATCH (a)-[:written_by]->(b:author) WITH b, COUNT(a) AS count ORDER BY count DESC LIMIT 1 MATCH (b)-[:written_by]->(j:j_articles)-[:written_by]->(c:author) RETURN c.name, COUNT(j) LIMIT 1",
        "MATCH (a:author {name:'Dan Suciu'})<-[:written_by]-(j:j_articles)-[:written_by]->(b:author) WITH b, COUNT(j) AS count ORDER BY count DESC LIMIT 1 MATCH (b)-[:written_by]->(j:j_articles)-[:written_by]->(c:author) RETURN c.name, COUNT(j) LIMIT 1",
    ]

    redis_db_conn = redis.Redis(host='localhost', port=1234, db=0)
    query_timings = {}
    for _ in range(RUN_AMOUNT):
        for q_name, query in zip(QUERIES[:-2], Q):
            if q_name not in query_timings:
                query_timings[q_name] = []
            query_timings[q_name].append(run_redis_test(query, redis_db_conn))

    for q_name, timings in query_timings.items():
        logger.info(f"{q_name}: {sum(timings) / len(timings)}")

    plt.boxplot(query_timings.values())
    plt.xticks(range(1, len(query_timings) + 1), query_timings.keys(), rotation=90)
    plt.title("Query Latency (Redis, avg. over 30 runs)")
    plt.ylabel("Latency (s)")
    plt.xlabel("Query")
    plt.show()

def main():
    # run_presto_benchmark()
    run_redis_benchmark()

if __name__ == "__main__":
    main()
