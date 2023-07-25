import json, os, re

import pandas as pd
import spacy

SEARCH_PATH = "C:/Users/lip21jaf/Code/SCP_Locations/downloads/"

REGEX = re.compile('(?:[sS]ite[ -])(\d+[a-zA-Z]*)')

def main():
    nlp = spacy.load('en_core_web_trf')

    # sbd = nlp.create_pipe('sentencizer')
    nlp.add_pipe('sentencizer')

    site_dict: dict[str, list] = {}

    entries = pd.DataFrame(columns = ["site code", "site long name", "page name", "location name", "sentence"])

    file_list = os.listdir(SEARCH_PATH)
    i = 0
    try:
        for fname in file_list:

            i+=1
            print(f"Scanning file {i} of {len(file_list)}", end='\r')
            sites_in_file = set()
            potential_entries = {}

            with open(SEARCH_PATH + fname, encoding="utf-8") as scp_file:
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

                            # if match[1] in site_locations:
                            #     site_locations[match[1]].append(sent_locations[0].text)
                            # else:
                            #     site_locations[match[1]] = [sent_locations[0].text]
                            new_row = {
                                "site code": match[1],
                                "site long name": match[0],
                                "page name": fname,
                                "location name": sent_locations[0],
                                "sentence": sent.text,
                            }
                            try:
                                potential_entries[new_row["site code"]].append(new_row)
                            except KeyError:
                                potential_entries[new_row["site code"]] = [new_row]

            for site_code, site_sentences in potential_entries.items():
                
                # if len(site_sentences) == 1:
                #     entries = entries.append(site_sentences[0], ignore_index=True)
                    
                # else:
                #     # TODO: loop through and save them all
                #     entries = entries.append(site_sentences[0], ignore_index=True)

                entries = pd.concat([
                    entries, 
                    pd.DataFrame(site_sentences[0])]
                )
            for site_name in sites_in_file:
                if site_name in site_dict:
                    site_dict[site_name].append(fname)
                else:
                    site_dict[site_name] = [fname]
    finally:
        print('-----------------------------------------------------')
        print(f'{len(site_dict)} sites found')
        # print(site_dict.keys())

        with open('site_stories_dict.json', 'w') as list_file:
            list_file.write(json.dumps(site_dict))

        # with open('site_locations_dict.json', 'w') as list_file:
        #     list_file.write(json.dumps(site_locations))
        entries.to_json("site_locations_partial.json", default_handler=str, orient="records")

def _filter_location_list(location_list: list[str]) -> list[str]:
    LOCATION_BLACKLIST = [
        "euclid", "earth", "oneiroi", "thaumiel", "anomaly", "scp", "site", "redacted", "anomalous", "d-", "goi-", "poi-", "oria", "lunar", "moon"
    ]

    for blacklisted_item in LOCATION_BLACKLIST:
        location_list = list(filter(lambda location: blacklisted_item not in location.text.lower() , location_list))

    return location_list

if __name__ == "__main__":
    main()
