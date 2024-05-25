"use client";
import Image from "next/image";
import PhotoComponent from "./component/photo";
import Darw from "./draw";
import React, { useState, useEffect } from "react";

const URL = "ws://127.0.0.1:8000/ws/chat/test/";
// const URL = "ws://49.213.238.75:8000/ws/chat/test/";
const SERVER_URL = "ws://49.213.238.75:5000/ws/chat/test/";

const WindSpeedComponent: React.FC = () => {
  const [windSpeed, setWindSpeed] = useState<number>(0);
  const [electricityFromWind, setElectricityFromWind] = useState<number>(0);
  const [electricityFromBlowing, setElectricityFromBlowing] =
    useState<number>(0);

  useEffect(() => {
    // Establish WebSocket connection
    const ws = new WebSocket(SERVER_URL);

    // Data to send before listening for messages
    const data_to_send = {
      device: "ipad ",
      people_count: 10,
      message: "",
    };

    // Send data to the WebSocket server
    ws.onopen = () => {
      ws.send(JSON.stringify(data_to_send));
    };

    // Handle messages received through WebSocket
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message);
      if (message.click === true && message.speed !== undefined) {
        updateWindSpeed(message.speed);
      }
    };

    // Cleanup WebSocket connection on unmount
    return () => {
      ws.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const updateWindSpeed = (speed: number) => {
    setWindSpeed(speed);

    // Calculate wind power and blowing power
    const windPower = calculateWindPower(speed);
    setElectricityFromWind(windPower);

    const blowingPower = speed;
    setElectricityFromBlowing(blowingPower);
  };

  // Function to calculate wind power
  const calculateWindPower = (speed: number) => {
    return speed * 10; // Assuming a simple linear relationship
  };

  return (
    <div className="text-center mt-8 font-sans">
      <h1 className="text-6xl font-bold mb-10">風速：{windSpeed} km/h</h1>
      <div className="flex justify-center space-x-8">
        <div className="text-left">
          <h2 className="text-4xl font-semibold mb-4">風力發電產生的電力：</h2>
          <p className="text-3xl">{electricityFromWind} 瓦特</p>
        </div>
        <div className="text-left">
          <h2 className="text-4xl font-semibold mb-4">吹風產生的電力：</h2>
          <p className="text-3xl">{electricityFromBlowing} 瓦特</p>
        </div>
      </div>
    </div>
  );
};

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="w-full text-center py-6 bg-blue-500 text-white">
        <h1 className="text-3xl font-bold">風速監控系統</h1>
      </header>

      {/* Container for centering the content */}
      <div className="flex-grow flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <WindSpeedComponent />
        </div>
      </div>
    </div>
  );
}
