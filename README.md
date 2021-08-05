# arknights-desktop-wallpapers
[live app](https://arknights-desktop-wallpapers.herokuapp.com/)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights desktop wallpapers on the fly.
The art was scraped from [Gamepress](https://gamepress.gg/arknights/tools/interactive-operator-list) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The background colours are chosen dynamically by analysing the art and detecting the most dominant colour.