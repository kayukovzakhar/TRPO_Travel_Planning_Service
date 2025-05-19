import { useRouter } from "next/router";
import Link from "next/link";
import Sidebar from "../../components/Sidebar";
import { useState } from "react";

type ChecklistItem = {
  title: string;
  description: string;
  photo: string; // URL картинки
};

const routeDetails: Record<
  string,
  {
    title: string;
    description: string;
    details: string;
    checklist: ChecklistItem[];
  }
> = {
  petersburg: {
    title: "Романтический Петербург",
    description: "Эрмитаж, Невский проспект, прогулки по рекам.",
    details:
      "Петербург — культурная столица России с множеством исторических достопримечательностей и атмосферой романтики.",
    checklist: [
      {
        title: "Посещение Эрмитажа",
        description: "Огромный музей с мировой коллекцией искусства.",
        photo: "/images/ermitage.jpg",
      },
      {
        title: "Прогулка по Невскому проспекту",
        description: "Главная улица города с магазинами и кафе.",
        photo: "/images/nevsky.jpg",
      },
      {
        title: "Поездка на речном трамвайчике",
        description: "Прогулка по каналам и рекам города.",
        photo: "/images/riverboat.jpg",
      },
      {
        title: "Визит в Петропавловскую крепость",
        description: "Исторический центр с музеями и парком.",
        photo: "/images/peterfort.jpg",
      },
    ],
  },
  "zolotoe-kolco": {
    title: "Золотое кольцо России",
    description: "Владимир, Суздаль, Ростов Великий — история и архитектура.",
    details:
      "Золотое кольцо — это древние города с богатой историей, архитектурой и уникальной русской культурой.",
    checklist: [
      {
        title: "Владимирский Успенский собор",
        description: "Знаменитый собор с фресками Андрея Рублева.",
        photo: "/images/vladimir_cathedral.jpg",
      },
      {
        title: "Суздальский кремль",
        description: "Исторический центр города с музеями.",
        photo: "/images/suzdal_kremlin.jpg",
      },
      {
        title: "Ростовский кремль",
        description: "Один из красивейших архитектурных ансамблей России.",
        photo: "/images/rostov_kremlin.jpg",
      },
      {
        title: "Музей деревянного зодчества",
        description: "Коллекция старинных деревянных построек.",
        photo: "/images/wooden_architecture.jpg",
      },
    ],
  },
  kavkaz: {
    title: "Кавказские горы",
    description: "Домбай, Эльбрус, горные тропы и горячие источники.",
    details:
      "Кавказские горы — отличное место для любителей природы, горных походов и отдыха на природе.",
    checklist: [
      {
        title: "Подъём на Эльбрус",
        description: "Самая высокая гора Европы, популярное место для альпинизма.",
        photo: "/images/elbrous.jpg",
      },
      {
        title: "Горнолыжный курорт Домбай",
        description: "Зимние виды спорта и красивые пейзажи.",
        photo: "/images/dombay.jpg",
      },
      {
        title: "Поход к водопадам",
        description: "Маршруты с живописными водопадами и горными видами.",
        photo: "/images/waterfalls.jpg",
      },
      {
        title: "Посещение горячих источников",
        description: "Релаксация и здоровье в природных бассейнах.",
        photo: "/images/hotsprings.jpg",
      },
    ],
  },
};

export default function RoutePage() {
  const router = useRouter();
  const { id } = router.query;
  const [checked, setChecked] = useState<boolean[]>([false, false, false, false]);

  if (!id || typeof id !== "string" || !routeDetails[id]) {
    return (
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-4">Маршрут не найден</h1>
        <Link href="/" className="text-blue-600 underline">
          Вернуться на главную
        </Link>
      </div>
    );
  }

  const { title, description, details, checklist } = routeDetails[id];

  const toggleCheck = (index: number) => {
    const newChecked = [...checked];
    newChecked[index] = !newChecked[index];
    setChecked(newChecked);
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />

      <main className="flex-1 py-12 px-10 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4 text-blue-900">{title}</h1>
        <p className="text-lg mb-6 text-gray-700">{description}</p>
        <p className="mb-8 text-gray-600">{details}</p>

        <div className="flex flex-col gap-6">
          {checklist.map((item, i) => (
            <button
              key={i}
              onClick={() => toggleCheck(i)}
              className={`flex items-center gap-4 p-6 rounded-2xl border shadow-md transition-colors duration-300 ${
                checked[i] ? "bg-green-100 border-green-500" : "bg-white border-gray-300 hover:bg-blue-50"
              }`}
            >
              <img
                src={item.photo}
                alt={item.title}
                className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
              />
              <div className="text-left">
                <h3 className="text-xl font-semibold text-blue-800">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            </button>
          ))}
        </div>

        <Link href="/" className="inline-block mt-10 text-blue-600 underline">
          ← Назад на главную
        </Link>
      </main>
    </div>
  );
}
