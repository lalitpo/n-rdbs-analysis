import redis
import json
import time

def update_progress(subject, progress):
    print(
        "\r{0} [{1}] {2}%".format(
            subject,
            ("#"*int(progress//2) + " "*int((102-progress)//2)),
            str(int(progress)).rjust(3)
        ),
        end=''
    )


def load_json(json_file: str):
    with open(json_file) as f:
        json_data = ",\n".join(f.readlines())
        data = json.loads(f"[{json_data}]")
        return data


def load_articles(r: redis.StrictRedis, json_file: str):
    """
    Load the journal articles into Redis. The articles are stored in a hash
    and the journal and author are stored in a set, referencing the article

    :param r: Redis connection
    :param json_file: Path to the json file
    """
    data = load_json(json_file)
    length = len(data)
    start = time.process_time()
    for i, article in enumerate(data):
        update_progress("Loading journal articles", (i/length)*100)
        r.execute_command(
            "HSET", f"journal_articles:{i}",
            "key", article["key"],
            "author", article["author"],
            "title", article["title"],
            "year", article["year"],
            "journal", article["journal"],
            "number", article["number"],
            "volume", article["volume"]
        )
        # Add the article to the journal
        r.sadd(f"journal:{article['journal']}:articles", f"journal_articles:{i}")
        # Add the article to the author
        authors = article["author"].split(",")
        for author in authors:
            r.sadd(f"author:{author.strip()}:articles", f"journal_articles:{i}")
        # Add the article to the year
        r.sadd(f"year:{article['year']}:articles", f"journal_articles:{i}")

    end = time.process_time()
    print(f"\nTime: {round(end-start, 2)}s")


def load_inproceedings(r: redis.StrictRedis, json_file: str):
    data = load_json(json_file)
    length = len(data)
    start = time.process_time()
    for i, inproceedings in enumerate(data):
        update_progress("Loading conference articles", (i/length)*100)
        r.execute_command(
            "HSET", f"conference_articles:{i}",
            "key", inproceedings["key"] if inproceedings["key"] is not None else "",
            "author", inproceedings["author"] if inproceedings["author"] is not None else "",
            "title", inproceedings["title"] if inproceedings["title"] is not None else "",
            "year", inproceedings["year"] if inproceedings["year"] is not None else "",
            "pages", inproceedings["pages"] if inproceedings["pages"] is not None else ""
        )
        # Add the article to the author
        authors = inproceedings["author"].split(",")
        for author in authors:
            r.sadd(f"author:{author.strip()}:inproceedings", f"conference_articles:{i}")

    end = time.process_time()
    print(f"\nTime: {round(end-start, 2)}s")


def load_proceedings(r: redis.StrictRedis, json_file: str):
    data = load_json(json_file)
    length = len(data)
    start = time.process_time()
    for i, proceedings in enumerate(data):
        update_progress("Loading proceedings", (i/length)*100)
        r.execute_command(
            "HSET", f"proceedings:{i}",
            "key", proceedings["key"] if proceedings["key"] is not None else "",
            "editor", proceedings["editor"] if proceedings["editor"] is not None else "",
            "title", proceedings["title"] if proceedings["title"] is not None else "",
            "publisher", proceedings["publisher"] if proceedings["publisher"] is not None else "",
            "year", proceedings["year"] if proceedings["year"] is not None else "",
            "volume", proceedings["volume"] if proceedings["volume"] is not None else ""
        )
        # Add the proceedings to the editor
        r.sadd(f"editor:{proceedings['editor']}:proceedings", f"proceedings:{i}")
        # Add the proceedings to the publisher
        r.sadd(f"publisher:{proceedings['publisher']}:proceedings", f"proceedings:{i}")
 
    end = time.process_time()
    print(f"\nTime: {round(end-start, 2)}s")


if __name__ == '__main__':
    # Connect to Redis
    r = redis.StrictRedis(host='localhost', port=1234, db=0)

    # DROP INDEX
    print("Dropping indexes...")
    start = time.process_time()
    try:
        r.execute_command("FT.DROPINDEX journal_articles DD")
        print("Dropped journal_articles")
        r.execute_command("FT.DROPINDEX conference_articles DD")
        print("Dropped conference_articles")
        r.execute_command("FT.DROPINDEX proceedings DD")
        print("Dropped proceedings")
    except:
        print("No more indexes to drop")
    finally:
        end = time.process_time()
        print(f"Indexes dropped in {round(end-start, 2)}s")

    input("Press enter to continue...")

    # Create the index
    article = "FT.CREATE journal_articles ON HASH PREFIX 1 article: SCHEMA key TEXT title TEXT author TEXT WEIGHT 5.0 year NUMERIC journal TEXT number NUMERIC volume NUMERIC"
    inproceedings = "FT.CREATE conference_articles ON HASH PREFIX 1 inproceedings: SCHEMA key TEXT author TEXT title TEXT WEIGHT 5.0 year NUMERIC pages TEXT"
    proceedings = "FT.CREATE proceedings ON HASH PREFIX 1 proceedings: SCHEMA key TEXT editor TEXT title TEXT WEIGHT 5.0 publisher TEXT year NUMERIC volume NUMERIC"

    r.execute_command(article)
    load_articles(r, "resources/journal_articles.json")
    r.execute_command(inproceedings)
    load_inproceedings(r, "resources/conference_articles.json")
    r.execute_command(proceedings)
    load_proceedings(r, "resources/conference_proceedings.json")


# Example resolution for query E2
# article_ids = r.sinter("journal:Theory of Computing Systems:articles", "author:Martin Gröhe:articles")
