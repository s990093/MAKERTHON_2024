"use client";
import Image from "next/image";
import PhotoComponent from "./component/photo";
import Darw from "./draw";
import React, { useState, useEffect } from "react";

const WindSpeedComponent: React.FC = () => {
  const [windSpeed, setWindSpeed] = useState<number>(0);
  const [electricityFromWind, setElectricityFromWind] = useState<number>(0);
  const [electricityFromBlowing, setElectricityFromBlowing] =
    useState<number>(0);

  useEffect(() => {
    const updateWindSpeed = () => {
      const newWindSpeed = Math.floor(Math.random() * 101);
      setWindSpeed(newWindSpeed);

      // 根據風速計算風力發電的電力
      const windPower = calculateWindPower(newWindSpeed);
      setElectricityFromWind(windPower);

      // 假設使用者吹風時，每km/h產生1瓦特的電力
      const blowingPower = newWindSpeed;
      setElectricityFromBlowing(blowingPower);
    };

    updateWindSpeed();

    const intervalId = setInterval(updateWindSpeed, 5000);

    return () => clearInterval(intervalId);
  }, []);

  // 根據風速計算風力發電的電力
  const calculateWindPower = (speed: number) => {
    // 這裡可以是一個複雜的計算公式，這裡假設簡單的線性關係
    return speed * 10; // 假設每km/h產生10瓦特的電力
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
