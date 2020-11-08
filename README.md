# Stack Exchange Scraper ![Python](https://img.shields.io/badge/python-v3.6+-blue.svg) ![version](https://img.shields.io/badge/version-1.0.0-green)

An easy and quick **python script** to extract data from question of the **stack exchange** network sites. Right now support question from **Stack Overflow**, **Ask Ubuntu** and **Mathematics Stack Exchange**.

## Motivation
This project born as part of the **Data Mining** project for **ITC Class of Fall 2020**.

## Installation

For now just **clone** the repo. If you want you can use the provided `requeriment.txt` file to set your virtual environment.

To set your virtual environment follow this commands from the project directory.

```bash
python -m venv your_venv
source your_venv/bin/activate
pip install -r requirements.txt
```

## Usage
You can set options using the main notation standards:

**-s --search** tag

**-w --where** website to parse 
* SO: stackoverflow (by default)
* MATH: math.stackexchange
* UBUNTU: ask.ubuntu

**-d --directory** save directory
```bash
python main.py -s python
python main.py -w MATH -s calculus
python main.py -w UBUNTU -s cloud -d c:/temp
```
## Contributing
Pull requests are welcome (especially from tutors). For major changes, please open an issue first to discuss what you would like to change.

## Team

[![regCode](https://avatars1.githubusercontent.com/u/18012903?s=460&u=b0300754272e701a5057c9b0c360fcd8fc51c0c1)](https://github.com/regCode)  | [![CyberMaryVer](https://avatars3.githubusercontent.com/u/66170525?s=40&v=7)](https://github.com/CyberMaryVer)
---|---
[David Frankenberg](https://github.com/regCode) | [Maria Startseva](https://github.com/CyberMaryVer)

## License
**Stack Exchange Scraper** is released under the [MIT License](http://www.opensource.org/licenses/MIT).
