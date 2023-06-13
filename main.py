# Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re


def merge_lists(list1, list2):
    new_list = []
    for i in range(len(list2)):
        if list2[i] == '':
            new_list.append(list1[i])
        else:
            new_list.append((list2[i]))
    return new_list


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# 1. Выполните пункты 1-3 задания.

# 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.

for line in contacts_list:
    FIO = ' '.join(line[0:3]).strip().split(' ')
    FIO = FIO + [''] * (3 - len(FIO))
    line[:3] = FIO[:3]

    # 2. Привести все телефоны в формат +7(999)999-99-99.
    # Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.

    pattern = r"(\+7|8)\W*(\d{3})\W*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
    subs = r"+7(\2)\3-\4-\5"
    phones = re.sub(pattern, subs, line[5])
    result_phones = re.sub(r"\(*доб.\s*(\d{4})\)*", r"доб.\1", phones)
    line[5] = result_phones

# 3. Объединить все дублирующиеся записи о человеке в одну.

temp_list = []
merge_list = []
contacts_new = [contacts_list[0]]

for index in range(1, len(contacts_list)):
    line = contacts_list[index]
    id_list = [n for n, x in enumerate(contacts_list) if x[:2] == line[:2]]
    merge_list = [''] * len(line)
    for index_ in id_list:
        if index_ not in temp_list:
            merge_list = merge_lists(contacts_list[index_], merge_list)
            temp_list.append(index_)
    if ''.join(merge_list) != '':
        contacts_new.append(merge_list)


# 2. Сохраните получившиеся данные в другой файл.
# Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_new)
