// src/pages/LandingPage.tsx
import React from "react";
import Latte from "../components/Latte";
import TypewriterFlashcard from "../components/TypewriterFlashcard";
import WhiskAnimation from "../components/WhiskAnimation";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="fixed inset-x-0 top-0 w-full bg-matcha text-white shadow-md z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-ptrootui font-bold tracking-wide">
            MatchaQuiz
          </div>
          <div className="space-x-6 flex font-ptrootui">
            <a href="#about" className="hover:underline">About</a>
            <a href="#features" className="hover:underline">Features</a>
            <a href="#login" className="hover:underline">Login</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="flex-1 flex flex-col items-center justify-center px-10 pt-60 pb-20">
        {/* Top row: text + image */}
        <div className="flex flex-col md:flex-row items-center md:items-start justify-center w-full max-w-6xl gap-12">
          {/* Left column */}
          <div className="flex-1 text-left mx-auto">
            <h1 className="text-6xl md:text-7xl font-ptrootui font-extrabold leading-none">
              Steep your mind in knowledge.
            </h1>
            <div className="mt-10 text-left max-w-2xl">
              <p className="text-xl font-ptrootui font-light text-gray-700">
                Brew stronger word-to-definition connections with AI-powered flashcards
                that make learning calm, focused, and effective.
              </p>
              <div className="mt-8 flex justify-left space-x-4">
                <button className="px-6 py-3 rounded-2xl bg-matcha text-white font-ptrootui font-medium shadow-lg hover:opacity-90 transition">
                  Get Started
                </button>
                <button className="px-6 py-3 rounded-2xl border border-matcha text-matcha font-ptrootui font-medium hover:bg-matcha/10 transition">
                  Learn More
                </button>
              </div>
            </div>
          </div>

          {/* Right column */}
          <div className="flex-1 flex justify-center md:justify-end hidden md:block">
            {/* Replace with your whisk animation / image */}
            <img
              src="/images/matcha_bowl.png"
              alt="Matcha Bowl"
              className="w-full max-w-md mx-auto"
            />
          </div>
        </div>

        
      </header>

      {/* How It Works */}
      <section id="about" className="py-20 px-10 bg-creme-medium">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-gray-900">How It Works</h2>
          <p className="mt-4 text-xl font-ptrootui font-light text-gray-700">
            Watch how MatchaQuiz turns a word into a flashcard + AI feedback.
          </p>
          <div className="mt-12">
            <TypewriterFlashcard />
          </div>
        </div>
      </section>

      {/* Why MatchaQuiz */}
      {/* <section id="features" className="py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-gray-900">Why MatchaQuiz?</h2>
          <div className="mt-12 grid gap-10 md:grid-cols-3">
            <div className="p-6 rounded-2xl bg-white shadow-md">
              <h3 className="font-semibold text-xl mb-2">AI-powered focus</h3>
              <p className="text-gray-600">Forget rote memorization—learn smarter with tailored connections.</p>
            </div>
            <div className="p-6 rounded-2xl bg-white shadow-md">
              <h3 className="font-semibold text-xl mb-2">Word-first recall</h3>
              <p className="text-gray-600">Train recall from the word, not just the definition.</p>
            </div>
            <div className="p-6 rounded-2xl bg-white shadow-md">
              <h3 className="font-semibold text-xl mb-2">Calm design</h3>
              <p className="text-gray-600">Matcha-inspired visuals that make studying a ritual, not a chore.</p>
            </div>
          </div>
        </div>
      </section> */}

      {/* Footer */}
      <footer className="bg-matcha text-white py-8 mt-20">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm">&copy; {new Date().getFullYear()} MatchaQuiz. All rights reserved.</p>
          <div className="space-x-4 mt-4 md:mt-0">
            <a href="#" className="hover:underline">Privacy</a>
            <a href="#" className="hover:underline">Terms</a>
            <a href="#" className="hover:underline">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
