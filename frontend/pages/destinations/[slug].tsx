// pages/destinations/[slug].tsx
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function DestinationDetail() {
  const router = useRouter()
  const { slug } = router.query

// Define the types for destination data
type Destination = {
  name: string;
  description: string;
  places: { name: string; type: string }[];
}

  // Example data for each destination (you can replace this with dynamic content or fetch data from an API)
  const destinationDetails: Record<string, Destination> = {
    "moscow-zolotoe-kolco": {
      name: "Москва и Золотое кольцо",
      description:
        "Красная площадь, Кремль, Сергиев Посад — 5 дней. Прекрасные исторические маршруты, которые позволят вам узнать культуру России.",
      places: [
        { name: "Кафе Пушкина", type: "Кафе" },
        { name: "Музей Кремля", type: "Музей" },
        { name: "Московский кинотеатр", type: "Кинотеатр" },
        { name: "Театр МХТ", type: "Театр" },
      ],
    },
    "petersburg-marshrut": {
      name: "Петербургский маршрут",
      description:
        "Эрмитаж, Невский проспект, Петергоф — 4 дня. Санкт-Петербург удивит вас своей архитектурой и культурой.",
      places: [
        { name: "Кафе на Невском", type: "Кафе" },
        { name: "Эрмитаж", type: "Музей" },
        { name: "Московский кинотеатр", type: "Кинотеатр" },
        { name: "Театр Балета", type: "Театр" },
      ],
    },
    "kavkaz-marshrut": {
      name: "Кавказские горы",
      description:
        "Красота вершин Кавказа не оставит никого равнодушным",
      places: [
        { name: "Кафе \"У брата\"", type: "Кафе" },
        { name: "Музей истории Кавказа", type: "Музей" },
        { name: "Эльбрус", type: "Достопримечательность" },
      ],
    }
    // Add more destinations here...
  }

  const destination = destinationDetails[slug as string]

  if (!destination) {
    return <div>Destination not found</div>
  }

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-4xl font-bold mb-4">{destination.name}</h1>
      <p className="text-lg mb-6">{destination.description}</p>

      <h2 className="text-2xl font-semibold mb-6">Популярные места</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {destination.places.map((place, index) => (
          <div key={index} className="p-6 bg-white shadow-xl rounded-2xl border border-blue-200">
            <h3 className="text-xl font-semibold">{place.name}</h3>
            <p className="text-gray-700 text-sm">{place.type}</p>
          </div>
        ))}
      </div>

      <Link href="/" className="text-blue-500 mt-6 inline-block">Назад на главную</Link>
    </div>
  )
}
