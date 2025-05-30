import { useState } from "react";
import { useRouter } from "next/router";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error("Invalid credentials");
      const { access_token } = await res.json();
      // сохраняем JWT в localStorage
      localStorage.setItem("token", access_token);
      router.push("/");
    } catch (err) {
      alert("Ошибка логина");
      console.error(err);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-blue-50">
      <form onSubmit={handleSubmit} className="p-6 bg-white rounded-2xl shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-4">Вход</h1>
        <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
            className="mb-4"
        />
        <Input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mb-6"
        />
        <Button type="submit" className="w-full">Войти</Button>
      </form>
    </main>
  );
}
