import React from "react"
import Link from "next/link"

export const Header: React.FC = () => {
  return (
    <header className="w-full bg-white shadow py-3 px-6 flex justify-between items-center">
      <Link href="/">
        <span className="text-2xl font-bold text-blue-800">Travelelo Tralala</span>
      </Link>
    </header>
  )
}
