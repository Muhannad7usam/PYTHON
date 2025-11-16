# World Data Explorer 

World Data Explorer is a small Flask web app that lets you play with **real-world live data**:

- Global **COVID-19** time-series
- **Foreign exchange** rates
- **News** for any topic
- **Country** information (population, area, currencies…)
- **Weather** for any location
---

## 1. Tech Stack

- **Backend:** Python 3.13 + Flask
- **Charts:** matplotlib (rendered to PNG + embedded as Base64)
- **Data handling:** requests, pandas (for some exports)
- **Tests:** pytest
- **Exports:** CSV (and optional Excel) files written to (exports/)

---

## 2. Project Structure

This is the structure of the folder you’ll submit / clone:

```text
World-Data-Explorer/
│
├─ app/
│  ├─ __init__.py          # Flask app setup (creates the app object)
│  ├─ covid.py             # COVID data logic + charts + CSV export
│  ├─ exchange.py          # FX data logic + charts + CSV export
│  ├─ news.py              # NewsAPI logic + charts + CSV export
│  ├─ restcountries.py     # Country data logic + charts + CSV/Excel export
│  └─ weather.py           # Weather data logic + charts + CSV export
│
├─ exports/                # All generated CSV / Excel files are stored here
│
├─ templates/
│  ├─ index.html           # Home page
│  ├─ covid.html           # COVID page
│  ├─ exchange.html        # Exchange page
│  ├─ news.html            # News page
│  ├─ restcountries.html   # Country page
│  └─ weather.html         # Weather page
│
├─ tests/
│  ├─ test_covid.py
│  ├─ test_exchange.py
│  ├─ test_news.py
│  ├─ test_restcountries.py
│  └─ test_weather.py
│
├─ .env                    # Local environment variables (API keys etc.)
├─ .gitignore
├─ README.md               # You are reading this file 👍👍👍
├─ requirements.txt        # All Python dependencies
├─ routes.py               # Flask routes / views, connecting pages to logic
└─ run.py                  # Application entry point

# Inside the World-Data-Explorer folder
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt

How to run the project

Open a terminal in the World-Data-Explorer folder.

Activate your virtual environment (if you created one).

Run the Flask app using run.py:

python run.py