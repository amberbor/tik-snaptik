import hashlib
import os
import tempfile
import urllib.request
from urllib.parse import urlparse
from typing import List

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import concurrent.futures
from image_downloader import download_image_out

app = FastAPI()

# Set up CORS
origins = ["http://localhost:3000"]  # Replace with your actual frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def download_image_save(url: str, local_path: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)

        print("local_path", local_path)
        return local_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download image: {e}")


def download_image_get(url: str, isVideo:bool):
    try:
        # Use a hash of the URL as part of the filename to make it unique
        filename_hash = hashlib.sha256(url.encode()).hexdigest()[:10]

        if isVideo:
            suffix = ".mp4"
        else:
            suffix = ".jpg"

        user_home = os.path.expanduser("~")
        downloads_dir = os.path.join(user_home, "Downloads")

        # Create a temporary file in the user's default download directory
        temp_file = tempfile.NamedTemporaryFile(prefix=f"downloaded_image_{filename_hash}_", suffix=suffix,
                                                delete=False, dir=downloads_dir)
        local_path = temp_file.name

        urllib.request.urlretrieve(url, local_path)
        print(local_path)
        return local_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download image: {e}")


def stream_image(file_path: str, isVideo:bool):
    try:
        media_type = "video/mp4" if isVideo else "image/jpeg"
        return FileResponse(file_path, media_type=media_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stream image: {e}")
    finally:
        # Clean up by removing the temporary image file
        # os.remove(file_path)
        print("yes")


@app.get('/download-image', response_class=FileResponse)
def download_image(url: str, isVideo: bool = False):
    local_path = download_image_get(url, isVideo)
    print(local_path)
    return stream_image(local_path, isVideo)


@app.post('/downloadAll', response_class=FileResponse)
def download_all(data: dict):
    try:
        image_urls = data.get('urls', [])
        responses = [download_image_get(url) for url in image_urls]

        # Stream each image separately
        return stream_image(responses[0])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download TikTok images: {e}")

@app.get('/download')
def download_tiktok(url: str, hd: str):
    tiktok_api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    headers = {
        # "X-RapidAPI-Key": "47406c2fdamshdeb572e33153011p122233jsn4fbb9e035084",
        "X-RapidAPI-Key": "22a6ad40a6msh640e908bb484950p1ee59ejsn68e3891bf491",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    querystring = {"url": url, "hd": hd}

    try:
        response = requests.get(tiktok_api_url, headers=headers, params=querystring)
        response.raise_for_status()

        data = response.json()

        images = data.get('data', {}).get('images', [])
        modified_data = {
            'images': [{'url': image, 'id': f'image_{index + 1}'} for index, image in enumerate(images)],
            'play': data.get('data', {}).get('play'),
        }

        return JSONResponse(content=modified_data)

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to download TikTok data: {e}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
