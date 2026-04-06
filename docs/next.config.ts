import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/pspFreeShop",
  assetPrefix: "/pspFreeShop",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
