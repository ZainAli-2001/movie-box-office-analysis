# Movie Box Office Analysis

Scraped data on the top 1,000 highest-grossing movies of all time from [Box Office Mojo](https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/), then cleaned and explored it to uncover trends in worldwide box office performance.

## Project Structure

```
movie-box-office-analysis/
├── scrapper.py          # Scrapes box office data from Box Office Mojo
├── EDA.ipynb            # Data cleaning, preprocessing, and exploratory analysis
└── movie_dataset/
    └── top_grossing_movies.csv   # Scraped raw dataset
```

## Data Collection

`scrapper.py` uses `requests` and `BeautifulSoup` to pull the lifetime gross table from Box Office Mojo across multiple paginated pages (offsets 0–1000), parses each table into rows, and combines everything into a single Pandas DataFrame. The result is saved to `output/top_grossing_movies.csv`.

To run the scraper:

```python
from scrapper import movie_scrapper
movie_scrapper()
```

## Data Cleaning & Preprocessing

Performed in `EDA.ipynb`:

- Normalized column names (lowercase, underscores, removed special characters)
- Checked for duplicates and inconsistent data types
- Cleaned currency columns (`worldwide_lifetime_gross`, `domestic_lifetime_gross`, `foreign_lifetime_gross`) by removing `$` and `,`, and replacing `-` placeholders with `0`
- Cleaned percentage columns (`domestic_percent`, `foreign_percent`) by removing `%` and handling `<0.1` and `-` placeholders
- Converted cleaned columns to numeric types

## Exploratory Data Analysis

Key analyses included:

- **Top domestic vs. foreign performers** – bar charts comparing the top 10 movies by domestic and foreign lifetime gross
- **Foreign-to-domestic ratio** – identifying movies that performed disproportionately better internationally
- **Yearly trends** – average worldwide gross and movie count per year, plus total domestic vs. foreign revenue by year
- **All-time blockbusters** – movies in the top 5th percentile of worldwide gross
- **Highest-grossing movie per year** – tracking the top film for each year across the dataset

## Tech Stack

- Python
- Requests & BeautifulSoup (web scraping)
- Pandas & NumPy (data processing)
- Matplotlib & Seaborn (visualization)
- Jupyter Notebook

## Getting Started

1. Clone the repo
2. Install dependencies:
   ```
   pip install requests beautifulsoup4 pandas numpy matplotlib seaborn
   ```
3. Run `EDA.ipynb` to scrape the data and reproduce the analysis
