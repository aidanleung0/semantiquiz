import { useParams, useNavigate } from "react-router-dom"
import { useState } from "react"
import { flashcardSets } from "../data/flashcards"

export default function FlashcardPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const set = flashcardSets.find(s => s.id === Number(id))

  const [index, setIndex] = useState(0)
  const [userInput, setUserInput] = useState("")

  const current = set.cards[index]
  const progress = ((index + 1) / set.cards.length) * 100

  function next() {
    if (index < set.cards.length - 1) {
      setIndex(i => i + 1)
      setUserInput("")
    }
  }

  function prev() {
    if (index > 0) {
      setIndex(i => i - 1)
      setUserInput("")
    }
  }

  return (
    <div className="max-w-xl mx-auto p-6">
      <button
        onClick={() => navigate("/")}
        className="text-blue-600 mb-4 hover:underline"
      >
        ← Back to sets
      </button>

      <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
        <div
          className="bg-blue-600 h-2 rounded-full"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-2xl font-bold mb-4">{current.word}</h2>

        <input
          type="text"
          value={userInput}
          onChange={e => setUserInput(e.target.value)}
          placeholder="Type your definition..."
          className="w-full border rounded-lg p-2 mb-4"
        />

        <div className="flex justify-between">
          <button
            onClick={prev}
            disabled={index === 0}
            className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
          >
            Prev
          </button>
          <button
            onClick={next}
            disabled={index === set.cards.length - 1}
            className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  )
}
