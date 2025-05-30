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
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  const filteredSuggestions = location.trim()
    ? routesArray
        .filter((r) =>
          r.title.toLowerCase().includes(location.toLowerCase())
        )
        .slice(0, 3)
    : [];

  const handleShuffle = () => {
    setVisibleRecommended(shuffleArray(routesArray).slice(0, 3));
  };

  const handleSearch = () => {
    const trimmed = location.trim();
    if (trimmed) {
      setShowSuggestions(false);
      router.push(`/search?query=${encodeURIComponent(trimmed)}`);
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
          {showSuggestions && filteredSuggestions.length > 0 && (
            <ul className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-b-xl shadow-lg max-w-md mx-auto mt-1 z-20">
              {filteredSuggestions.map((route) => (
                <li
                  key={route.slug}
                  className="px-4 py-2 hover:bg-blue-100 cursor-pointer"
                  onMouseDown={() => {
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

        {/* Рекомендованные маршруты */}
        <h2 className="text-2xl font-semibold text-blue-800 text-center mb-4">
          Рекомендуемые маршруты
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {visibleRecommended.map((route) => (
            <Link
              key={route.slug}
              href={`/routes/${route.slug}`}
              className="block p-6 bg-white shadow-md rounded-2xl border border-blue-100 hover:scale-[1.02] transition-transform duration-300 cursor-pointer"
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
            className="px-10 py-3 rounded-2xl text-lg shadow-md bg-green-600 hover:bg-green-700 text-white"
          >
            Обновить
          </button>
        </div>
      </main>
    </div>
  );
}
