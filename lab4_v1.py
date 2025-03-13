import os
import csv
"Здесь будут изменения"
class Person:
    """
    Базовый класс, представляющий человека.
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name})"


class Student(Person):
    """
    Класс, представляющий студента. Наследуется от класса Person.
    """
    def __init__(self, id, name, email, group):
        super().__init__(name)
        self.id = id
        self.email = email
        self.group = group

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, email={self.email}, group={self.group})"

    def __setattr__(self, key, value):
        """
        Устанавливает значение атрибута через setattr.
        """
        super().__setattr__(key, value)

    @staticmethod
    def validate_email(email):
        """
        Статический метод для проверки корректности email.
        """
        return "@" in email and "." in email


class StudentCollection:
    """
    Класс для работы с коллекцией студентов.
    """
    def __init__(self, students=None):
        self.students = students if students is not None else []

    def __iter__(self):
        """
        Итератор для коллекции студентов.
        """
        return iter(self.students)

    def __getitem__(self, index):
        """
        Доступ к элементам коллекции по индексу.
        """
        return self.students[index]

    def __repr__(self):
        """
        Перегрузка метода repr для вывода коллекции.
        """
        return "\n".join(repr(student) for student in self.students)

    def add_student(self, student):
        """
        Добавляет студента в коллекцию.
        """
        self.students.append(student)

    def sort_by_name(self):
        """
        Сортирует студентов по имени.
        """
        self.students.sort(key=lambda x: x.name)

    def sort_by_id(self):
        """
        Сортирует студентов по ID.
        """
        self.students.sort(key=lambda x: x.id)

    def filter_by_id(self, min_id):
        """
        Фильтрует студентов по ID и возвращает новую коллекцию.
        """
        filtered_students = [student for student in self.students if student.id > min_id]
        return StudentCollection(filtered_students)

    @staticmethod
    def count_files_in_directory(directory):
        """
        Статический метод для подсчёта файлов в директории.
        """
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])


def read_csv(file_path):
    """
    Читает данные из CSV-файла и возвращает коллекцию студентов.
    """
    students = []
    encodings = ['utf-8-sig', 'windows-1251', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, newline='', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    student = Student(
                        id=int(row['№'].strip('"')),
                        name=row['ФИО'].strip('"'),
                        email=row['email'].strip('"'),
                        group=row['группа'].strip('"')
                    )
                    students.append(student)
                break
        except UnicodeDecodeError:
            continue
        except KeyError as e:
            print(f"Ошибка: Отсутствует ожидаемый столбец в CSV-файле: {e}")
            return []
        except ValueError as e:
            print(f"Ошибка: Некорректные данные в CSV-файле: {e}")
            return []

    return StudentCollection(students)


def save_to_csv(file_path, students):
    """
    Сохраняет коллекцию студентов в CSV-файл.
    """
    try:
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['№', 'ФИО', 'email', 'группа']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for student in students:
                writer.writerow({
                    '№': student.id,
                    'ФИО': student.name,
                    'email': student.email,
                    'группа': student.group
                })
        print(f'Данные успешно сохранены в файл {file_path}')
    except PermissionError:
        print("Ошибка: Нет прав на запись в файл. Закройте файл в других программах.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    # Шаг 1: Подсчет количества файлов в директории
    directory = input("Введите путь к директории: ")
    file_count = StudentCollection.count_files_in_directory(directory)
    print(f'Количество файлов в директории: {file_count}')

    # Шаг 2: Чтение данных из CSV-файла
    file_path = input("Введите путь к файлу data.csv: ")
    student_collection = read_csv(file_path)

    if not student_collection.students:
        print("Не удалось прочитать данные. Завершение программы.")
        exit()

    # Шаг 2.1: Сортировка по имени
    print("\nСортировка по ФИО:")
    student_collection.sort_by_name()
    print(student_collection)

    # Шаг 2.2: Сортировка по номеру (ID)
    print("\nСортировка по номеру (ID):")
    student_collection.sort_by_id()
    print(student_collection)

    # Шаг 2.3: Фильтрация по номеру (ID)
    age_limit = int(input("Введите минимальный номер для фильтрации: "))
    print("\nФильтр по номеру:")
    filtered_students = student_collection.filter_by_id(age_limit)
    for student in filtered_students:
        print(student)

    # Шаг 3: Сохранение отфильтрованных данных обратно в файл
    save_to_csv(file_path, filtered_students)
