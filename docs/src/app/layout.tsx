import type { Metadata } from "next";
import { Inter, Outfit, Orbitron } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const outfit = Outfit({ subsets: ["latin"], variable: "--font-outfit" });
const orbitron = Orbitron({ subsets: ["latin"], weight: ["600", "900"], variable: "--font-orbitron" });

export const metadata: Metadata = {
  title: "pspFreeShop Enhanced — Onde a nostalgia e o moderno se encontram",
  description: "Explore, baixe e instale jogos, DLCs e atualizações dos repositórios oficiais diretamente no seu console com apenas um clique.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${outfit.variable} ${orbitron.variable} antialiased min-h-screen bg-background font-sans dark custom-scrollbar`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
