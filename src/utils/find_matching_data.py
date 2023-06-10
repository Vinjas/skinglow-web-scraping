from src.constants import SKIN_TYPES_LIST, HIGHLIGHT_LIST

list_test = ['Hyaluronic Acid', 'Community Favorite', 'Plumping', 'Hydrating', 'Clean at Sephora', 'Good for: Dryness']


def find_matching_concerns(string, concerns_list):
    matching_concerns = []

    if '/' in string and ' / ' not in string:
        string = string.replace('/', ' / ')

    for concern in concerns_list:
        if any(word.lower() in string.lower() for word in concern.split('/')) or concern.lower() in string.lower():
            matching_concerns.append(concern)

    return matching_concerns


def find_matching_skin(string, skin_types_list):
    matching = []

    for concern in skin_types_list:
        if concern.lower() in string.lower():
            matching.append(concern)

    return matching


def find_matching_highlights(input_list, highlight_dict):
    result = {}
    for key, values in highlight_dict.items():
        matches = [element for element in input_list if element in values]
        if matches:
            result[key] = matches
    return result
