import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-44 bg-blue-900 text-white p-6 flex flex-col min-h-screen">
      <h2 className="text-2xl font-bold mb-6">Меню</h2>
      <nav className="flex flex-col gap-4">
        <Link href="/" className="hover:underline">Главная</Link>
        <Link href="/about" className="hover:underline">О проекте</Link>
        <Link href="/contacts" className="hover:underline">Контакты</Link>
      </nav>
    </aside>
  );
}
