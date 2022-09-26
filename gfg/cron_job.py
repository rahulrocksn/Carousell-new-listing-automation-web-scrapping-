import scrape
import os

file = open(os.path.dirname(__file__) + "/search.txt", "r")
search_str = file.read().split(",")
file.close()

scrape.send_request(
    search_str[0], int(search_str[1]), int(search_str[2]), search_str[3]
)
