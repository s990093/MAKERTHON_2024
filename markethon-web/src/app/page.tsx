import Image from "next/image";
import PhotoComponent from "./component/photo";
import Darw from "./draw";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="w-full text-center py-6 bg-blue-500 text-white">
        <h1 className="text-3xl font-bold">灑水模擬</h1>
      </header>

      {/* Container for centering the content */}
      <div className="flex-grow flex flex-col items-center justify-center bg-gray-100">
        <Darw />
      </div>

      <footer className="w-full text-center py-4 bg-gray-200">
        <p className="text-sm text-gray-600">
          &copy; 2024 Your Company Name. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
