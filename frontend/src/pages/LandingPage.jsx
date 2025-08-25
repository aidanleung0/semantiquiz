import { Link } from "react-router-dom"
import { flashcardSets } from "../data/flashcards"

export default function LandingPage() {
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Your Flashcard Sets</h1>
      <div className="grid gap-4">
        {flashcardSets.map(set => (
          <Link
            key={set.id}
            to={`/set/${set.id}`}
            className="p-4 bg-white rounded-xl shadow hover:bg-gray-50 transition"
          >
            <h2 className="text-xl font-semibold">{set.title}</h2>
            <p className="text-gray-600">{set.cards.length} cards</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
