import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,

  // вот этот блок добавляем или расширяем
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },
};

export default nextConfig;
