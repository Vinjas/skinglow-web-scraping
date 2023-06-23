def clear_subcategory_name(subcategory_name):
    words = subcategory_name.split("(")
    return words[0].strip().replace(" ", "-")
