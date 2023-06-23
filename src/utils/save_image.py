import requests
import os


def save_image(url, filename, category, subcategory):
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, '..', '..', 'product_images', category.lower(), subcategory.lower())
    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Folder {folder_path} created')

    headers = {
        'Accept-Language': 'en-US,en',
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Authority': 'www.google.com',
        'User-Agent': 'SomeAgent',
        'Upgrade-Insecure-Requests': '1',
    }

    response = requests.get(url.split("?")[0], headers=headers)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"[SUCCESS] Image {filename} downloaded")
    else:
        print(f"[ERROR] Cannot download {filename}")
