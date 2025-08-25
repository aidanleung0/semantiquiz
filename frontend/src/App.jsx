import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import LandingPage from "./pages/LandingPage"
import FlashcardPage from "./pages/FlashcardPage"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/set/:id" element={<FlashcardPage />} />
      </Routes>
    </Router>
  )
}

export default App
