import re

from fill_mongo import create_connection
from models import Author, Quote
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def print_quotes(quotes):
    if type(quotes) == 'str':
        print(quotes)
    for q in quotes:
        print(f"Author:  {q.author.fullname}")
        print(f"Quote:  {q.quote}")


@cache
def get_quotes_by_name(value: str):
    regex = re.compile('^' + value.strip() + '[^ .]*')
    author = Author.objects(fullname=regex)
    if not author:
        return "Author not found"
    quotes = Quote.objects(author=author[0].id)
    return quotes


@cache
def get_quotes_by_tag(value: str):
    values = value.strip().split(", ")
    if len(values) > 1:
        quotes = Quote.objects(tags__in=values)
    else:
        regex = re.compile(values[0] + '[^ .]*')
        quotes = Quote.objects(tags=regex)
    if not quotes:
        return "No quotes for given tags"
    return quotes

def main():
    while True:
        raw_command = input("enter command: ")
        try:
            command, value = raw_command.split(":")
            match command:
                case "name":
                    print_quotes(get_quotes_by_name(value))
                case "tag":
                    print_quotes(get_quotes_by_tag(value))
                case _:
                    print("Wrong command. Try again")
        except ValueError:
            if raw_command == "exit":
                return
            print("Wrong command. Try again")


if __name__ == "__main__":
    create_connection()
    main()
