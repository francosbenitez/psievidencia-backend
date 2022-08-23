import requests

req = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vS95wGgZlEivufodGteKLOxDzeC1dCCae38NCYiQZ7xIWSKnXMUc0-kionSL_BBRNO4xdrqAe1VDQ-P/pub?output=csv"
)
url_content = req.content
csv_file = open("psychologists.csv", "wb")

csv_file.write(url_content)
csv_file.close()
