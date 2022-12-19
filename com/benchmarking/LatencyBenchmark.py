import os
import time
import glob
import logging

import random
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmarking")

RUN_AMOUNT = 30

def run_test(script_path):
    start_time = time.process_time()
    time.sleep(random.random() * 0.01)
    end_time = time.process_time()
    return end_time - start_time

def main():
    sql_scripts = sorted(glob.glob("com/queries/presto/*.sql"))
    logger.info("running %d sql scripts", len(sql_scripts))
    query_timings = {}

    for _ in range(RUN_AMOUNT):
        for script_path in sql_scripts:
            logger.info("running %s", script_path)
            query_name, _ = os.path.splitext(os.path.basename(script_path))
            if query_name not in query_timings:
                query_timings[query_name] = []
            query_timings[query_name].append(run_test(script_path))

    for query_name, timings in query_timings.items():
        logger.info(f"{query_name}: {sum(timings) / len(timings)}")

    plt.boxplot(query_timings.values())
    plt.xticks(range(1, len(query_timings) + 1), query_timings.keys(), rotation=90)
    plt.title("Query Latency (Presto, avg. over 30 runs)")
    plt.ylabel("Latency (s)")
    plt.xlabel("Query")
    plt.show()

if __name__ == "__main__":
    main()
