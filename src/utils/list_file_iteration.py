

def save_list_in_file(filename, item_list):
    # open file in write mode
    with open(rf'{filename}.txt', 'w') as fp:
        for item in item_list:
            # write each item on a new line
            fp.write("%s\n" % item)
        print(f'[SUCCESS] File {filename}.txt created')


def iterate_file_list(filename):
    # open file and read the content in a list
    with open(rf'{filename}.txt', 'r') as fp:
        names = []

        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)
