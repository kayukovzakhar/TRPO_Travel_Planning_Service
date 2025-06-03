import { useEffect, useState } from "react";
import Link from "next/link";
import Sidebar from "../components/Sidebar";
import { routeDetails } from "../data/routesData";
import { Card, CardContent } from "../components/ui/card";

interface Bookmark {
  id: number;
  route_slug: string;
}

export default function SavedRoutes() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("token") || "";
    fetch("/api/v1/bookmarks", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(data => setBookmarks(data))
      .catch(console.error);
  }, []);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />

      <main className="flex-1 py-12 px-10 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-900 mb-6">Сохранённые маршруты</h1>

        <div className="grid gap-6">
          {bookmarks.map((bm) => {
            const route = routeDetails[bm.route_slug as keyof typeof routeDetails];

            if (!route) return null;

            return (
              <Link href={`/routes/${bm.route_slug}`} key={bm.id}>
                <Card className="cursor-pointer hover:shadow-lg transition-shadow duration-300">
                  <CardContent>
                    <h2 className="text-xl font-semibold text-blue-800">{route.title}</h2>
                    <p className="text-gray-600">{route.description}</p>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>

        {bookmarks.length === 0 && (
          <p className="text-gray-600 mt-10">У вас пока нет сохранённых маршрутов.</p>
        )}
      </main>
    </div>
  );
}
