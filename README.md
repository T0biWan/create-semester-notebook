# vuenotes

> create a notebook for the semester                                                                             |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need a current version of [_Python 3_](https://www.python.org/downloads/) and [_vuepress_](https://vuepress.vuejs.org/)

### Installing

After cloning the repository, you can fill out the needed informations for your upcoming semester in `semester-data.json`, you'll find a little example there already. Now run the following commands

```bash
# create your notebook
python create_notebook.py

# start a development server
vuepress dev
```

You might want to delete some files or week-folder while you are writing, just run the following command to update the table of contents

```bash
# create your notebook
python create_config.py
```

## Built With

-   [Vuepress](https://vuepress.vuejs.org/)

## Authors

-   **Tobias Klatt** - _Initial work_ - [GitHub](https://github.com/T0biWan/)

See also the list of [contributors](https://github.com/T0biWan/bachelor-frontend-prototype/graphs/contributors) who participated in this project.
