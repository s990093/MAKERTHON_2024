"use client";
// import Darw from "./draw";
import React, { useState, useEffect } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import {
  faLightbulb,
  faLightbulb as faLightbulbOff,
  faPlay,
  faStop,
} from "@fortawesome/free-solid-svg-icons";

// Data to send before listening for messages
const data_to_send = {
  device: "ipad",
  people_count: 10,
  message: "",
};

const URL = "ws://127.0.0.1:8000/ws/chat/test/";
// const URL = "ws://49.213.238.75:8000/ws/chat/test/";
// const SERVER_URL = "ws://127.0.0.1:8000/ws/chat/test/";
const SERVER_URL = "ws://49.213.238.75:8000/ws/chat/test/";

export default function Home() {
  const [isNightLightOn, setNightLightOn] = useState<boolean>(false);
  const [isPlaying, setPlaying] = useState<boolean>(false);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Establish WebSocket connection
    const socket = new WebSocket(SERVER_URL);

    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      console.log("Message from server:", event.data);
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    setWs(socket);

    // Cleanup WebSocket connection on component unmount
    return () => {
      socket.close();
    };
  }, []);

  const toggleNightLight = () => {
    const newState = !isNightLightOn;
    setNightLightOn(newState);
    console.log(newState ? "Night Light On" : "Night Light Off");

    if (ws && ws.readyState === WebSocket.OPEN) {
      const message = {
        device: "ipad",
        state: newState ? "on" : "off",
      };
      ws.send(JSON.stringify(message));
    } else {
      console.log("WebSocket is not connected");
    }
  };

  const toggleMusic = () => {
    const newState = !isPlaying;
    setPlaying(newState);
    handlePlayMusic(newState);
    console.log(newState ? "Music Playing" : "Music Stopped");
  };

  const handlePlayMusic = (playState: boolean) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      const message = {
        device: "ipad",
        state: playState ? "play" : "stop",
      };
      ws.send(JSON.stringify(message));
    } else {
      console.log("WebSocket is not connected");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <div className="flex flex-col items-center mb-8">
        <div
          className={`w-24 h-24 rounded-full flex items-center justify-center transition-colors duration-500 ${
            isNightLightOn ? "bg-yellow-400" : "bg-gray-700"
          }`}
          onClick={toggleNightLight}
        >
          <FontAwesomeIcon
            icon={isNightLightOn ? faLightbulb : faLightbulbOff}
            className="text-4xl cursor-pointer transition-transform duration-500 transform hover:scale-110"
          />
        </div>
      </div>
      <div className="flex flex-col items-center">
        <div
          className={`relative w-48 h-48 rounded-full bg-black border-8 border-gray-800 flex items-center justify-center transition-transform duration-500 ${
            isPlaying ? "animate-spin" : ""
          }`}
          onClick={toggleMusic}
        >
          <FontAwesomeIcon
            icon={isPlaying ? faStop : faPlay}
            className="text-4xl cursor-pointer transition-transform duration-500 transform hover:scale-110"
          />
          <div className="absolute inset-0 m-auto w-2 h-2 bg-white rounded-full" />
        </div>
      </div>
    </div>
  );
}
