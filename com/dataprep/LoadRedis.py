import redis
import json
from redisgraph import Node, Edge, Graph, Path

r = redis.Redis(host='localhost', port=1234)

redis_graph = Graph('dblp', r)

# Use this to limit the number of records to load, set to -1 to load all
# I used this because the code fill my ram and crash my computer
LIMIT = -1


def update_progress(subject, progress, index, length):
    print(
        "\r{0} [{1}] {2}% {3}/{4}".format(
            subject,
            ("#"*int(progress//2) + "-"*int((100-progress)//2)),
            str(int(progress)).zfill(3),
            str(index).zfill(5),
            str(length).zfill(5)
        ),
        end=''
    )

node_dict = {}


def get_or_create_node(redis_graph, label, key, value):
    try:
        node = redis_graph.query(f"MATCH (y:{label} {key: '{value}'}) RETURN y")
    except:
        if label not in node_dict.keys():
            node_dict[label] = {}
        # Check if it exists in the dict
        if value in node_dict[label].keys():
            return node_dict[label][value]
        else:
            node = Node(label=label, properties={key: value})
            redis_graph.add_node(node)
            node_dict[label][value] = node

    return node

# Load conference articles
with open("resources/conference_articles.json") as conference_articles:
    for i, line in enumerate(conference_articles.readlines()[:LIMIT]):
        length = LIMIT
        conf_article = json.loads(line)
        article = Node(
            label='c_articles',
            properties={
                "key": conf_article["key"] if conf_article["key"] is not None else "",
                "title": conf_article["title"] if conf_article["title"] is not None else "",
                "booktitle": conf_article["booktitle"] if conf_article["booktitle"] is not None else "",
                "pages": conf_article["pages"] if conf_article["pages"] is not None else "",
            })
        redis_graph.add_node(article)

        if conf_article["year"] is not None:
            year_node = get_or_create_node(redis_graph, 'year', 'year', conf_article["year"])
            published_in = Edge(article, 'published_year', year_node)
            redis_graph.add_edge(published_in)

        if conf_article["booktitle"] is not None:
            book_node = get_or_create_node(redis_graph, 'book', 'booktitle', conf_article["booktitle"])
            published_in = Edge(article, 'published_in', book_node)
            redis_graph.add_edge(published_in)

        if conf_article["author"] is not None:
            authors = conf_article["author"].split(",")
            for author in authors:
                author = author.strip()
                author_node = get_or_create_node(redis_graph, 'author', 'name', author)
                written_by = Edge(article, 'written_by', author_node)
                redis_graph.add_edge(written_by)

        update_progress("Loading conference articles", (i/length)*100, i, length)
print()

# Load journal articles
with open("resources/journal_articles.json") as journal_articles:
    for i, line in enumerate(journal_articles.readlines()[:LIMIT]):
        length = LIMIT
        journal_article = json.loads(line)
        article = Node(
            label='j_articles',
            properties={
                "key": journal_article["key"] if journal_article["key"] is not None else "",
                "title": journal_article["title"] if journal_article["title"] is not None else "",
                "number": journal_article["number"] if journal_article["number"] is not None else "",
                "volume": journal_article["volume"] if journal_article["volume"] is not None else "",
            })
        redis_graph.add_node(article)

        if journal_article["year"] is not None:
            year_node = get_or_create_node(redis_graph, 'year', 'year', journal_article["year"])
            published_in = Edge(article, 'published_year', year_node)
            redis_graph.add_edge(published_in)

        if journal_article["journal"] is not None:
            journal_node = get_or_create_node(redis_graph, 'journal', 'journal', journal_article["journal"])
            published_in = Edge(article, 'published_in', journal_node)
            redis_graph.add_edge(published_in)

        if journal_article["author"] is not None:
            authors = journal_article["author"].split(",")
            for author in authors:
                author = author.strip()
                author_node = get_or_create_node(redis_graph, 'author', 'name', author)
                written_by = Edge(article, 'written_by', author_node)
                redis_graph.add_edge(written_by)

        update_progress("Loading journal articles", (i/length)*100, i, length)

print()

# Load conferences proceedings
with open("resources/conference_proceedings.json") as conferences:
    for i, line in enumerate(conferences.readlines()[:LIMIT]):
        length = LIMIT
        conference = json.loads(line)
        conf = Node(
            label='conferences',
            properties={
                "key": conference["key"] if conference["key"] is not None else "",
                "title": conference["title"] if conference["title"] is not None else "",
                "volume": conference["volume"] if conference["volume"] is not None else "",
            })
        redis_graph.add_node(conf)

        if conference["year"] is not None:
            year_node = get_or_create_node(redis_graph, 'year', 'year', conference["year"])
            published_in = Edge(conf, 'published_year', year_node)
            redis_graph.add_edge(published_in)

        if conference["editor"] is not None:
            editors = conference["editor"].split(",")
            for editor in editors:
                editor = editor.strip()
                editor_node = get_or_create_node(redis_graph, 'editor', 'name', editor)
                edited_by = Edge(conf, 'edited_by', editor_node)
                redis_graph.add_edge(edited_by)

        if conference["booktitle"] is not None:
            book_node = get_or_create_node(redis_graph, 'book', 'booktitle', conference["booktitle"])
            published_in = Edge(conf, 'published_in', book_node)
            redis_graph.add_edge(published_in)

        if conference["publisher"] is not None:
            publisher_node = get_or_create_node(redis_graph, 'publisher', 'name', conference["publisher"])
            published_by = Edge(conf, 'published_by', publisher_node)
            redis_graph.add_edge(published_by)

        update_progress("Loading conferences proceedings", (i/length)*100, i, length)

print()

redis_graph.commit()
