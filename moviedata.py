import csv

dict = {}
def read_data():
    with open("data/movie_metadata.csv") as f:
        reader = csv.DictReader(f)
        id = 0
        for row in reader:
            title_original = row['movie_title'].strip()
            title_lowercase = row['movie_title'].strip().lower()
            director = [row['director_name'].strip()]
            actors = [row['actor_1_name'].strip(), row['actor_2_name'].strip(), row['actor_3_name'].strip()]
            country = [row['country'].strip()]
            type = row['genres'].strip().split("$")
            score = 5
            if row['imdb_score'] is not None:
                score = float(row['imdb_score'])
            id += 1
            dict[title_lowercase] = (director, actors, country, type, score, title_original, id)
