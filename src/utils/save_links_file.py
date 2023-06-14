import os


def save_links_file(filename, category, data):
    # open file in write mode
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, '..', '..', 'product_links', category.lower())
    file_path = os.path.join(folder_path, filename + '.txt')

    if not os.path.exists(folder_path):
        # Crear la carpeta si no existe
        os.makedirs(folder_path)
        print(f'Folder {folder_path} created')

    with open(file_path, 'w') as fp:
        for item in data:
            # write each item on a new line
            fp.write("%s\n" % item)
        print(f'[SUCCESS] File {filename}.txt created')
