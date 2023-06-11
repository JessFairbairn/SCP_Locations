import os

from functions import download_article, get_all_scp_links

urls = get_all_scp_links()


urls = get_all_scp_links()

def process_article(article_url):
    if article_url not in already_downloaded:
        offset_links = download_article(article_url)
        already_downloaded.append(article_url)
        for link in offset_links:
            process_article(link)

already_downloaded = os.listdir("/home/furby/Code/SCP_Locations/downloads/")
for url in urls:
    process_article(url)
