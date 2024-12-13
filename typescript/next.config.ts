import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["@boundaryml/baml"],
  webpack: (config) => {
    config.module.rules.push({
      test: /\.node$/,
      use: [
        {
          loader: "nextjs-node-loader",
          options: {
            outputPath: config.output.path,
          },
        },
      ],
    });

    // You can ignore this block -- it's just to run the baml compiler on the web for the PDF demo:
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
      syncWebAssembly: true,
      layers: true,
      topLevelAwait: true,
    };

    return config;
  },
};

export default nextConfig;
