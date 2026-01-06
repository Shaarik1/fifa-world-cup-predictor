import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        // IMPORTANT: Keep the /:path* at the very end of this line!
        destination: "https://fifa-world-cup-predictor.onrender.com/:path*", 
      },
    ];
  },
};

export default nextConfig;
