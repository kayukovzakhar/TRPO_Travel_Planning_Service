// frontend/pages/index.tsx

import React, { useState, useRef, useEffect, useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { routeDetails } from "../data/routesData";
import Sidebar from "../components/Sidebar";

function shuffleArray<T>(array: T[]): T[] {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

// Категории для фильтрации
const categories = [
  { id: "all", name: "Все" },
  { id: "nature", name: "Природа" },
  { id: "culture", name: "Культура" },
  { id: "adventure", name: "Приключения" },
  { id: "relax", name: "Отдых" },
];

export default function Home() {
  // Стабильный массив маршрутов (slug + данные)
  const routesArray = useMemo(
    () =>
      Object.entries(routeDetails).map(([slug, data]) => ({
        slug,
        ...data,
      })),
    []
  );

  // Начальное состояние — первые три маршрута (SSR и клиент одинаково)
  const [visibleRecommended, setVisibleRecommended] = useState(
    () => routesArray.slice(0, 3)
  );

  // После монтирования на клиенте раз в useEffect делаем случайные три
  useEffect(() => {
    setVisibleRecommended(shuffleArray(routesArray).slice(0, 3));
  }, [routesArray]);

  const [location, setLocation] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  const filteredSuggestions = location.trim()
    ? routesArray
        .filter((r) => {
          const matchesSearch = 
            r.title.toLowerCase().includes(location.toLowerCase()) ||
            r.description.toLowerCase().includes(location.toLowerCase());
          const matchesCategory = selectedCategory === "all" || r.category === selectedCategory;
          return matchesSearch && matchesCategory;
        })
        .slice(0, 5)
    : [];

  const handleShuffle = () => {
    setVisibleRecommended(shuffleArray(routesArray).slice(0, 3));
  };

  const handleSearch = () => {
    const trimmed = location.trim();
    if (trimmed) {
      setShowSuggestions(false);
      router.push(`/search?query=${encodeURIComponent(trimmed)}&category=${selectedCategory}`);
    }
  };

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
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />
      <main className="flex-1 py-12 px-10 relative">
        <h1 className="text-4xl font-bold text-center mb-6 text-blue-900 drop-shadow">
          Путешествия
        </h1>

        {/* Поисковая строка */}
        <div className="flex flex-col items-center justify-center gap-4 mb-6 max-w-3xl mx-auto relative">
          <div className="w-full flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
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
                className="w-full px-4 py-3 shadow-md rounded-2xl border border-blue-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                autoComplete="off"
              />
              {showSuggestions && filteredSuggestions.length > 0 && (
                <ul className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-xl shadow-lg mt-1 z-20 transform transition-all duration-200 ease-in-out">
                  {filteredSuggestions.map((route) => (
                    <li
                      key={route.slug}
                      className="px-4 py-3 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 transition-colors duration-150"
                      onMouseDown={() => {
                        setLocation(route.title);
                        setShowSuggestions(false);
                      }}
                    >
                      <div className="font-medium text-blue-700">{route.title}</div>
                      <div className="text-sm text-gray-600 truncate">{route.description}</div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <button
              onClick={handleSearch}
              className="px-6 py-3 rounded-2xl text-lg shadow-md bg-blue-600 hover:bg-blue-700 text-white transition-colors duration-200"
            >
              Поиск
            </button>
          </div>
          
          {/* Категории */}
          <div className="flex flex-wrap gap-2 justify-center mt-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-full text-sm transition-all duration-200 ${
                  selectedCategory === category.id
                    ? "bg-blue-600 text-white shadow-md"
                    : "bg-white text-gray-600 hover:bg-blue-50"
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Рекомендованные маршруты */}
        <h2 className="text-2xl font-semibold text-blue-800 text-center mb-4">
          Рекомендуемые маршруты
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {visibleRecommended.map((route) => (
            <Link
              key={route.slug}
              href={`/routes/${route.slug}`}
              className="block p-6 bg-white shadow-md rounded-2xl border border-blue-100 hover:scale-[1.02] transition-all duration-300 cursor-pointer hover:shadow-lg"
            >
              <h3 className="text-lg font-semibold text-blue-700">
                {route.title}
              </h3>
              <p className="text-sm text-gray-600">{route.description}</p>
            </Link>
          ))}
        </div>

        <div className="flex justify-center mt-8">
          <button
            onClick={handleShuffle}
            className="px-10 py-3 rounded-2xl text-lg shadow-md bg-green-600 hover:bg-green-700 text-white transition-colors duration-200"
          >
            Обновить
          </button>
        </div>
      </main>
    </div>
  );
}
