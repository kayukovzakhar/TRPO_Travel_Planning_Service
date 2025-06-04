import { useRouter } from "next/router";
import Link from "next/link";
import React from "react";
import { routeDetails } from "../data/routesData";
import Sidebar from "../components/Sidebar";  // Импортируем Sidebar

export default function SearchPage() {
  const router = useRouter();
  const { query } = router.query;

  const allRoutes = React.useMemo(() => {
    return Object.entries(routeDetails).map(([slug, data]) => ({
      id: slug,
      ...data,
    }));
  }, []);

  const filteredRoutes = React.useMemo(() => {
    if (!query || typeof query !== "string") return [];
    return allRoutes.filter(route =>
      route.title.toLowerCase().includes(query.toLowerCase())
    );
  }, [query, allRoutes]);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />
      <main className="flex-1 py-12 px-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-blue-900">Результаты поиска</h1>

        {filteredRoutes.length > 0 ? (
          <div className="grid grid-cols-1 gap-6">
            {filteredRoutes.map(route => (
              <Link
                key={route.id}
                href={`/routes/${route.id}`}
                className="block p-6 bg-white shadow-md rounded-2xl border border-blue-100 hover:scale-[1.01] transition-transform duration-300"
              >
                <h3 className="text-lg font-semibold text-blue-700">{route.title}</h3>
                <p className="text-sm text-gray-600 leading-relaxed">{route.description}</p>
              </Link>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">Маршруты по вашему запросу не найдены.</p>
        )}

        <Link href="/" className="inline-block mt-8 text-blue-600 underline">
          ← Вернуться на главную
        </Link>
      </main>
    </div>
  );
}
