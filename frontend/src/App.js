// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [previews, setPreviews] = useState([]);
  const [previewsVideo, setPreviewsVideo] = useState([]);
  const [response, setResponse] = useState('');

  const handleDownload = async () => {
    try {
      const response = await axios.get('http://localhost:5000/download', {
        params: { url: url, hd: '1' },
        headers: {
          // 'X-RapidAPI-Key': '47406c2fdamshdeb572e33153011p122233jsn4fbb9e035084',
          'X-RapidAPI-Key': '22a6ad40a6msh640e908bb484950p1ee59ejsn68e3891bf491',
          'X-RapidAPI-Host': 'tiktok-video-no-watermark2.p.rapidapi.com',
        },
      });

      setResponse(response.data);

      // Handle the preview based on the response
      if (response.data.images && response.data.images.length > 0) {
  setPreviews(response.data.images);
  setPreviewsVideo([]); // Reset previewsVideo if images are present
} else if (response.data.play && response.data.play.length > 0) {
  setPreviewsVideo(response.data.play);
  setPreviews([]); // Reset previews if videos are present
} else {
  setPreviews([]);
  setPreviewsVideo([]);
}

      console.log(previews)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleImageDownload = async (imageUrl, isVideo) => {
    try {
      const encoder = encodeURIComponent(imageUrl);
      await axios.get(`http://localhost:5000/download-image?url=${encoder}&isVideo=${isVideo}`);
    } catch (error) {
      console.error('Error downloading image:', error);
    }
  };

   const handleDownloadAllImages = async () => {
    try {
      const imageUrls = previews.map((preview) => preview.url);
      console.log(imageUrls)
      // const encodedUrls = imageUrls.map((url) => encodeURIComponent(url));
      // console.log(encodedUrls)
      await axios.post('http://localhost:5000/downloadAll', {
          urls: imageUrls,
      })
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };


  return (
    <div className="App">
      <header className="App-header">
        <div className="logo">Your Logo</div>
        <div className="menu">
          <ul>
            <li>Home</li>
            <li>Contact Us</li>
            <li>About</li>
          </ul>
        </div>
      </header>
      <main>
        <div className="input-container">
          <h1 className="text-body">TikTok Video Download</h1>
            <h3 className="text-body">Without Watermark. Fast. All devices</h3>
          <input
            type="text"
            placeholder="Press Url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleDownload}>Download</button>
        </div>
        {previews.length > 0 && (
        <div className="preview-container">
          {previews.map((preview, index) => (
            <div key={index} className="image-container">
              <img src={preview.url} alt={`Preview ${index + 1}`} className="preview-image" />
              <button className="download-button" onClick={() => handleImageDownload(preview.url, false)}>
                Download Image
              </button>
            </div>
          ))}
        </div>
      )}
      {previewsVideo.length > 0 && (
          <div className="video-container-wrapper">
            <div className="video-container">
              {/* Render video player or any other logic for video previews */}
              <video src={previewsVideo} controls autoPlay className="preview-video"/>
            </div>
            <button className="download-button-video" onClick={() => handleImageDownload(previewsVideo, true)}>
              Download Video
            </button>
          </div>
      )}
        <div>
          {response && previews.length > 0 && (
              <p>
                <button className="download-all-button" onClick={handleDownloadAllImages}>Download All Images</button>
                {/*Author ID: {response.data.author.unique_id}*/}
              </p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
