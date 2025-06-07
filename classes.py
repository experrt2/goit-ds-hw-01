from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    # def __init__(self, value):
    #     # Logic
    #     super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not value.isdigit():
            raise ValueError

        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # datetime.strptime(value, "DD.MM.YYYY")
            value = datetime.strptime(value, "%d.%m.%Y").strftime('%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_str: str):
        phone = Phone(phone_str)
        self.phones.append(phone)

    def find_phone(self, phone_str: str):
        for i in self.phones:
            if i.value == phone_str:
                return i

        return None


    def remove_phone(self, phone: str):
        # self.phones = [p for p in self.phones if p.value != phone]
        self.phones.remove (self.find_phone(phone))


    def edit_phone(self, current_phone, new_phone):
        if self.find_phone(current_phone) is None:
            raise ValueError

        # Validation
        Phone(new_phone)

        self.remove_phone(current_phone)
        self.add_phone(new_phone)

    def add_birthday(self, value: str):
        self.birthday = Birthday(value)

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday is not None:
            result += f" Contact birthday: {self.birthday.value}"
        return result

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name)

    def __str__(self):
        result = ""
        for key, record in self.data.items():
            result += str(record) + '\n'

        return result

    def adjust_for_weekend(self, birthday: datetime):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_object = datetime.strptime(record.birthday.value, "%d.%m.%Y")

            birthday_this_year = birthday_object.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=(today.year + 1))

            if today <= birthday_this_year <= (today + timedelta(days)):
                upcoming_birthdays.append(
                    {"name": record.name.value, "congratulation_date": self.adjust_for_weekend(birthday_this_year).strftime('%d.%m.%Y')})

        return upcoming_birthdays

