from flask import render_template
from collections import OrderedDict
from difflib import SequenceMatcher

import operator
import similarity
import moviedata as m


"""Function to recommend movies to an user after the user reviews a movie"""
def user_recommendation(name, review):
    title_lower = name.lower()
    if title_lower not in m.dict:
        similar_title = similar_movie_title(title_lower)
        return (render_template("similartitle.html", name=name, similar_title=similar_title ), False)
    sim = similarity_matrix(name)

    #if review is 5 (best), recommend top 10 movies that are most similar
    if review == '5':
        sorted_sim = sorted(sim.items(), key=operator.itemgetter(1), reverse=True)
        all_top = top_movies(sorted_sim)
        return (all_top, True)

    #if review is 1 (worst), recommend a list of movies that are least similar with {imdb > 8}
    if review == '1':
        sorted_sim = sorted(sim.items(), key=operator.itemgetter(1), reverse=False)
        all_top = top_movies(sorted_sim, good=False)
        all_top_least_same = dict((k, v) for (k,v) in all_top.items() if v['sim'] == 0 and int(v['imdb']) >= 8.0)
        return (all_top_least_same, True)

"""Function to return similar movies for an user when the user submit a search request via HTML form"""
def similar_movies(name, number):
    title_lower = name.lower()
    if title_lower not in m.dict:
        similar_title = similar_movie_title(title_lower)
        return (render_template("similartitle.html", name=name, similar_title=similar_title), False)
    sim = similarity_matrix(name)
    sorted_sim = sorted(sim.items(), key=operator.itemgetter(1), reverse=True)
    all_top = top_movies(sorted_sim, number)
    return (all_top, True)

def auto_suggest(name):
    title_lower = name.lower()
    if title_lower not in m.dict:
        similar_title = similar_movie_title(title_lower)
        return (render_template("similartitle.html", name=name, similar_title=similar_title), False)

"""Return top N(default is 10) movies on the sorted dictionary by similarity"""
def top_movies(sorted_sim, n=10, good=True):
    all_top = OrderedDict()
    if good == True:
        for tuple in sorted_sim[:n]:
            top = OrderedDict()
            top['title'] = tuple[0]
            top['sim'] = tuple[1]
            top['director'] = m.dict[tuple[0].lower()][0]
            top['actors'] = m.dict[tuple[0].lower()][1]
            top['country'] = m.dict[tuple[0].lower()][2]
            top['type'] = m.dict[tuple[0].lower()][3]
            id = m.dict[tuple[0].lower()][6]
            all_top[id] = top

    else:
        for tuple in sorted_sim:
            top = OrderedDict()
            top['title'] = tuple[0]
            top['sim'] = tuple[1]
            top['director'] = m.dict[tuple[0].lower()][0]
            top['actors'] = m.dict[tuple[0].lower()][1]
            top['country'] = m.dict[tuple[0].lower()][2]
            top['type'] = m.dict[tuple[0].lower()][3]
            top['imdb'] = m.dict[tuple[0].lower()][4]
            id = m.dict[tuple[0].lower()][6]
            all_top[id] = top
    return all_top

"""Create a dictionary of {movie: score} pairs"""
def similarity_matrix(name):
    name=name.lower()
    values = {}
    for other in m.dict:
        if name == other:
            continue
        else:
            sim = combined_similarity(m.dict[name], m.dict[other])
            title_original = m.dict[other][5]
            values[title_original] = sim
    return values

"""Calculate the combined similarity between two movies. Weights can be adjusted to focus on one category"""
def combined_similarity(query, other):
    director_weight = 1
    actor_weight = 1
    country_weight = 1
    type_weight = 1

    director_score = director_weight * similarity.jaccard_similarity(query[0], other[0])
    actor_score = actor_weight * similarity.jaccard_similarity(query[1], other[1])
    country_score = country_weight * similarity.jaccard_similarity(query[2], other[2])
    type_score = type_weight * similarity.jaccard_similarity(query[3], other[3])

    sum = director_score + actor_score + country_score + type_score
    return sum

"""If the movie title is not found, return the most similar title in the database"""
def similar_movie_title(query):
    title_sim = {}
    for title in m.dict:
        sim = SequenceMatcher(None, query, title).ratio()
        title_sim[title] = sim
    max = 0
    most_similar_title = ""
    for key in title_sim:
        if(max < title_sim[key]):
            most_similar_title = m.dict[key][5]
            max = title_sim[key]
    return most_similar_title
