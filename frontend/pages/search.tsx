import { useRouter } from "next/router";
import Link from "next/link";
import React from "react";
import { routeDetails } from "../data/routesData";
// import Sidebar from "../components/Sidebar"

const categories = [
  { id: "all", name: "Все" },
  { id: "nature", name: "Природа" },
  { id: "culture", name: "Культура" },
  { id: "adventure", name: "Приключения" },
  { id: "relax", name: "Отдых" },
];

export default function SearchPage() {
  const router = useRouter();
  const { query, category = "all" } = router.query;

  const filteredRoutes = React.useMemo(() => {
    if (!query || typeof query !== "string") return [];
    return Object.entries(routeDetails)
      .map(([slug, data]) => ({
        slug,
        ...data,
      }))
      .filter(route => {
        const matchesSearch = 
          route.title.toLowerCase().includes(query.toLowerCase()) ||
          route.description.toLowerCase().includes(query.toLowerCase());
        const matchesCategory = category === "all" || route.category === category;
        return matchesSearch && matchesCategory;
      });
  }, [query, category]);

  const handleCategoryChange = (newCategory: string) => {
    router.push({
      pathname: router.pathname,
      query: { ...router.query, category: newCategory }
    });
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 to-white py-12 px-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-blue-900">Результаты поиска</h1>

      {/* Категории */}
      <div className="flex flex-wrap gap-2 justify-center mb-8">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => handleCategoryChange(cat.id)}
            className={`px-4 py-2 rounded-full text-sm transition-all duration-200 ${
              category === cat.id
                ? "bg-blue-600 text-white shadow-md"
                : "bg-white text-gray-600 hover:bg-blue-50"
            }`}
          >
            {cat.name}
          </button>
        ))}
      </div>

      {filteredRoutes.length > 0 ? (
        <div className="grid grid-cols-1 gap-6">
          {filteredRoutes.map(route => (
            <Link
              key={route.slug}
              href={`/routes/${route.slug}`}
              className="block p-6 bg-white shadow-md rounded-2xl border border-blue-100 hover:scale-[1.01] transition-all duration-300 hover:shadow-lg"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-blue-700">{route.title}</h3>
                  <p className="text-sm text-gray-600 leading-relaxed">{route.description}</p>
                </div>
                <span className="px-3 py-1 text-xs rounded-full bg-blue-100 text-blue-700">
                  {categories.find(c => c.id === route.category)?.name}
                </span>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg mb-4">Маршруты по вашему запросу не найдены.</p>
          <p className="text-gray-500">Попробуйте изменить параметры поиска или выбрать другую категорию.</p>
        </div>
      )}

      <Link 
        href="/" 
        className="inline-block mt-8 text-blue-600 hover:text-blue-800 transition-colors duration-200"
      >
        ← Вернуться на главную
      </Link>
    </main>
  );
}
