# Usage
```bash
venv\Scripts\activate
pip install -e .
python -m main
```
# Note
Ошибку F401 при линтинге через `flake8` следует игнорировать, она некорректно указывает на импорты в файлах `__init__.py` модулей.
