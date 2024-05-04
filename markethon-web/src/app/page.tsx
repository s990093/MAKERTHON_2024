import Image from "next/image";
import PhotoComponent from "./component/photo";

export default function Home() {
  return (
    <div>
      <header className="w-full text-center py-6 bg-blue-500 text-white">
        <h1 className="text-3xl font-bold">Photo Gallery</h1>
      </header>

      <section className="flex flex-col items-center justify-center w-full p-6 bg-white rounded-lg shadow-lg">
        <PhotoComponent /> {/* 使用你的組件 */}
      </section>

      <footer className="w-full text-center py-4 bg-gray-200">
        <p className="text-sm text-gray-600">
          &copy; 2024 Your Company Name. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
