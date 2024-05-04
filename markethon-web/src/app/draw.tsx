"use client";
import { ReactNode } from "react";
import React, { useState, useEffect } from "react";
import axios from "axios";

interface PositionedProps {
  top: number; // top 位置
  left: number; // left 位置
  children: ReactNode; // 子组件
}
interface BlueBallProps {
  isSprinkling: boolean; // 用于传入灑水状态
}

const Positioned: React.FC<PositionedProps> = ({ top, left, children }) => {
  return (
    <div
      className="absolute" // 绝对定位
      style={{ top: `${top}px`, left: `${left}px` }} // 使用 px 设置位置
    >
      {children}
    </div>
  );
};

const BlueBall: React.FC<BlueBallProps> = ({ isSprinkling }) => {
  // 根据 isSprinkling 的值选择颜色
  const ballColor = isSprinkling ? "bg-blue-900" : "bg-red-600"; // 蓝色或红色

  return (
    <div
      className={`w-3 h-3 ${ballColor} rounded-full flex items-center justify-center`}
    >
      {/* 如果需要，可以在这里添加额外的内容 */}
    </div>
  );
};

const Darw = () => {
  const [isSprinkling, setIsSprinkling] = useState(false); // 存储 API 数据

  const [audio] = useState(new Audio("/music.mp3")); // 创建 Audio 对象

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://49.213.238.75:8000/app/d/1")
        .then((response) => {
          setIsSprinkling(response.data.is_sprinkling);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }, 300);

    return () => {
      clearInterval(intervalId); // 清除计时器
    };
  }, []); // 只在组件挂载时设置一次计时器

  useEffect(() => {
    if (isSprinkling) {
      audio.play(); // 播放音效
    } else {
      audio.pause(); // 暂停音效
    }
  }, [isSprinkling, audio]);

  return (
    <div
      className="w-[500px] h-[500px] bg-center bg-cover"
      style={{
        backgroundImage: "url('/bg.png')",
      }}
    >
      {/* 1 */}
      <Positioned top={250} left={530}>
        <BlueBall isSprinkling={isSprinkling} />
        {isSprinkling && <span className="sprinkling-effect" />}{" "}
        {/* 添加灑水效果 */}
      </Positioned>
      <Positioned top={250} left={595}>
        <BlueBall isSprinkling={isSprinkling} />
        {isSprinkling && <span className="sprinkling-effect" />}{" "}
        {/* 添加灑水效果 */}
      </Positioned>

      <Positioned top={250} left={725}>
        <BlueBall isSprinkling={isSprinkling} />
        {isSprinkling && <span className="sprinkling-effect" />}
      </Positioned>
      <Positioned top={335} left={945}>
        <BlueBall isSprinkling={isSprinkling} />
        {isSprinkling && <span className="sprinkling-effect" />}
      </Positioned>
      {/* 3 */}
      <Positioned top={435} left={630}>
        <BlueBall isSprinkling={false} />
      </Positioned>
      {/* 4 */}
      <Positioned top={435} left={820}>
        <BlueBall isSprinkling={false} />
      </Positioned>
      {/* 5 */}
      <Positioned top={623} left={530}>
        <BlueBall isSprinkling={false} />
      </Positioned>
      {/* 6 */}
      <Positioned top={623} left={725}>
        <BlueBall isSprinkling={false} />
      </Positioned>
    </div>
  );
};

export default Darw;
