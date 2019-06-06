import os


def create_config(working_directory = './'):
    make_directory(working_directory + '.vuepress')
    template = open_file('templates/config.md')

    table_of_contents = create_table_of_contents(working_directory)
    template = template.replace('{table_of_contents}', table_of_contents)

    with open(working_directory + '.vuepress/config.js', 'w', encoding='utf8') as configjs:
        configjs.write(template)


def filter_files_for_vorlesungen_uebungen_zusammenfassungen(working_directory, modul):
    vorlesungen = []
    uebungen = []
    zusammenfassungen = []

    for week in get_directories(working_directory + modul):
        files = get_files(working_directory + modul + '/' + week)

        if 'vorlesung.md' in files:
            vorlesungen.append(f'/{modul}/{week}/vorlesung')

        if 'übung.md' in files:
            uebungen.append(f'/{modul}/{week}/übung')

        if 'zusammenfassung.md' in files:
            zusammenfassungen.append(f'/{modul}/{week}/zusammenfassung')

    return (vorlesungen, uebungen, zusammenfassungen)


def get_modules(path):
    return filter(is_not_templates, filter(is_not_vuepress, get_directories(path)))


def has_elements(list):
    return len(list) > 0


def create_table_of_contents(working_directory):
    tab = '  '
    table_of_contents = ''
    for modul in get_modules(working_directory):
        table_of_contents += f'{tab*3}"/{modul}/": [\n{tab*4}"/", /* semester-readme */\n{tab*4}"",  /* modul-readme */\n'

        (vorlesungen, uebungen, zusammenfassungen) = filter_files_for_vorlesungen_uebungen_zusammenfassungen(working_directory, modul)
        if has_elements(vorlesungen):
            table_of_contents += create_module_toc_string(tab, vorlesungen, 'Vorlesungen')

        if has_elements(uebungen):
            table_of_contents += create_module_toc_string(tab, uebungen, 'Übungen')

        if has_elements(zusammenfassungen):
            table_of_contents += create_module_toc_string(tab, zusammenfassungen, 'Zusammenfassungen')

        table_of_contents += f'{tab*3}],\n'

    table_of_contents += f'{tab*3}"/": [\n{tab*4}"",\n'
    for modul in get_modules(working_directory):
        table_of_contents += f'{tab*4}"{modul}/",\n'
    table_of_contents += f'{tab*3}]'

    return table_of_contents


def make_directory(path):
    if not directoryExists(path):
        os.mkdir(path)


def create_module_toc_string(tab, content, title):
    toc_string = f'{tab*4}' + '{' + f'\n{tab*5}title: "{title}",\n{tab*5}children: [\n'
    for file in content:
        toc_string += f'{tab*6}"{file}",\n'
    toc_string += f'{tab*5}]\n{tab*4}' + '},\n'
    return toc_string


def directoryExists(path):
    return os.path.isdir(path)


def open_file(path):
    with open(path, 'r', encoding='utf8') as template:
        return template.read()


def is_not_vuepress(directory):
    return directory != '.vuepress'


def is_not_templates(directory):
    return directory != 'templates'


def is_vorlesung_note(file):
    return file == 'vorlesung.md'


def is_uebung_note(file):
    return file == 'übung.md'


def is_zusammenfassung_note(file):
    return file == 'zusammenfassung.md'


def get_directories(path):
    directories = []
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
           directories.append(file)
    return directories


def get_files(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
           files.append(file)
    return files


if __name__ == "__main__":
    create_config()
