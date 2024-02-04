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

  const sendVideoUrl =async (videoUrl: string) => {
    try {
      const response = await fetch('http://localhost:8000/upload_video', { // Change the URL to your backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoUrl }),
      });

      if (!response.ok) {
        throw new Error(`Failed to upload video URL to backend: ${response.status} - ${response.statusText}`);
      }

      console.log('Video URL successfully sent to backend.');
      // Handle success response from backend if needed
    } catch (error) {
      console.error('Error sending video URL to backend:', error);
      // Handle error response from backend if needed
    }
  }

  const handleVideoSubmit = async () => {
    const urlParts = videoUrl.split('v=');
    const id = urlParts[1];

    // Fetch video title
    const title = await fetchVideoTitle(id);

    // Add video to the queue with title
    setQueue([...queue, { id, title }]);

    // Send video to backend
    sendVideoUrl(videoUrl);

    // If it's the first video, start playing immediately
    if (currentVideoIndex === null) {
      setCurrentVideoIndex(0);
    }
  };

  const handleQueueItemClick = (index: number) => {
    setCurrentVideoIndex(index);
  };

  const youtubeOptions = {
    width: '720',
    height: '400',
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
    <div className="flex flex-row space-y-4 max-w-5xl w-full">

      {/* Queue List on the Left Below */}
      <div className="mr-3 w-1/3">
        <p className="font-mono text-md font-bold p-2 m-2">Resource List</p>
        <div className='overflow-auto max-h-96'>
          <ul className="list-none">
            {queue.map((item, index) => (
              <li key={index} className='cursor-pointer font-mono text-sm border-solid rounded-lg p-4 m-2 bg-gradient-to-r from-purple-200 hover:bg-pink-200 hover:ring hover:ring-offset-2 hover:ring-neutral-300'
                onClick={() => handleQueueItemClick(index)}>
                {item.title}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Video View on the Right Below */}
      <div className="flex flex-col flex-1">
        {/* Input text box for YouTube URL and Button at the Top */}
        <div className="flex items-center justify-between gap-2 p-2">
          <Input
            autoFocus
            type="text"
            placeholder="Enter YouTube URL"
            value={videoUrl}
            onChange={handleInputChange}
            className="url-input mr-1 flex-1"
          />
          {/* Button to submit the URL */}
            <Button onClick={handleVideoSubmit} className='bg-gradient-to-r from-green-400 to-blue-500 hover:from-pink-500 hover:to-yellow-500 '>
              Load Video
            </Button>
        </div>

        {/* Display YouTube video */}
        {currentVideoIndex !== null && (
          <div className="flex items-center justify-between p-2">
            <YouTube
              videoId={queue[currentVideoIndex].id}
              opts={youtubeOptions}
              className="youtube-video"
            />
          </div>
        )}
      </div>
      
    </div>
  );
};

export default dynamic(() => Promise.resolve(VideoSection), { ssr: false });
