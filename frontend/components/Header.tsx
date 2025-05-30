import React, { useEffect, useState } from "react"
import Link from "next/link"
import axios from "axios"

axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;  // обязательно!

interface IUser {
  email: string
  // другие поля по необходимости
}

export const Header: React.FC = () => {
  const [user, setUser] = useState<IUser | null>(null)

  // По монтированию пытаемся получить информацию о текущем пользователе
  useEffect(() => {
    axios
      .get<IUser>("/api/v1/auth/me", { withCredentials: true })
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
  }, [])

  const handleLogout = () => {
    axios.post("/api/v1/auth/logout", {}, { withCredentials: true })
      .then(() => {
        setUser(null)
        // можно дополнительно редиректить на главную
      })
  }

  return (
    <header className="w-full bg-white shadow py-3 px-6 flex justify-between items-center">
      <Link href="/">
    <span className="text-2xl font-bold text-blue-800">Travelelo Tralala</span>
      </Link>

      <div>
        {user ? (
          <div className="flex items-center gap-4">
            <span className="text-gray-700">Привет, {user.email}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Выйти
            </button>
          </div>
        ) : (
          <Link href="/login">
            <button className="px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
              Войти
            </button>
          </Link>
        )}
      </div>
    </header>
  )
}
