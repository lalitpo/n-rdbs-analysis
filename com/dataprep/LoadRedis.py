import redis
import json

def update_progress(subject, progress):
    print(
        "\r{0} [{1}] {2}%".format(
            subject,
            ("#"*int(progress//2) + " "*int((102-progress)//2)),
            str(round(progress, 2)).rjust(6)
        ),
        end=''
    )


def load_json(json_file: str):
    with open(json_file) as f:
        data = json.load(f)
        return data


def load_articles(r: redis.StrictRedis, json_file: str):
    data = load_json(json_file)
    length = len(data)
    for i, article in enumerate(data):
        update_progress("Loading articles", (i/length)*100)
        r.execute_command("HSET", f"article:{i}", "key", article["key"], "title", article["title"], "year", article["year"], "journal", article["journal"], "number", article["number"], "volume", article["volume"])
    print()


def load_inproceedings(r: redis.StrictRedis, json_file: str):
    data = load_json(json_file)
    length = len(data)
    for i, inproceedings in enumerate(data):
        update_progress("Loading inproceedings", (i/length)*100)
        r.execute_command("HSET", f"inproceedings:{i}", "key", inproceedings["key"], "author", inproceedings["author"], "title", inproceedings["title"], "year", inproceedings["year"], "pages", inproceedings["pages"])
    print()


def load_proceedings(r: redis.StrictRedis, json_file: str):
    data = load_json(json_file)
    length = len(data)
    for i, proceedings in enumerate(data):
        update_progress("Loading proceedings", (i/length)*100)
        r.execute_command("HSET", f"proceedings:{i}", "key", proceedings["key"], "editor", proceedings["editor"], "title", proceedings["title"], "publisher", proceedings["publisher"], "year", proceedings["year"], "volume", proceedings["volume"])
    print()


if __name__ == '__main__':
    # Connect to Redis
    r = redis.StrictRedis(host='localhost', port=1234, db=0)

    # DROP INDEX
    try:
        r.execute_command("FT.DROPINDEX articles DD")
        r.execute_command("FT.DROPINDEX inproceedings DD")
        r.execute_command("FT.DROPINDEX proceedings DD")
    except:
        pass

    # Create the index
    article = "FT.CREATE articles ON HASH PREFIX 1 article: SCHEMA key TEXT title TEXT WEIGHT 5.0 year NUMERIC journal TEXT number NUMERIC volume NUMERIC"
    inproceedings = "FT.CREATE inproceedings ON HASH PREFIX 1 inproceedings: SCHEMA key TEXT author TEXT title TEXT WEIGHT 5.0 year NUMERIC pages TEXT"
    proceedings = "FT.CREATE proceedings ON HASH PREFIX 1 proceedings: SCHEMA key TEXT editor TEXT title TEXT WEIGHT 5.0 publisher TEXT year NUMERIC volume NUMERIC"

    r.execute_command(article)
    load_articles(r, "resources/article.json")
    r.execute_command(inproceedings)
    load_inproceedings(r, "resources/inproceedings.json")
    r.execute_command(proceedings)
    load_proceedings(r, "resources/proceedings.json")
