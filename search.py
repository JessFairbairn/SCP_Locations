import json, os, re

import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span

from geography import pick_location

SEARCH_PATH = "C:/Users/lip21jaf/Code/SCP_Locations/downloads/"

REGEX = re.compile('(?:[sS]ite[ -])(\d+[a-zA-Z]*)')

ENTITY_TYPES = ['GPE', 'LOC']

def main():
    nlp = spacy.load('en_core_web_trf')

    # sbd = nlp.create_pipe('sentencizer')
    nlp.add_pipe('sentencizer')

    site_dict: dict[str, list] = {}

    entries = pd.DataFrame(columns = ["site code", "site long name", "page name", "location name", "sentence"])

    pattern = [{"ENT_TYPE": {"IN": ENTITY_TYPES}}, {"ORTH": ","}, {"ENT_TYPE": {"IN": ENTITY_TYPES}}]
    pattern2 = [{"ENT_TYPE": {"IN": ENTITY_TYPES}}, {"ORTH": ","}, {"ENT_TYPE": {"IN": ENTITY_TYPES}}, {"ORTH": ","}, {"ENT_TYPE": {"IN": ENTITY_TYPES}}]
    TWO_PART_LOCATION_MATCHER = Matcher(nlp.vocab, validate=True)
    TWO_PART_LOCATION_MATCHER.add("CompoundLocation", [pattern])
    THREE_PART_LOCATION_MATCHER = Matcher(nlp.vocab, validate=True)
    THREE_PART_LOCATION_MATCHER.add("CompoundLocation", [pattern2])

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

                            filter(lambda ent: ent.label_ in ENTITY_TYPES, sent.ents)
                        )

                        sent_locations = _filter_location_list(sent_locations)


                        if not sent_locations:
                            continue
                        
                        
                        compound_matches = []
                        if len(sent_locations) > 1:
                            matches = TWO_PART_LOCATION_MATCHER(sent)
                            for match_id, start, end in matches:
                                # Create the matched span and assign the match_id as a label
                                span = Span(doc, start+sent.start, end+sent.start, label=match_id)
                                compound_matches.append(span)

                            matches = THREE_PART_LOCATION_MATCHER(sent)
                            if matches:
                                compound_matches = [] # three part matches will always override two part matches
                                for match_id, start, end in matches:
                                    # Create the matched span and assign the match_id as a label
                                    span = Span(doc, start+sent.start, end+sent.start, label=match_id)
                                    compound_matches.append(span)
                        
                        if compound_matches:
                            sent_locations = _filter_redundant_locations(compound_matches, sent_locations)
                            
                        # Pick best location
                        top_location_name = pick_location(
                            map(lambda ent: ent.text, sent_locations)
                        )

                        top_location = next(filter(lambda ent: ent.text == top_location_name, sent_locations))

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
                            "location name": top_location.text,
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
                    pd.DataFrame(site_sentences[0], index=[1])
                ], ignore_index=True)
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
        entries.sort_values(by=["site code"]).to_json("site_locations_partial.json", default_handler=str, orient="records")

def _filter_location_list(location_list: list[str]) -> list[str]:
    LOCATION_BLACKLIST = [
        "euclid", "earth", "oneiroi", "thaumiel", "anomaly", "scp", "site", "redacted", "anomalous", "d-", "goi-", "poi-", "oria", "lunar", "moon", "Sloth's Pit",
    ]

    for blacklisted_item in LOCATION_BLACKLIST:
        location_list = list(filter(lambda location: blacklisted_item not in location.text.lower() , location_list))

    return location_list

def _filter_redundant_locations(compound_matches: list[Span], sent_locations: list[Span]):
    for compound_span in compound_matches:
        sent_locations = list(filter(
            lambda span: span.start < compound_span.start or span.end > compound_span.end,
            sent_locations
        ))
    sent_locations = sent_locations + compound_matches
    return sent_locations

if __name__ == "__main__":
    main()
