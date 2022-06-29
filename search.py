import json, os, re

import spacy

SEARCH_PATH = "/home/furby/Code/SCP_Locations/downloads/"

REGEX = re.compile('(?:[sS]ite[ -])(\d+[a-zA-Z]*)')

def main():
    nlp = spacy.load('en_core_web_lg')

    # sbd = nlp.create_pipe('sentencizer')
    nlp.add_pipe('sentencizer')

    site_dict: dict[str, list] = {}

    site_locations: dict[str, list] = {}

    file_list = os.listdir(SEARCH_PATH)
    i = 0
    try:
        for fname in file_list:
            i+=1
            print(f"Scanning file {i} of {len(file_list)}", end='\r')
            sites_in_file = set()

            with open(SEARCH_PATH + fname) as scp_file:
                for line in scp_file.readlines():
                    if not REGEX.search(line):
                        continue
                    doc = nlp(line)
                    for sent in doc.sents:
                        match = REGEX.search(sent.text)
                        if match is None:
                            continue
                        sites_in_file.add(match[1])

                        sent_locations = list(

                            filter(lambda ent: ent.label_ == 'GPE' or ent.label_ == 'LOC', sent.ents)
                        )

                        sent_locations = _filter_location_list(sent_locations)


                        if sent_locations:
                            print(sent_locations)
                            print(sent)
                            # site_locations[match[1]] = sent_locations[0].text

                            # data to save: site name, page name, location name, sentence

                            if match[1] in site_locations:
                                site_locations[match[1]].append(sent_locations[0].text)
                            else:
                                site_locations[match[1]] = [sent_locations[0].text]

            for site_name in sites_in_file:
                if site_name in site_dict:
                    site_dict[site_name].append(fname)
                else:
                    site_dict[site_name] = [fname]
    finally:
        print(f'{len(site_dict)} sites found')
        # print(site_dict.keys())

        with open('site_stories_dict.json', 'w') as list_file:
            list_file.write(json.dumps(site_dict))

        with open('site_locations_dict.json', 'w') as list_file:
            list_file.write(json.dumps(site_locations))

def _filter_location_list(location_list: list[str]) -> list[str]:
    LOCATION_BLACKLIST = ["euclid", "earth", "oneiroi", "thaumiel", "anomaly", "scp", "site"]
    for blacklisted_item in LOCATION_BLACKLIST:
        location_list = list(filter(lambda location: blacklisted_item not in location.text.lower() , location_list))

    return location_list

if __name__ == "__main__":
    main()
