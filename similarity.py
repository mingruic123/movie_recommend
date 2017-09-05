from moviedata import dict

def jaccard_similarity(item1, item2):

    intersect = set(item1).intersection(item2)
    union     = set(item1).union(item2)

    if len(union) is 0:
        return 0
    else:
        jaccard_similarity = len(intersect) / len(union)
        return jaccard_similarity
