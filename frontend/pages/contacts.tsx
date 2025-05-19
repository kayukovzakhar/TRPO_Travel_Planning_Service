import Sidebar from "../components/Sidebar"

export default function Contacts() {
  return (
    <main className="min-h-screen p-10 bg-gradient-to-br from-blue-100 to-white max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-6 text-blue-900">Контакты</h1>
      <p className="text-lg text-gray-700 leading-relaxed">
        Свяжитесь с нами по электронной почте: travel@example.com <br />
        Или по телефону: +7 (123) 456-78-90
      </p>
    </main>
  )
}
