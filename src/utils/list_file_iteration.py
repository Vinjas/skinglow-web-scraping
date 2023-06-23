import os
import inquirer


def save_list_in_file(filename, item_list):
    # open file in write mode
    with open(rf'{filename}.txt', 'w') as fp:
        for item in item_list:
            # write each item on a new line
            fp.write("%s\n" % item)
        print(f'[SUCCESS] File {filename}.txt created')


def iterate_file_list(path):
    # open file and read the content in a list
    with open(path, 'r') as fp:
        names = []

        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names


def delete_line(file, line_to_delete):
    with open(file, 'r') as f:
        lines = f.readlines()

    lines = [line for line in lines if line.strip() != line_to_delete.strip()]

    with open(file, 'w') as f:
        f.writelines(lines)
