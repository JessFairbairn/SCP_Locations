import os

from functions import download_article, get_all_scp_links

scp_root_urls = get_all_scp_links()


already_downloaded = os.listdir("C://Users/lip21jaf/Code/SCP_Locations/downloads")
num_scps_downloaded = len(list(filter(lambda file_name: "¦" not in file_name, already_downloaded)))

def process_article(article_url):
    if article_url not in already_downloaded:
        offset_links = download_article(article_url)
        already_downloaded.append(article_url)
        for link in offset_links:
            process_article(link)

# Beginning of action
print(f"{len(scp_root_urls)} SCPs in total; {num_scps_downloaded} already downloaded")
i = 0
for url in scp_root_urls:
    i += 1
    print(f"Processing SCP {i} of {len(scp_root_urls)}", end="\r")
    process_article(url)
