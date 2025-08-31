import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const items = [
  {
    word: "Ephemeral",
    definition: "Lasting a short time.",
    feedback: "✅ Correct! Ephemeral means something brief and short-lived.",
    status: "correct" // green
  },
  {
    word: "Prolific",
    definition: "Tiny or insignificant.",
    feedback: "⚠️ Almost! Prolific actually means producing a lot, not tiny.",
    status: "middle" // yellow
  },
  {
    word: "Obfuscate",
    definition: "To polish a surface to a brilliant shine.",
    feedback: "❌ Incorrect! Obfuscate means to make something confusing or unclear.",
    status: "wrong" // red
  }
];

const feedbackColors: Record<string, string> = {
  correct: "bg-green-100 border-green-300",
  middle: "bg-yellow-100 border-yellow-300",
  wrong: "bg-red-100 border-red-300",
};

export default function TypewriterFlashcard() {
  const [index, setIndex] = useState(0);
  const [displayed, setDisplayed] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    let i = 0;
    setShowFeedback(false);
    const currentText = items[index].definition;

    const interval = setInterval(() => {
      setDisplayed(currentText.slice(0, i + 1));
      i++;
      if (i === currentText.length) {
        clearInterval(interval);
        setTimeout(() => {
          setShowFeedback(true);
          setTimeout(() => {
            setDisplayed("");
            setShowFeedback(false);
            setIndex((prev) => (prev + 1) % items.length);
          }, 3000); // keep feedback visible for 3s
        }, 500); // delay before showing feedback
      }
    }, 40);

    return () => clearInterval(interval);
  }, [index]);

  return (
    <div className="grid md:grid-cols-2 gap-8 items-center">
      {/* Flashcard */}
      <motion.div
        key={`card-${index}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="bg-white rounded-2xl shadow-md p-6 border border-matcha"
      >
        <h3 className="font-bold text-lg text-gray-900 mb-3">
          {items[index].word}
        </h3>
        <div className="border border-gray-300 rounded-md p-3 bg-gray-50 min-h-[80px] font-ptrootui text-gray-700">
          {displayed}
          <span className="animate-blink">|</span>
        </div>
      </motion.div>

      {/* Feedback card */}
      <AnimatePresence>
        {showFeedback && (
          <motion.div
            key={`feedback-${index}`}
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 40 }}
            transition={{ duration: 0.6 }}
            className={`rounded-2xl shadow-md p-6 border ${feedbackColors[items[index].status]}`}
          >
            <h3 className="font-bold text-lg text-gray-900 mb-3">
              AI Feedback ✨
            </h3>
            <p className="font-ptrootui text-gray-700">
              {items[index].feedback}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
