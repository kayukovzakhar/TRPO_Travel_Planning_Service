import { useRouter } from "next/router";
import Link from "next/link";
import { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { routeDetails, ChecklistItem } from "../../data/routesData";
import { Button } from "../../components/ui/button";

export default function RoutePage() {
  const router = useRouter();
  const { id } = router.query;

  const routeKey =
    typeof id === "string" && id in routeDetails
      ? (id as keyof typeof routeDetails)
      : null;

  const [checked, setChecked] = useState<boolean[]>([]);
  const [visibleIndexes, setVisibleIndexes] = useState<number[]>([]);
  const [shownIndexes, setShownIndexes] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (routeKey) {
      const total = routeDetails[routeKey].checklist.length;
      setChecked(new Array(total).fill(false));
      const initial = getRandomIndexes(total, new Set(), Math.min(6, total));
      setVisibleIndexes(initial);
      setShownIndexes(new Set(initial));
    }
  }, [routeKey]);

  const toggleCheck = (index: number) => {
    setChecked((prev) => {
      const copy = [...prev];
      copy[index] = !copy[index];
      return copy;
    });
  };

  const getRandomIndexes = (total: number, exclude: Set<number>, count: number): number[] => {
    const available = [...Array(total).keys()].filter((i) => !exclude.has(i));
    const shuffled = available.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  };

  const replaceOne = (indexToReplace: number) => {
    if (!routeKey) return;
    const total = routeDetails[routeKey].checklist.length;
    const exclude = new Set(visibleIndexes);
    const candidates = getRandomIndexes(total, exclude, 1);
    if (candidates.length === 0) return;
    const newIndex = candidates[0];

    const updated = [...visibleIndexes];
    updated[indexToReplace] = newIndex;
    setVisibleIndexes(updated);
    setShownIndexes((prev) => new Set([...prev, newIndex]));
  };

  const reloadAll = () => {
    if (!routeKey) return;
    const total = routeDetails[routeKey].checklist.length;
    const count = Math.min(6, total);
    const newSet = getRandomIndexes(total, new Set(), count);
    setVisibleIndexes(newSet);
    setShownIndexes(new Set(newSet));
  };

  const [isBookmarked, setIsBookmarked] = useState(false);
  const [currentBookmarkId, setCurrentBookmarkId] = useState<number | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token") || "";
    fetch("/api/v1/bookmarks", {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Не удалось загрузить закладки");
        return res.json();
      })
      .then((data: { id: number; route_slug: string }[]) => {
        const bm = data.find((b) => b.route_slug === routeKey);
        if (bm) {
          setIsBookmarked(true);
          setCurrentBookmarkId(bm.id);
        }
      })
      .catch(console.error);
  }, [routeKey]);

  const addBookmark = async () => {
    if (!routeKey) return;
    try {
      const token = localStorage.getItem("token") || "";
      const res = await fetch("/api/v1/bookmarks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ route_slug: routeKey }),
      });
      if (!res.ok) throw new Error("Не удалось сохранить маршрут");
      const bm = await res.json();
      setIsBookmarked(true);
      setCurrentBookmarkId(bm.id);
    } catch (e) {
      console.error(e);
      alert("Ошибка сохранения маршрута");
    }
  };

  const removeBookmark = async () => {
    if (!currentBookmarkId) return;
    try {
      const token = localStorage.getItem("token") || "";
      const res = await fetch(`/api/v1/bookmarks/${currentBookmarkId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (res.status !== 204) throw new Error("Не удалось удалить закладку");
      setIsBookmarked(false);
      setCurrentBookmarkId(null);
    } catch (e) {
      console.error(e);
      alert("Ошибка удаления из закладок");
    }
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
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-4xl font-bold text-blue-900">{title}</h1>
          {isBookmarked ? (
            <Button variant="destructive" onClick={removeBookmark}>
              Убрать из закладок
            </Button>
          ) : (
            <Button onClick={addBookmark}>Сохранить маршрут</Button>
          )}
        </div>

        <p className="text-lg mb-6 text-gray-700">{description}</p>
        <p className="mb-8 text-gray-600">{details}</p>

        <div className="flex justify-end mb-6">
          <Button onClick={reloadAll} className="flex items-center gap-2">
            <span className="text-xl">🔄</span> Обновить подборку
            </Button>
            </div>


        <div className="flex flex-col gap-6">
          {visibleIndexes.map((i, idx) => {
            const item = checklist[i];
            return (
              <div key={i} className="relative">
                <button
                  onClick={() => toggleCheck(i)}
                  className={`w-full text-left flex items-center gap-4 p-6 rounded-2xl border shadow-md transition-colors duration-300 ${
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
                  <div>
                    <h3 className="text-xl font-semibold text-blue-800">{item.title}</h3>
                    <p className="text-gray-600">{item.description}</p>
                  </div>
                </button>
                <button
                onClick={() => replaceOne(idx)}
                 className="absolute top-3 right-3 p-1.5 bg-white border border-gray-300 rounded-full shadow hover:bg-blue-50 transition"
                 title="Заменить место"> 🔁 </button>

              </div>
            );
          })}
        </div>

        <Link href="/" className="inline-block mt-10 text-blue-600 underline">
          ← Назад на главную
        </Link>
      </main>
    </div>
  );
}
