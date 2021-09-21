# Kriptografi Tucil 3

## Installing Requirements
### Linux
```bash
virtualenv -p python3 venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows
```bash
virtualenv -p python3 venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Running Program
### Linux
```bash
source venv/bin/activate
python main.py
```

### Windows
```bash
venv\Scripts\activate
python main.py
```

## Building Exe
```bash
pyinstaller -F main.py --clean -w
```
