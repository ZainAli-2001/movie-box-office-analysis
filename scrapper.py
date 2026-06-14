import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from pathlib import Path

def extract_rows(table):
    data = []

    rows_data = table.find_all("tr")[1:]

    for row in rows_data:
        row_data = row.find_all("td")
        data.append([td.text.strip() for td in row_data])

    return data


def movie_scrapper():
    with requests.Session() as session:
        headers_request = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        url = 'https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/'

        try:
            response = session.get(
                url,
                headers=headers_request,
                timeout=10
            )
            response.raise_for_status()
        
            print("Connection established to Website")

            soup = BeautifulSoup(response.text, "html.parser")

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise

        print(f"Scraping first page")

        container = soup.find('div', class_ = 'a-section imdb-scroll-table-inner')
        if not container:
            raise Exception("Failed to find container on first page")

        table = container.find("table")
        if not table:
            raise Exception("Failed to find table on first page")

        all_data = []

        header_row = table.find("tr")
        headers = [th.text.strip() for th in header_row.find_all('th')]

        all_data.extend(extract_rows(table))


        for offset in range(200, 1000, 200):
            time.sleep(random.uniform(1, 3))

            print(f"Scraping page with offset {offset}")

            url = f"https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset={offset}"

            try:
                response = session.get(
                    url,
                    headers=headers_request,
                    timeout=10
                )        
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

            except requests.RequestException as e:
                print(f"Request failed: {e}")
                continue

            container = soup.find('div', class_ = 'a-section imdb-scroll-table-inner')
            if not container:
                print(f"[SKIP] No container found at offset {offset}")
                continue
            table = container.find("table")
            if not table:
                print(f"[SKIP] No table found at offset {offset}")        
                continue

            all_data.extend(extract_rows(table))
            

    df = pd.DataFrame(all_data, columns=headers)

    print("Scraping completed successfully!")
    print(f"Rows scraped: {len(all_data)}")
    print(df.shape)
    # print(df)

    BASE_DIR = Path(__file__).resolve().parent
    OUTPUT_DIR = BASE_DIR / "movie_dataset"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "top_grossing_movies.csv"

    df.to_csv(output_file, index=False)