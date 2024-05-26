"use client";
// import Darw from "./draw";
import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

// Data to send before listening for messages
const data_to_send = {
  device: "ipad",
  people_count: 10,
  message: "",
};

const URL = "ws://127.0.0.1:8000/ws/chat/test/";
// const URL = "ws://49.213.238.75:8000/ws/chat/test/";
const SERVER_URL = "ws://49.213.238.75:5000/ws/chat/test/";

const WindSpeedComponent: React.FC = () => {
  const [windSpeed, setWindSpeed] = useState<number>(0);
  const [electricityFromWind, setElectricityFromWind] = useState<number>(0);
  const [electricityFromBlowing, setElectricityFromBlowing] =
    useState<number>(0);
  const [isConnecting, setIsConnecting] = useState<boolean>(false); // State to manage connection status
  const [windSpeedData, setWindSpeedData] = useState<number[]>([]);

  useEffect(() => {
    // Establish WebSocket connection
    const ws = new WebSocket(SERVER_URL);

    // Send data to the WebSocket server
    ws.onopen = () => {
      ws.send(JSON.stringify(data_to_send));
      setIsConnecting(true); // Set connection status to false when open
    };

    // Handle messages received through WebSocket
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message.speed);
      // if (message.speed >= 200) {
      // ?????
      // message.speed = message.speed - 175;
      updateWindSpeed(message.speed - 175);

      // if (message.speed < 0) {
      //     message.speed = 0;
      //   }
      //   setTimeout(() => {
      //     updateWindSpeed(message.speed);
      //   }, 1000); // 3 seconds delay      } else {
      //   updateWindSpeed(0);
      // }

      setWindSpeedData((prevData) => {
        const newData = [...prevData, message.speed];
        // Keep only the last 600 data points
        return newData.length > 100
          ? newData.slice(newData.length - 100)
          : newData;
      });
    };

    // Cleanup WebSocket connection on unmount
    return () => {
      ws.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const chartData = {
    labels: windSpeedData.map((_, index) => index + 1),
    datasets: [
      {
        label: "Wind Speed (km/h)",
        data: windSpeedData,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: false,
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: "Data Point",
        },
      },
      y: {
        title: {
          display: true,
          text: "Wind Speed (km/h)",
        },
        beginAtZero: true,
      },
    },
  };

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
      {windSpeed == 0 ? (
        <h1 className="text-9xl font-bold mb-10 text-red-600">吹一下!</h1>
      ) : (
        <>
          <div className="mt-8">
            <Line data={chartData} options={chartOptions} />
          </div>
          <h1 className="text-6xl font-bold mb-10">風速：{windSpeed} km/h</h1>
          <div className="flex justify-center space-x-8">
            <div className="text-left">
              <h2 className="text-4xl font-semibold mb-4">
                風力發電產生的電力：
              </h2>
              <p className="text-3xl">{electricityFromWind} 瓦特</p>
            </div>
            <div className="text-left">
              <h2 className="text-4xl font-semibold mb-4">吹風產生的電力：</h2>
              <p className="text-3xl">{electricityFromBlowing} 瓦特</p>
            </div>
          </div>
        </>
      )}
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
