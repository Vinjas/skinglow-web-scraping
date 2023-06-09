import re


def parse_ingredients(text):
    parsed_ingredients_list = []

    if "Clean at Sephora" in text:
        clean_text = re.sub(r"Clean at Sephora.*", "", text)
    else:
        clean_text = text

    list_text = clean_text.split(".")
    clean_list_text = [item.strip() for item in list_text if item.strip() != ""]

    for elem in clean_list_text:
        stripped_elem = elem.strip()

        if stripped_elem.startswith("-"):
            parsed_result = stripped_elem.split("-")[1].split(":")[0].strip()
            parsed_ingredients_list.append(parsed_result.title())
        else:
            parsed_result = stripped_elem.split(", ")
            for result in parsed_result:
                parsed_ingredients_list.append(result.strip().title())

    return parsed_ingredients_list
