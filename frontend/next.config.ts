import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // строгий режим React
  reactStrictMode: true,

  output: "export",

  // При желании можно указать базовый путь (если сайт будет в подкаталоге):
  // basePath: "/my-static-site",

  // Все API-запросы отключены
};

export default nextConfig;
