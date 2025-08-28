// src/pages/LandingPage.tsx
import React from "react";
import Latte from "../components/Latte";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray">
      {/* Navbar */}
      <nav className="w-full bg-matcha text-white shadow-md">
        <div className="max-w mx-auto px-6 py-4 flex items-center justify-between">
          {/* Logo / App Name */}
          <div className="text-xl font-ptrootui font-bold tracking-wide text-left">
            MatchaQuiz
          </div>

          {/* Nav Links */}
          <div className="space-x-6 flex justify-end font-ptrootui">
            <a href="#about" className="hover:underline">About</a>
            <a href="#login" className="hover:underline">Login</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="flex-1 flex flex-col items-center justify-center text-left px-6">
        <h1 className="text-4xl md:text-6xl font-ptrootui font-extrabold text-gray-900">
          Steep your mind<br />in knowledge. 🍵
        </h1>
        <p className="mt-6 text-lg font-ptrootui font-light text-gray-600 max-w-2xl">
          Test your knowledge, get instant AI feedback, and track your progress with ease.
        </p>
        <div className="mt-8 flex space-x-4">
          <button className="px-6 py-3 rounded-xl bg-matcha text-white font-ptrootui font-medium shadow-md hover:opacity-90 transition">
            Get Started
          </button>
          <button className="px-6 py-3 rounded-xl border border-matcha text-matcha font-ptrootui font-medium hover:bg-matcha/10 transition">
            Learn More
          </button>
        </div>

        {/* <div className="mt-12">
          <Latte />
        </div> */}
      </header>
    </div>
  );
}
