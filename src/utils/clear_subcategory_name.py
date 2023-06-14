def clear_subcategory_name(subcategory_name):
    words = subcategory_name.split("(")
    return words[0].strip().replace(" ", "-")


result = clear_subcategory_name("Night creams (43534)")
print(result)


print(len(["asdf", "23423"]))