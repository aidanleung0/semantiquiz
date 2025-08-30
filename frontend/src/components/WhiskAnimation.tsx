// src/components/WhiskAnimation.tsx
import React from "react";
import { motion } from "framer-motion";

export default function WhiskAnimation() {
  return (
    <div className="relative w-64 h-64 md:w-80 md:h-80 flex justify-center items-end">
      {/* Wooden bowl */}
      <div className="absolute bottom-0 w-56 md:w-72 h-20 md:h-28 bg-yellow-700 rounded-full shadow-inner"></div>

      {/* Matcha powder inside bowl */}
      <div className="absolute bottom-4 w-52 md:w-68 h-12 md:h-16 bg-green-500 rounded-full shadow-inner"></div>

      {/* Whisk handle */}
      <motion.div
        className="absolute w-4 md:w-6 h-32 md:h-40 bg-yellow-800 rounded-full origin-bottom"
        animate={{ rotate: [0, -25, 25, 0] }}
        transition={{ repeat: Infinity, duration: 1.2, ease: "easeInOut" }}
      ></motion.div>

      {/* Whisk wires */}
      <motion.div
        className="absolute w-10 md:w-14 h-20 md:h-24 border-t-4 border-yellow-700 rounded-t-full origin-bottom"
        animate={{ rotate: [0, -25, 25, 0] }}
        transition={{ repeat: Infinity, duration: 1.2, ease: "easeInOut" }}
      ></motion.div>

      {/* Floating matcha powder particles */}
      {[...Array(8)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 md:w-3 md:h-3 bg-green-300 rounded-full"
          initial={{ y: 0, opacity: 0 }}
          animate={{ y: [-5, -15, -5], opacity: [0, 1, 0] }}
          transition={{
            repeat: Infinity,
            delay: i * 0.15,
            duration: 1.2,
            ease: "easeInOut",
          }}
        ></motion.div>
      ))}
    </div>
  );
}
