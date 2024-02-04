"use client";

import dynamic from 'next/dynamic';
import React, { useState, ChangeEvent, useEffect } from 'react';
import YouTube from 'react-youtube';
import { Button } from './ui/button';
import { Input } from './ui/input';

const VideoSection: React.FC = () => {
  const [videoUrl, setVideoUrl] = useState<string>('');
  const [queue, setQueue] = useState<{ id: string; title: string }[]>([]);
  const [currentVideoIndex, setCurrentVideoIndex] = useState<number | null>(null);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setVideoUrl(event.target.value);
  };

  const fetchVideoTitle = async (videoId: string) => {
    try {
      const response = await fetch(
        `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=snippet&key=AIzaSyB8weUJgIcYroqe9DXl58YvlomjmDHPnz0`
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch video title: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      const title = data.items?.[0]?.snippet?.title || 'Video Title Not Available';

      return title;
    } catch (error) {
      console.error('Error fetching video title:', error);
      return 'Video Title Not Available';
    }
  };

  const handleVideoSubmit = async () => {
    const urlParts = videoUrl.split('v=');
    const id = urlParts[1];

    // Fetch video title
    const title = await fetchVideoTitle(id);

    // Add video to the queue with title
    setQueue([...queue, { id, title }]);

    // If it's the first video, start playing immediately
    if (currentVideoIndex === null) {
      setCurrentVideoIndex(0);
    }
  };

  const handleQueueItemClick = (index: number) => {
    setCurrentVideoIndex(index);
  };

  const youtubeOptions = {
    width: '640',
    height: '360',
    playerVars: {
      autoplay: 0, // Set autoplay to 0 to disable autoplay
    },
  };

  useEffect(() => {
    // Ensure the video title is available when changing the currentVideoIndex
    if (currentVideoIndex !== null) {
      fetchVideoTitle(queue[currentVideoIndex].id).then((title) => {
        setQueue((prevQueue) => {
          const updatedQueue = [...prevQueue];
          updatedQueue[currentVideoIndex].title = title;
          return updatedQueue;
        });
      });
    }
  }, [currentVideoIndex]);

  return (
    <div className="max-w-5xl	">

      {/* Queue List on the Left Below */}
      <div className="queue-container">
        <h2>Queue List</h2>
        <ul>
          {queue.map((item, index) => (
            <li key={index} onClick={() => handleQueueItemClick(index)}>
              {item.title}
            </li>
          ))}
        </ul>
      </div>

      {/* Video View on the Right Below */}
      <div className="video-view-container">
        {/* Input text box for YouTube URL and Button at the Top */}
        <div className="flex w-full items-start justify-between gap-2">
          <Input
            autoFocus
            type="text"
            placeholder="Enter YouTube URL"
            value={videoUrl}
            onChange={handleInputChange}
            className="url-input flex-2"
          />
          {/* Button to submit the URL */}
          <Button onClick={handleVideoSubmit}>
            Show Video
          </Button>
        </div>

        {/* Display YouTube video */}
        {currentVideoIndex !== null && (
          <>
            <h2>{queue[currentVideoIndex].title}</h2>
            <YouTube
              videoId={queue[currentVideoIndex].id}
              opts={youtubeOptions}
              className="youtube-video"
            />
          </>
        )}
      </div>
      
      <style jsx>{`
        .video-section-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          display: flex;
          flex-direction: row;
        }

        .queue-container {
          width: 30%;
          margin-right: 20px;
        }

        .video-view-container {
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        ul {
          list-style-type: none;
          padding: 0;
        }

        li {
          cursor: pointer;
          padding: 8px;
          margin: 4px;
          background-color: #eee;
        }

        li:hover {
          background-color: #ddd;
        }

        /* Your existing styling styles here */
      `}</style>
    </div>
  );
};

export default dynamic(() => Promise.resolve(VideoSection), { ssr: false });
