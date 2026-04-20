# wu-parabank-rpa.py

Šis RPA robotas skirtas automatizuoti ParaBank veiksmus su vartotojų duomenimis iš CSV failo.
Projektas parašytas su `Python`, o visos naudojamos bibliotekos yra nurodytos `requirements.txt`.

## Ką daro robotas

- Nuskaito vartotojų duomenis iš CSV failo
- Užregistruoja vartotoją
- Atidaro naują sąskaitą
- Pateikia paskolos užklausą
- Sugeneruoja ataskaitą (`xlsx` arba `csv`)

## Priklausomybės (`requirements.txt`)

- `certifi==2026.2.25`
- `charset-normalizer==3.4.7`
- `et_xmlfile==2.0.0`
- `greenlet==3.4.0`
- `idna==3.11`
- `numpy==2.4.4`
- `openpyxl==3.1.5`
- `pandas==3.0.2`
- `playwright==1.58.0`
- `pyee==13.0.1`
- `python-dateutil==2.9.0.post0`
- `requests==2.33.1`
- `six==1.17.0`
- `typing_extensions==4.15.0`
- `tzdata==2026.1`
- `urllib3==2.6.3`

## Paleidimas

### Windows

1. Paleisk `install_windows.bat`
2. Po sėkmingos instaliacijos paleisk `run_windows.bat`

### macOS

1. Paleisk `install_mac.command`
2. Po sėkmingos instaliacijos paleisk `run_mac.command`

`install` skriptas automatiškai paruošia virtualią aplinką (`venv`) ir įrašo priklausomybes.
Po to `run` skriptas paleidžia robotą.

## Paleidimas per terminala su venv

Jei nori paleisti projekta rankiniu budu per terminala, naudok zemiau esancius zingsnius

### Windows (`PowerShell`)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\main\main.py
```

### macOS (`zsh` arba `bash`)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main/main.py
```

## Nustatymai

Paleidimo metu robotas leidžia pasirinkti režimą:

- `default` – naudojami numatytieji nustatymai
- `custom` – gali ranka pasirinkti norimus roboto nustatymus
