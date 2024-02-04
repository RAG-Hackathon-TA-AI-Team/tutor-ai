import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";
import VideoSection from "./components/video-section";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-10 p-24 background-gradient">
      <Header />
      {/* TODO: Add video player component */}
      <VideoSection />
      {/* TODO: Handle youtube URL input*/}
      <ChatSection />
    </main>
  );
}
