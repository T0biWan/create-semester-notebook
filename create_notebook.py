import json
import os
from shutil import copyfile
from functions import *
from create_config import create_config


if __name__ == "__main__":
    with open('semester-data.json', 'r', encoding='utf8') as file:
        semester_data = json.load(file)

    weeks = semester_weeks(semester_data)
    semester_directory = semester_data['target_directory'] + '/' + semester_data['semester_titel'] + '/'
    make_directory(semester_directory)

    semester_readme_file = create_semester_readme_file(semester_data)
    write_file(semester_directory + 'readme.md', semester_readme_file)

    for modul in semester_data['modules']:
        module_directory = semester_directory + modul['modul'] + '/'
        make_directory(module_directory)
        write_file(module_directory + 'readme.md', create_module_readme(semester_data, modul))

        for week in weeks:
            week_directory = module_directory + week + '/'
            make_directory(week_directory)
            create_note_files(week_directory, week, modul)

    make_directory(semester_directory + 'templates/')
    copyfile('templates/config.md', semester_directory + 'templates/config.md')
    copyfile('semester-data.json', semester_directory + 'semester-data.json')
    copyfile('create_config.py', semester_directory + 'create_config.py')
    create_config(semester_directory)
