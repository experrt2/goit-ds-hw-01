import pickle
import sys

from classes import Phone, Birthday, Record, AddressBook

def parse_input(user_input):
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter user name and 10 digit phone please"
        except KeyError:
            return "Name does not exist in contacts"
        except IndexError:
            return "Enter user name please"

    return inner

@input_error
def add_birthday(args, book: AddressBook):
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    record.add_birthday(birthday)
    return f"Birthday {birthday} added for user {name}"

@input_error
def show_birthday(args, book):
    record = book.find(args[0])
    if record.birthday is None:
        return "Birthday not found"
    return record.birthday.value

@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def show_phone(args, book: AddressBook):
    record = book.find(args[0])
    result = ''
    for number in record.phones:
        result+= str(number) + " "
    return result

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "Name does not exist in contacts"
    record.edit_phone(old_phone, new_phone)
    return f"Phone changed to {new_phone} for user {name}"

def show_all(book: AddressBook):
    return str(book)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    # except EOFError:
    #     return print('File is empty')

def main():
    book = load_data()
    # book = AddressBook()
    # add_contact(['Bohdan', '1234567890'], book)
    # save_data(book)
    # print(book)
    # sys.exit(123)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

    save_data(book)

if __name__ == "__main__":
    main()
