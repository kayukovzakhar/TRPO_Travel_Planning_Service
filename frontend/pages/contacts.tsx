import Sidebar from "../components/Sidebar";

export default function Contacts() {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-100 to-white">
      <Sidebar />
      <main className="flex-1 p-10 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6 text-blue-900">Контакты</h1>
        <p className="text-lg text-gray-700 leading-relaxed">
          Свяжитесь с нами по электронной почте: kayukovzakhar@mail.ru <br />
          Или по телефону: +7 (900) 115-**-**
        </p>
      </main>
    </div>
  );
}
