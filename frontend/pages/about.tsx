import Sidebar from "../components/Sidebar";

export default function About() {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />
      <main className="flex-1 p-10 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6 text-blue-900">О проекте</h1>
        <p className="text-lg text-gray-700 leading-relaxed">
          Этот проект создан для планирования путешествий по России с удобным поиском и рекомендованными маршрутами.
          Здесь вы можете найти интересные направления и получить персональные предложения.
        </p>
      </main>
    </div>
  );
}
