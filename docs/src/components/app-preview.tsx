"use client";

import { useState } from "react";
import Image from "next/image";

interface AppPreviewProps {
  lang: "pt" | "en";
}

const TABS = [
  {
    id: "store",
    labelPt: "Loja de Jogos",
    labelEn: "Game Store",
    src: "/assets/Store.png",
    descPt: "Explore e baixe jogos de todas as regiões em poucos cliques.",
    descEn: "Browse and download games from all regions in just a few clicks.",
  },
  {
    id: "installed",
    labelPt: "Jogos Instalados",
    labelEn: "Installed Games",
    src: "/assets/InstalledGames.png",
    descPt: "Gerencie sua biblioteca instalada diretamente pelo app.",
    descEn: "Manage your installed library directly from the app.",
  },
] as const;

export default function AppPreview({ lang }: AppPreviewProps) {
  const [active, setActive] = useState<"store" | "installed">("store");
  const current = TABS.find((t) => t.id === active)!;

  return (
    <section className="py-[100px] relative z-10 px-8" id="preview">
      <div className="max-w-[1100px] mx-auto">
        {/* Heading */}
        <div className="text-center mb-16 scroll-reveal">
          <h2 className="font-outfit text-5xl font-extrabold">
            {lang === "pt" ? (
              <>
                Veja o App em{" "}
                <span className="accent-text">Ação</span>
              </>
            ) : (
              <>
                See the App in{" "}
                <span className="accent-text">Action</span>
              </>
            )}
          </h2>
          <p className="text-muted-foreground mt-4 text-lg max-w-xl mx-auto">
            {lang === "pt"
              ? "Interface moderna construída para a comunidade PSP."
              : "Modern interface built for the PSP community."}
          </p>
        </div>

        {/* Window frame */}
        <div className="scroll-reveal liquid-glass rounded-[20px] overflow-hidden shadow-[0_30px_80px_rgba(0,0,0,0.6),0_0_0_1px_rgba(255,255,255,0.08)]">
          {/* Title bar */}
          <div
            className="flex items-center gap-4 px-5 py-3 border-b border-white/10"
            style={{ background: "rgba(10,5,20,0.85)" }}
          >
            {/* Traffic lights */}
            <div className="flex gap-1.5 shrink-0">
              <div className="w-3 h-3 rounded-full bg-[#ff5f57] shadow-[0_0_6px_rgba(255,95,87,0.6)]" />
              <div className="w-3 h-3 rounded-full bg-[#ffbd2e] shadow-[0_0_6px_rgba(255,189,46,0.5)]" />
              <div className="w-3 h-3 rounded-full bg-[#28c840] shadow-[0_0_6px_rgba(40,200,64,0.5)]" />
            </div>

            {/* App title */}
            <span className="text-white/40 text-xs font-mono flex-1 text-center select-none">
              PSP FreeShop Enhanced
            </span>

            {/* Tabs */}
            <div className="flex gap-1 shrink-0">
              {TABS.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActive(tab.id)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 ${
                    active === tab.id
                      ? "bg-[#9d4edd]/25 text-white border border-[#9d4edd]/40 shadow-[0_0_12px_rgba(157,78,221,0.2)]"
                      : "text-white/40 hover:text-white/70 border border-transparent"
                  }`}
                >
                  {lang === "pt" ? tab.labelPt : tab.labelEn}
                </button>
              ))}
            </div>
          </div>

          {/* Screenshot */}
          <div className="relative bg-[#080415]">
            <Image
              key={current.src}
              src={current.src}
              alt={lang === "pt" ? current.labelPt : current.labelEn}
              width={1100}
              height={700}
              className="w-full h-auto block"
              style={{ animation: "previewFadeIn 0.35s ease" }}
              priority={active === "store"}
            />
            {/* Bottom caption bar */}
            <div
              className="absolute bottom-0 left-0 right-0 px-6 py-3 flex items-center gap-3"
              style={{
                background:
                  "linear-gradient(0deg, rgba(5,2,15,0.9) 0%, transparent 100%)",
              }}
            >
              <div className="w-2 h-2 rounded-full bg-[#9d4edd] shadow-[0_0_8px_#9d4edd] shrink-0" />
              <p className="text-white/60 text-sm">
                {lang === "pt" ? current.descPt : current.descEn}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
