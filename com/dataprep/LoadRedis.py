import redis
import json

def update_progress(subject, progress):
    print(
        "\r{0} [{1}] {2}%".format(
            subject,
            ("#"*(progress//5) + " "*((104-progress)//5)),
            str(progress).rjust(3)
        ),
        end=''
    )

def load_json(r, json_file, title="?"):
    with open(json_file) as f:
        data = json.load(f)
        length = len(data)
        for index, element in enumerate(data):
            update_progress(f"Loading {title}", int((index/length)*100))
            r.hmset(element['key'], element)
        print()

if __name__ == '__main__':
    # Connect to Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    load_json(r, "resources/article.json", "articles")
    load_json(r, "resources/inproceedings.json", "inproceedings")
    load_json(r, "resources/proceedings.json", "proceedings")
