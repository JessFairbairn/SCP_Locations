import os

from functions import download_article, get_all_scp_links

# article_name = "scp-002"

# download_article(article_name)

urls = get_all_scp_links()


already_downloaded = os.listdir("/home/furby/Code/SCP_Locations/downloads/")
for url in urls:
    if url not in already_downloaded:
        download_article(url)