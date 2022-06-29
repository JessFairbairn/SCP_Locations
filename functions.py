from bs4 import BeautifulSoup
import requests

def get_all_scp_links() -> list[str]:
    url = f"https://scp-wiki.wikidot.com/system:page-tags/tag/scp"

    file = requests.get(url)
    file.raise_for_status()

    soup = BeautifulSoup(file.text, 'html.parser')
    wrapper = soup.find(id="tagged-pages-list")

    links = wrapper.find_all('a')
    return list(map(lambda link_tag: link_tag.attrs['href'][1:], links))

def download_article(article_name: str) -> None:
    url = f"https://scp-wiki.wikidot.com/{article_name}"

    file = requests.get(url)
    file.raise_for_status()

    soup = BeautifulSoup(file.text, 'html.parser')
    content = soup.find(id='page-content')

    with open(f'downloads/{article_name}', 'w') as mah_file:
        mah_file.write(content.text)
