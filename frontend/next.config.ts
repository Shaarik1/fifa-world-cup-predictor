import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        // MAKE SURE YOU PASTE YOUR REAL RENDER URL BELOW
        destination: "https://fifa-world-cup-predictor.onrender.com", 
      },
    ];
  },
};

export default nextConfig;
