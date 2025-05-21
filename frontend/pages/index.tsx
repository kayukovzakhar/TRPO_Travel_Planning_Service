import React, { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import Sidebar from "../components/Sidebar";

const allRoutes = [
  {
    id: "petersburg",
    title: "Романтический Петербург",
    description: "Эрмитаж, Невский проспект, прогулки по рекам.",
  },
  {
    id: "zolotoe-kolco",
    title: "Золотое кольцо России",
    description: "Владимир, Суздаль, Ростов Великий — история и архитектура.",
  },
  {
    id: "kavkaz",
    title: "Кавказские горы",
    description: "Домбай, Эльбрус, горные тропы и горячие источники.",
  },
];


function shuffleArray<T>(array: T[]): T[] {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export default function Home() {
  const [location, setLocation] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  // const [recommendedRoutes, setRecommendedRoutes] = useState(allRoutes);
  const [recommendedRoutes] = useState(allRoutes);
  const [visibleRecommended, setVisibleRecommended] = useState(allRoutes.slice(0, 3));
  // const [lastVisibleIds, setLastVisibleIds] = useState(allRoutes.slice(0, 3).map(r => r.id));
  const router = useRouter();

  const inputRef = useRef<HTMLInputElement>(null);

  const filteredSuggestions = location.trim()
    ? recommendedRoutes.filter(r => r.title.toLowerCase().includes(location.toLowerCase())).slice(0, 3)
    : [];

const handleShuffle = () => {
  // Кандидаты — маршруты, которых сейчас нет в visibleRecommended
  const currentIds = visibleRecommended.map(r => r.id);
  const candidates = recommendedRoutes.filter(r => !currentIds.includes(r.id));

  if (candidates.length === 0) {
    // Если кандидатов нет (т.е. все маршруты в visibleRecommended), можно просто перемешать все и показать первые 3
    const shuffled = shuffleArray(recommendedRoutes);
    const newVisible = shuffled.slice(0, 3);
    setVisibleRecommended(newVisible);
    // setLastVisibleIds(newVisible.map(r => r.id));
    return;
  }

  // Копируем текущие visibleRecommended для изменения
  const newVisible = [...visibleRecommended];

  // Кол-во для замены — минимум из 3 и количества кандидатов
  const replaceCount = Math.min(3, candidates.length);

  for (let i = 0; i < replaceCount; i++) {
    // Случайный кандидат
    const randomIndex = Math.floor(Math.random() * candidates.length);
    newVisible[i] = candidates[randomIndex];
    candidates.splice(randomIndex, 1);
  }

  setVisibleRecommended(newVisible);
  // setLastVisibleIds(newVisible.map(r => r.id));
};


  const handleSearch = () => {
    const trimmed = location.trim();
    if (trimmed) {
      setShowSuggestions(false);
      router.push(`/search?query=${encodeURIComponent(trimmed)}`);
    }
  };

  // Закрыть подсказки, если клик вне поля ввода или подсказок
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />

      <main className="flex-1 py-12 px-10 relative">
        <h1 className="text-4xl font-bold text-center mb-6 text-blue-900 drop-shadow">Путешествия</h1>

        <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-6 max-w-3xl mx-auto relative">
          <input
            type="text"
            ref={inputRef}
            placeholder="Введите пункт назначения или фильтр..."
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              setShowSuggestions(true);
            }}
            onFocus={() => setShowSuggestions(true)}
            className="w-full md:w-2/3 px-4 py-2 shadow-md rounded-2xl border"
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            autoComplete="off"
          />
          <button
            onClick={handleSearch}
            className="px-6 py-2 rounded-2xl text-lg shadow-md bg-blue-600 hover:bg-blue-700 text-white"
          >
            Поиск
          </button>

          {/* Подсказки */}
          {showSuggestions && filteredSuggestions.length > 0 && (
            <ul className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-b-xl shadow-lg max-w-md mx-auto mt-1 z-20">
              {filteredSuggestions.map(route => (
                <li
                  key={route.id}
                  className="px-4 py-2 hover:bg-blue-100 cursor-pointer"
                  onMouseDown={() => { // onMouseDown чтобы избежать потери фокуса input
                    setLocation(route.title);
                    setShowSuggestions(false);
                  }}
                >
                  {route.title}
                </li>
              ))}
            </ul>
          )}
        </div>

        <h2 className="text-2xl font-semibold text-blue-800 text-center mb-4">Рекомендуемые маршруты</h2>
        <div className="flex items-center justify-center gap-6 mb-6 max-w-5xl mx-auto">
          {visibleRecommended.map((route) => (
            <Link
              key={route.id}
              href={`/routes/${route.id}`}
              className="flex-1 block p-6 bg-white shadow-md rounded-2xl border border-blue-100 hover:scale-[1.02] transition-transform duration-300 cursor-pointer"
              style={{ minWidth: '220px', minHeight: '150px' }}
            >
              <h3 className="text-lg font-semibold text-blue-700 break-words">{route.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed">{route.description}</p>
            </Link>
          ))}
        </div>

        <div className="flex justify-center mb-10">
          <button
            onClick={handleShuffle}
            className="px-10 py-3 rounded-2xl text-lg shadow-md bg-green-600 hover:bg-green-700 text-white"
            title="Обновить рекомендуемые маршруты"
          >
            Обновить
          </button>
        </div>
      </main>
    </div>
  );
}
