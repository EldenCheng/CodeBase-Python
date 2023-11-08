import itertools

from data.constant import idcard_group_number, idcard_number


if __name__ == '__main__':

    idcard_every_group_number = int(idcard_number / idcard_group_number)
    with open("../data/chat_list.txt", "r") as text_file:
        for i in range(1, idcard_group_number + 1):
            for line in itertools.islice(text_file, 0, idcard_every_group_number):
                print(line)
    text_file.close()
