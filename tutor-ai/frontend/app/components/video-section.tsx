// app/components/VideoSection.tsx

'use client';
import dynamic from 'next/dynamic';
import React, { useState, ChangeEvent } from 'react';
import YouTube from 'react-youtube';
import Slider from 'react-slick';

import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const VideoSection: React.FC = () => {
  const [videoUrls, setVideoUrls] = useState<string[]>([]);
  const [videoIds, setVideoIds] = useState<string[]>([]);

  const handleInputChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const value = event.target.value;
    setVideoUrls(value.split('\n').map(url => url.trim()));
  };

  const handleVideoSubmit = async () => {
    // Extract video IDs from the YouTube URLs
    const ids = videoUrls.map(url => {
      const urlParts = url.split(/[?&]/);
      const videoIdMatch = urlParts.find(part => part.startsWith('v='));
      return videoIdMatch ? videoIdMatch.split('=')[1] : '';
    });

    // Set the video IDs in the state
    setVideoIds(ids.filter(id => id));

    // Send the video URLs to the backend
    try {
      const response = await fetch('/api/youtube', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoUrls }),
      });

      if (response.ok) {
        console.log('Video URLs sent to the backend successfully');
      } else {
        console.error('Failed to send video URLs to the backend');
      }
    } catch (error) {
      console.error('Error sending video URLs to the backend:', error);
    }
  };

  const youtubeOptions = {
    width: '640',
    height: '360',
    playerVars: {
      autoplay: 1,
    },
  };

  const sliderSettings = {
    dots: true,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <div className="video-section-container">
      {/* Input textarea for YouTube URLs */}
      <div className="input-container">
        <textarea
          placeholder="Enter YouTube URLs (one per line)"
          value={videoUrls.join('\n')}
          onChange={handleInputChange}
          className="url-input"
        />
        {/* Button to submit the URLs */}
        <button onClick={handleVideoSubmit} className="submit-button">
          Show Videos
        </button>
      </div>

      {/* Display YouTube videos in a horizontal slider */}
      {videoIds.length > 0 && (
        <Slider {...sliderSettings} className="video-slider">
          {videoIds.map((id, index) => (
            <div key={index} className="video-container">
              <YouTube
                videoId={id}
                opts={youtubeOptions}
                className="youtube-video"
              />
            </div>
          ))}
        </Slider>
      )}

      <style jsx>{`
        /* Styles remain the same */

        .video-slider {
          margin-top: 20px;
        }
      `}</style>
    </div>
  );
};

export default dynamic(() => Promise.resolve(VideoSection), { ssr: false });