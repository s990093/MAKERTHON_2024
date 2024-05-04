"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

// 定義照片數據的類型
interface PhotoData {
  message: string;
  photo_url: string;
}

const PhotoComponent: React.FC = () => {
  let baseUrl = "http://49.213.238.75:8000";
  const [photo, setPhoto] = useState<PhotoData | null>(null);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    const fetchPhoto = async () => {
      try {
        const response = await fetch(`${baseUrl}/app/`);
        const data: PhotoData = await response.json();
        data.photo_url = `${baseUrl}${data.photo_url}`;
        console.log(data.photo_url);
        setPhoto(data);
      } catch (error) {
        console.error("Error fetching photo:", error);
      }
    };

    fetchPhoto();

    const interval = setInterval(() => {
      setRefresh(!refresh);
    }, 5000);

    return () => clearInterval(interval);
  }, [baseUrl, refresh]);

  return (
    <div>
      {photo ? (
        <Image
          src={photo.photo_url}
          alt="Random Photo"
          width={400} // 圖片寬度
          height={300} // 圖片高度
          layout="responsive" // 可根據容器尺寸自動調整
        />
      ) : (
        <p>Loading photo...</p>
      )}
    </div>
  );
};

export default PhotoComponent;
