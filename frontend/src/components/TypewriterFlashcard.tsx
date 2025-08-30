// src/components/AnimatedFlashcard.tsx
import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const items = [
  {
    phrase: "Matcha is a finely ground powder of shade-grown green tea leaves.",
    feedback: "Nice! Remember: matcha is shade-grown, which makes it richer in nutrients."
  },
  {
    phrase: "It contains more antioxidants than regular green tea.",
    feedback: "Great connection! The higher antioxidants come from consuming the whole leaf."
  },
  {
    phrase: "Traditionally whisked into hot water, not steeped.",
    feedback: "Exactly—unlike tea bags, matcha is whisked, giving you the entire leaf."
  }
];

export default function AnimatedFlashcard() {
  const [index, setIndex] = useState(0);
  const [displayed, setDisplayed] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    let i = 0;
    setShowFeedback(false);
    const currentText = items[index].phrase;

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
        }, 500); // small delay before showing feedback
      }
    }, 40);

    return () => clearInterval(interval);
  }, [index]);

  return (
    <div className="grid md:grid-cols-2 gap-8 items-center">
      {/* Flashcard with input-style box */}
      <motion.div
        key={`card-${index}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="bg-white rounded-2xl shadow-md p-6 border border-green-200"
      >
        <h3 className="font-bold text-lg text-gray-900 mb-3">Flashcard</h3>
        <div className="border border-gray-300 rounded-md p-3 bg-gray-50 min-h-[80px] font-ptrootui text-gray-700">
          {displayed}
          <span className="animate-blink">|</span>
        </div>
      </motion.div>

      {/* AI Feedback card */}
      <AnimatePresence>
        {showFeedback && (
          <motion.div
            key={`feedback-${index}`}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.6 }}
            className="bg-green-50 rounded-2xl shadow-md p-6 border border-green-200"
          >
            <h3 className="font-bold text-lg text-gray-900 mb-3">AI Feedback ✨</h3>
            <p className="font-ptrootui text-gray-700">{items[index].feedback}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
