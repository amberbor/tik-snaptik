# image_downloader.py

import os
import requests


def download_image_out(url: str, local_path: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'https://www.tiktok.com/',  # Add a fake referer header
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(local_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

        print("local_path", local_path)
        return local_path

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download image: {e}")
