# Stack Exchange Scraper ![Python](https://img.shields.io/badge/python-v3.6+-blue.svg) ![version](https://img.shields.io/badge/version-1.0.0-green)

An easy and quick **python script** to extract data from question of the 
[Stack Exchange](https://stackexchange.com/) network sites. Right now support question from 
[Stack Overflow](https://stackoverflow.com/), [Ask Ubuntu](https://askubuntu.com/) 
and [Mathematics Stack Exchange](https://math.stackexchange.com/).

## Motivation
This project born as part of the **Data Mining** project for **ITC Class of Fall 2020**. The [Stack Exchange](https://stackexchange.com/) 
family sites are a meeting point between people who have questions on a related topic and other users and experts who freely answer their questions. 
The voting system allows us to follow the most popular questions and answers and gives us an idea of the trending topics in a specialized communities.
In summary it's a rich source of information that is regularly updated, ideal for **scraping**.

## Installation

For now just **clone** the repo. If you want you can use the provided `requeriment.txt` file to set your virtual environment.

To set your virtual environment follow this commands from the project directory.

```bash
python -m venv your_venv
source your_venv/bin/activate
pip install -r requirements.txt
```

## Options

The program runs as a **command-line script**. Below you can see the list of available options. 
You can always go back to them using the `--help` flag.

```bash
python stack-scraper.py --help

usage: stack-scraper.py [-h] [-t TAG] [-w {SO,MATH,UBUNTU}] [-d DIRECTORY] [-b BEGIN] [-l LIMIT] [-v]

Performs a scraping on a web page of the Stack Exchange network saving the information of the questions in a csv file

optional arguments:
  -h, --help            show this help message and exit
  -t TAG, --tag TAG     the tag to specify the topic of the search. If it is not specified, it will search within the general FAQ
  -w {SO,MATH,UBUNTU}, --where {SO,MATH,UBUNTU}
                        the target website. -SO: https://stackoverflow.com -MATH: https://math.stackexchange.com -UBUNTU: https://askubuntu.com
  -d DIRECTORY, --directory DIRECTORY
                        the directory path where the results will be saved. If it does not exist, it will be created
  -b BEGIN, --begin BEGIN
                        the page number to start the search
  -l LIMIT, --limit LIMIT
                        the maximum number of questions to retrieve
  -v, --verbose         determines if the program execution is displayed by CLI
```

Aqui estan las opciones en mayor detalle:

- `-h --help` show help.
- `-t --tag` search tag. specify the topic of the search. If it is not specified, it will search within the general **FAQ**.
- `-w --where` website to parse 
    - **SO**: [Stack Exchange](https://stackexchange.com/) (by default)
    - **MATH**: [Mathematics Stack Exchange](https://math.stackexchange.com/).
    - **UBUNTU**: [Ask Ubuntu](https://askubuntu.com/) 
- `-d --directory` save directory 
- `-b --begin` the page number to start the search
- `-l --limit` the number of questions to retrieve
- `-v --verbose` if the program execution is displayed by CLI

## Usage

The `stack-scraper.py` command extract question and answers from the [FAQ](https://en.wikipedia.org/wiki/FAQ) list of one  the specified site. The usage is the following.

```bash
stack-scraper.py [-h] [-t TAG] [-w {SO,MATH,UBUNTU}] [-d DIRECTORY] [-b BEGIN] [-l LIMIT] [-v]
```

Some example executions:

```bash
python stack-scraper.py -t python
python stack-scraper.py -w MATH -t calculus
python stack-scraper.py -w UBUNTU -t cloud -d ~/temp
python stack-scraper.py -t sql -d ./temp -l 5000 -v
```
## Contributing
Pull requests are welcome (especially from tutors). For major changes, please open an issue first to discuss what you would like to change.

## Team

[![regCode](https://avatars1.githubusercontent.com/u/18012903?s=460&u=b0300754272e701a5057c9b0c360fcd8fc51c0c1)](https://github.com/regCode)  | [![CyberMaryVer](https://avatars3.githubusercontent.com/u/66170525?s=40&v=7)](https://github.com/CyberMaryVer)
---|---
[David Frankenberg](https://github.com/regCode) | [Maria Startseva](https://github.com/CyberMaryVer)

## License
**Stack Exchange Scraper** is released under the [MIT License](http://www.opensource.org/licenses/MIT).
