import re
from urllib.parse import urlparse

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


OFFSET_REGEX = re.compile(r"offset\/\d+")

def download_article(article_name: str) -> list[int]:
    """Downloads article, returns list of offset articles linked"""
    if "scp-wiki.wikidot.net" in article_name:
        article_name = urlparse(article_name).path

    url = f"https://scp-wiki.wikidot.com/{article_name.replace('¦', '/')}"

    file = requests.get(url)
    try:
        file.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            print(ex)
            return []
        else:
            raise

    soup = BeautifulSoup(file.text, 'html.parser')
    content = soup.find(id='page-content')

    with open(f'downloads/{article_name}', 'w', encoding="utf-8") as mah_file:
        mah_file.write(content.text)
    offset_links = content.find_all("a", href=OFFSET_REGEX)
    return list(map(
        lambda link_tag: _clean_internal_link(link_tag.attrs['href']),
        offset_links
    ))

def _clean_internal_link(url: str) -> str:
    if url.startswith("http"):
        url = urlparse(url).path[1:]
    elif url.startswith("/"):
        url=url[1:]
    return url.replace('/','¦')