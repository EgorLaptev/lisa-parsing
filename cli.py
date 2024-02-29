import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from models.OpenModel import OpenModel


model = OpenModel()


def list_files(directory):
    files = os.listdir(directory)
    txt_files = [f for f in files if f.endswith('.txt')]
    return txt_files

def main():
    directory = 'docs/txt'
    files = list_files(directory)
    if not files:
        print("В директории нет .txt файлов.")
        return

    choices = [(filename, filename) for filename in files]

    result = radiolist_dialog(
        title="Выберите файл",
        text="Доступные файлы:",
        values=choices
    ).run()

    if result:
        selected_file = result
        model.send_file(f'docs/txt/{selected_file}')
        print(f"Выбран файл: {selected_file}")
    else:
        print("Файл не выбран")

if __name__ == "__main__":
    main()
