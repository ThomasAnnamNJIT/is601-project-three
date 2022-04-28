import csv
from typing import Dict


def read_csv(filename: str) -> Dict:

    songs = []

    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader, None)
        for row in reader:
            title, artist, year, genre = row
            songs.append({
                "title": title,
                "artist": artist,
                "year": year,
                "genre": genre
            })

    return songs
