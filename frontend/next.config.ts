import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',  // <-- добавьте эту строку
};

export default nextConfig;
