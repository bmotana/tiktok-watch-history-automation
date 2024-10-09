import requests
import json
import os
from urllib.parse import urlparse, parse_qs

def resolve_shortlink(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def download_tiktok_images(url):
    # Resolve the shortened URL
    full_url = resolve_shortlink(url)
    print(f"Resolved URL: {full_url}")

    # Extract the item_id from the URL
    parsed_url = urlparse(full_url)
    path_parts = parsed_url.path.split('/')
    item_id = path_parts[-1] if len(path_parts) > 2 else None

    if not item_id:
        print("Couldn't extract item_id from the URL.")
        return

    # API endpoint
    api_url = f"https://api2.musical.ly/aweme/v1/aweme/detail/?aweme_id={item_id}"

    # Send a request to the API
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract image URLs
    image_urls = []
    if 'image_post_info' in data['aweme_detail']:
        for image in data['aweme_detail']['image_post_info']['images']:
            image_urls.append(image['display_image']['url_list'][0])
    elif 'video' in data['aweme_detail']:
        # If it's a video, get the cover image
        image_urls.append(data['aweme_detail']['video']['cover']['url_list'][0])

    # Download images
    for i, img_url in enumerate(image_urls):
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            filename = f"tiktok_image_{i+1}.jpg"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download image {i+1}")

# Usage
url = "https://vm.tiktok.com/ZMhrX8qXQ/"
download_tiktok_images(url)