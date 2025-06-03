import { useRouter } from "next/router";
import Link from "next/link";
import { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { routeDetails } from "../../data/routesData";
import { Route } from "../../types/route";

export default function RoutePage() {
  const router = useRouter();
  const { id } = router.query;

  const routeKey =
    typeof id === "string" && id in routeDetails
      ? (id as keyof typeof routeDetails)
      : null;

  const [checked, setChecked] = useState<boolean[]>([]);
  useEffect(() => {
    if (routeKey && routeDetails[routeKey].checklist) {
      setChecked(new Array(routeDetails[routeKey].checklist!.length).fill(false));
    }
  }, [routeKey]);

  const toggleCheck = (index: number) => {
    setChecked((prev) => {
      const copy = [...prev];
      copy[index] = !copy[index];
      return copy;
    });
  };

  if (!routeKey) {
    return (
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-4">Маршрут не найден</h1>
        <Link href="/" className="text-blue-600 underline">
          Вернуться на главную
        </Link>
      </div>
    );
  }

  const { title, description, details, checklist } = routeDetails[routeKey];

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />
      <main className="flex-1 py-12 px-10 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-900 mb-6">{title}</h1>
        <p className="text-lg mb-6 text-gray-700">{description}</p>
        <p className="mb-8 text-gray-600">{details}</p>

        {checklist && (
          <div className="flex flex-col gap-6">
            {checklist.map((item, i) => (
              <button
                key={i}
                onClick={() => toggleCheck(i)}
                className={`flex items-center gap-4 p-6 rounded-2xl border shadow-md transition-colors duration-300 ${
                  checked[i]
                    ? "bg-green-100 border-green-500"
                    : "bg-white border-gray-300 hover:bg-blue-50"
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
        )}

        <Link href="/" className="inline-block mt-10 text-blue-600 underline">
          ← Назад на главную
        </Link>
      </main>
    </div>
  );
}
