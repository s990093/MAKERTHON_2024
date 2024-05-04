import Image from "next/image";
import PhotoComponent from "./component/photo";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Photo Gallery</h1>
      <PhotoComponent /> {/* 使用你的組件 */}
    </main>
  );
}
