from pymongo import MongoClient
import csv

#Створення підключення до локальної бази
conn = MongoClient(host='localhost', port=27017)

#Перевірка чи існує база Тест, якщо існує, то видаляється і створюється нова
if 'Test' in conn.list_database_names():
    conn.drop_database('Test')
database = conn['Test']

#Створення двох коллекцій, Project i Tasks
collection_p = database['Project']
collection_t = database['Tasks']

#Додавання типів даних до коллекцій
col_types_p = [str, str, str]
col_types_t = [int, str, str, str, str, str]

#Функція збору даних з csv в словник
def insert_from_csv(f_name, formats, collection_obj):
    with open(f'{f_name}', 'r') as f:
        csv_data = csv.reader(f, delimiter='|')
        headers = tuple(next(csv_data))
        for id_, row in enumerate(csv_data, start=1):
            row_typed = tuple(convert(value) for convert, value in zip(formats, row))
            dict_ = {"_id": id_}
            for head, body in zip(headers, row_typed):
                dict_[head] = body
            collection_obj.insert_one(dict_)
            dict_.clear()
        return id_

#Заповнення даними коллекції MongoDB з csv 
rows_inserted_p = insert_from_csv('Project.csv', col_types_p, collection_p)
rows_inserted_t = insert_from_csv('Tasks.csv', col_types_t, collection_t)

#Вивід проектів тільки з статусом Canceled
canceled_projects = set(x['Project'] for x in collection_t.find({"Status": "Canceled"}))
print('Projects with canceled tasks:', canceled_projects, sep='\n')

conn.close()

