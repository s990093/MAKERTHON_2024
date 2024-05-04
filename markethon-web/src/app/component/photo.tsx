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
  let delay = 500;
  let PIX = 400;
  const [photo, setPhoto] = useState<PhotoData | null>(null);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    const fetchPhoto = async () => {
      try {
        const response = await fetch(`${baseUrl}/app/`);
        const data: PhotoData = await response.json();
        // change the data
        data.photo_url = `${baseUrl}${data.photo_url}`;
        setPhoto(data);
      } catch (error) {
        console.error("Error fetching photo:", error);
      }
    };

    fetchPhoto();

    const interval = setInterval(() => {
      setRefresh(!refresh);
    }, delay);

    return () => clearInterval(interval);
  }, [baseUrl, delay, refresh]);

  return (
    <div>
      {photo ? (
        <Image
          loader={() => photo.photo_url}
          src={photo.photo_url}
          width={PIX}
          height={PIX}
          alt={""}
        />
      ) : (
        <p>Loading photo...</p>
      )}
    </div>
  );
};

export default PhotoComponent;
