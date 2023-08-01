import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request

try:
    baseURL = 'https://www.imdb.com/search/title/?title_type=tv_series&sort=num_votes,desc'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    tvShowList = []
    for start in range(1, 5001, 50):
        url = f'{baseURL}&start={start}'
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        htmlContent = response.read()

        soup = BeautifulSoup(htmlContent, 'html.parser')

        tvShowData = soup.select('.lister-item.mode-advanced')
        for tvShow in tvShowData:
            titleElement = tvShow.select_one('.lister-item-header a')
            title = titleElement.text.strip()

            ratingElement = tvShow.select_one('.ratings-imdb-rating strong')
            rating = ratingElement.text.strip() if ratingElement else 'N/A'

            overviewElement = tvShow.select('.text-muted')
            overview = overviewElement[2].text.strip() if len(overviewElement) >= 2 else 'N/A'

            tvShowList.append({'Title': title, 'Rating': rating, 'Overview' : overview})
            print(title, '-', rating, '-', overview)

    df = pd.DataFrame(tvShowList)
    df.to_csv('imdbTVShows.csv', index=False)

except Exception as e:
    print(e)






