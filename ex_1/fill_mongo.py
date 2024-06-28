import datetime
import json
import sys
from pathlib import Path

from mongoengine import connect
import configparser
from models import Author, Quote


def create_connection():
    config = configparser.ConfigParser()
    config.read('.env')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    # connect to cluster on AtlasDB with connection string

    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?\
retryWrites=true&w=majority&appName=Claster""", ssl=True)


def fill_authors(filename: Path):
    # create authors
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for a in json.loads(f.read()):
                author = Author(**a)
                author.born_date = datetime.datetime.strptime(author.born_date, "%B %d, %Y").date()
                db_authors = Author.objects(fullname=author.fullname)
                if len(db_authors) > 0:
                    db_authors.update(fullname=author.fullname, born_date=author.born_date,
                                      born_location=author.born_location,
                                      description=author.description)
                else:
                    author.save()
        return len(Author.objects())
    except FileNotFoundError:
        print("Something goes wrong. Check if file exist.")
    except Exception as e:
        print(e)


def fill_quotes(filename: Path):
    # create quotes
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for q in json.loads(f.read()):
                q["author"] = Author.objects(fullname=q.get("author"))[0].id
                quote = Quote(**q)
                db_quotes = Quote.objects(quote=quote.quote)
                if len(db_quotes) > 0:
                    db_quotes.update(author=quote.author, tags=quote.tags)
                else:
                    quote.save()
        return len(Quote.objects())
    except FileNotFoundError:
        print("Something goes wrong. Check if file exist.")
    except IndexError:
        print("Can not add quote. Check if author of quote exist in DB.")
    except Exception as e:
        print(e)


# script format  -----   python fill_mongo.py {file_name}
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = Path(sys.argv[1])
        filename = filename.absolute()
        match filename.name:
            case "authors.json":
                create_connection()
                print(f"{fill_authors(filename)} authors in DB")
            case "quotes.json":
                create_connection()
                print(f"{fill_quotes(filename)} quotes in DB")
            case _:
                print("filename should be 'authors.json' or 'quotes.json'")
