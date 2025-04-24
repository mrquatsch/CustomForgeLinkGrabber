import json

import requests

from Constants import *


def main():
    artist_search = '<artist name here>'
    lead_results = get_customforge_results(artist_search, 'lead')
    rhythm_results = get_customforge_results(artist_search, 'rhythm')
    print_results(lead_results)
    print_results(rhythm_results)

    # Get a list of links from our results
    lead_download_link_list = parse_download_links(lead_results)
    rhythm_download_link_list = parse_download_links(rhythm_results)
    
    # Merge our lists
    download_list = []
    download_list.extend(lead_download_link_list)
    download_list.extend(rhythm_download_link_list)

    # Convert our list
    download_list = convert_http_to_https(download_list)
    download_list = remove_odlc_items(download_list)
    download_list = fix_media_fire_links(download_list)

    # Remove dupes and sort
    download_link_set = list(set(download_list))
    download_link_set.sort()

    # Print output
    # print(f'Link list: {download_link_set}')
    print(f'{len(download_link_set)} unique links found')
    print(' '.join(download_link_set))

def urlify_search_term(search_term):
    return str(search_term).replace(' ', '%20')

def print_results(results):
    json_results = json.loads(results)
    songs = json_results['data']
    for song in songs:
        artist = song['artist']['name']
        album = song['album']
        title = song['title']
        download_link = song['file_pc_link']
        # download_link = song['file_mac_link']
        print(f'Artist: {artist}, Album: {album}, Title: {title}, Download Link: {download_link}')

def parse_download_links(results):
    try:
        json_results = json.loads(results)
        songs = json_results['data']
        download_link_list = []
        for song in songs:
            download_link = song['file_pc_link']
            # download_link = song['file_mac_link']
            download_link_list.append(download_link)
        return download_link_list
    except Exception as e:
        print(f'Error parsing JSON: {e}')
        return []

def convert_http_to_https(list_of_inks):
    new_list = []
    for link in list_of_inks:
        if 'http:' in str(link):
            updated_link = str(link).replace('http:', 'https:')
            new_list.append(updated_link)
        else:
            new_list.append(link)
    return new_list

def remove_odlc_items(list_of_links):
    new_list = []
    for link in list_of_links:
        if 'theriffrepeater.com' in link:
            # Skip links from theriffrepeater.com
            pass
        elif 'ubisoft.com' in link:
            # Skip links from ubisoft.com
            pass
        else:
            new_list.append(link)
    return new_list

def fix_media_fire_links(list_of_links):
    new_list = []
    for link in list_of_links:
        if 'www.mediafire.com' in link and '/file' in link:
            new_link = str(link).rstrip('/file')
            new_list.append(new_link)
        else:
            new_list.append(link)
    return new_list

def get_customforge_results(search_value, arrangement_type):
    search_value = urlify_search_term(search_value)
    base_url = CUSTOM_FORGE_BASE_URL
    search_key = CUSTOM_FORGE_SEARCH_KEY
    length_key = CUSTOM_FORGE_LENGTH_KEY
    length_value = CUSTOM_FORGE_LENGTH_VALUE
    arrangement_key = CUSTOM_FORGE_ARRANGEMENT_KEY
    misc = CUSTOM_FORGE_REQUESTED_COLUMNS
    delimiter = '&'
    equals_sign = '='
    search_url = base_url + search_key + equals_sign + search_value + delimiter + \
                length_key + equals_sign + length_value + delimiter + \
                arrangement_key + equals_sign + arrangement_type + delimiter + \
                misc

    # Do NOT use zipped encoding or the response will be compressed and unreadable
    headers = {
        REQUEST_HEADER_USER_AGENT: REQUEST_HEADER_USER_AGENT_VALUE,
        REQUEST_HEADER_ACCEPT: REQUEST_HEADER_ACCEPT_VALUE,
        REQUEST_HEADER_ACCEPT_LANGUAGE: REQUEST_HEADER_ACCEPT_VALUE,
        REQUEST_HEADER_REFERER: REQUEST_HEADER_REFERER_VALUE,
        REQUEST_HEADER_CSRF_TOKEN: '<csrf token here>',  # Replace with your actual CSRF token
        REQUEST_HEADER_X_REQUESTED_WITH: REQUEST_HEADER_X_REQUESTED_WITH_VALUE,
        REQUEST_HEADER_CONNECTION: REQUEST_HEADER_CONNECTION_VALUE,
        REQUEST_HEADER_COOKIE: '<cookie here>',  # Replace with your actual cookie
    }

    print('Searching for ' + arrangement_type + ' tracks...')
    response = requests.get(search_url, headers=headers, data={})

    print('Response code: ' + str(response.status_code))
    return response.content


if __name__ == '__main__':
    main()
