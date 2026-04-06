"use client";

import {
  Gamepad2,
  PackagePlus,
  RefreshCcw,
  Zap,
  Download,
  Heart,
  Coffee,
  ExternalLink,
  ChevronDown,
} from "lucide-react";
import ParticlesBackground from "@/components/ui/particles-bg";
import AppPreview from "@/components/app-preview";
import { useState, useRef } from "react";

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden="true">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}
import { useScrollReveal } from "@/hooks/use-scroll-reveal";

// PSP button symbol colours (PlayStation palette)
const PSP_SYMBOLS = [
  { sym: "×", cls: "psp-sym psp-sym-cross", style: { top: "18%", left: "6%" , animationDelay: "0s"   } },
  { sym: "○", cls: "psp-sym psp-sym-circle", style: { top: "55%", left: "88%", animationDelay: "2.5s" } },
  { sym: "□", cls: "psp-sym psp-sym-square", style: { top: "78%", left: "5%" , animationDelay: "5s"   } },
  { sym: "△", cls: "psp-sym psp-sym-tri",    style: { top: "12%", left: "80%", animationDelay: "7.5s" } },
];

// PlayStation-style button badge per feature card
const FEATURE_BADGES = ["○", "□", "△", "×"] as const;
const BADGE_COLORS   = [
  "text-[#e80000]",   // circle  — red
  "text-[#e5007a]",   // square  — pink
  "text-[#00a86b]",   // triangle — green
  "text-[#0070d1]",   // cross   — blue
] as const;

function SpotlightCard({
  children,
  className = "",
  style,
}: {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) {
  const ref = useRef<HTMLDivElement>(null);

  const onMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    ref.current.style.setProperty("--mouse-x", `${e.clientX - rect.left}px`);
    ref.current.style.setProperty("--mouse-y", `${e.clientY - rect.top}px`);
  };

  return (
    <div
      ref={ref}
      className={`feature-card liquid-glass ${className}`}
      style={style}
      onMouseMove={onMouseMove}
    >
      {children}
    </div>
  );
}

export default function Home() {
  const [lang, setLang] = useState<"pt" | "en">("pt");
  useScrollReveal();

  return (
    <>
      <ParticlesBackground />

      {/* ── Navigation ── */}
      <nav className="glass-nav font-sans">
        <div className="max-w-[1200px] mx-auto h-[76px] flex justify-between items-center px-8">
          <div className="logo-text font-orbitron text-xl font-black tracking-tighter uppercase drop-shadow-[0_0_20px_rgba(157,78,221,0.55)]">
            pspFreeShop{" "}
            <span className="accent-text">Enhanced</span>
          </div>
          <div className="flex items-center gap-3">
            {/* Nav links */}
            <a href="#preview" className="hidden md:flex items-center gap-1.5 text-white/50 hover:text-white/90 text-sm transition-colors px-3 py-2">
              {lang === "pt" ? "Preview" : "Preview"}
            </a>
            <a href="#features" className="hidden md:flex items-center gap-1.5 text-white/50 hover:text-white/90 text-sm transition-colors px-3 py-2">
              {lang === "pt" ? "Funcionalidades" : "Features"}
            </a>
            <a href="#guide" className="hidden md:flex items-center gap-1.5 text-white/50 hover:text-white/90 text-sm transition-colors px-3 py-2">
              {lang === "pt" ? "Guia" : "Guide"}
            </a>

            <div className="w-px h-5 bg-white/10 mx-1 hidden md:block" />

            <button onClick={() => setLang((p) => (p === "pt" ? "en" : "pt"))} className="glass-btn">
              {lang === "pt" ? "EN" : "PT"}
            </button>
            <a
              href="https://github.com/marcosferreirarj/pspFreeShop/releases"
              className="btn-primary glass-btn"
            >
              <Download className="w-4 h-4" />
              Download
            </a>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative pt-[180px] pb-[80px] text-center z-10 px-8 overflow-hidden">
        {/* PSP floating button symbols */}
        {PSP_SYMBOLS.map(({ sym, cls, style }) => (
          <span key={sym} className={cls} style={style}>
            {sym}
          </span>
        ))}

        {/* XMB-inspired horizontal glow line */}
        <div
          className="absolute left-0 right-0 pointer-events-none"
          style={{
            top: "52%",
            height: "1px",
            background:
              "linear-gradient(90deg,transparent 0%,rgba(0,245,255,0.08) 25%,rgba(157,78,221,0.12) 50%,rgba(0,245,255,0.08) 75%,transparent 100%)",
          }}
        />

        <div className="max-w-[1200px] mx-auto">
          {/* Badge */}
          <div className="hero-enter" data-delay="1">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold text-[#00f5ff] border border-[#00f5ff]/20 bg-[#00f5ff]/5 mb-8">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00f5ff] shadow-[0_0_6px_#00f5ff] inline-block" style={{animation: "pulse-glow 2s ease-in-out infinite"}} />
              {lang === "pt" ? "Versão Estável Disponível" : "Stable Version Available"}
            </span>
          </div>

          <h1
            className="hero-enter font-outfit text-5xl md:text-7xl lg:text-[5.2rem] font-black leading-tight mb-6 drop-shadow-[0_10px_30px_rgba(0,0,0,0.6)]"
            data-delay="2"
          >
            {lang === "pt" ? (
              <>
                O melhor do PSP
                <br />
                <span className="gradient-text">Na palma da mão</span>
              </>
            ) : (
              <>
                The Best of PSP
                <br />
                <span className="gradient-text">In your hands</span>
              </>
            )}
          </h1>

          <p
            className="hero-enter text-[1.2rem] text-muted-foreground max-w-[720px] mx-auto mb-12 font-light leading-relaxed"
            data-delay="3"
          >
            {lang === "pt" ? (
              <>
                Explore, baixe e instale jogos, DLCs e atualizações dos
                repositórios oficiais diretamente no seu console com apenas um
                clique.
              </>
            ) : (
              <>
                Explore, download, and install games, DLCs, and updates from
                official repositories directly to your console with just one
                click.
              </>
            )}
          </p>

          <div className="hero-enter flex flex-col sm:flex-row gap-4 justify-center" data-delay="4">
            <a
              href="https://github.com/marcosferreirarj/pspFreeShop/releases"
              className="inline-flex items-center justify-center gap-2.5 px-10 py-4 text-base btn-primary text-white rounded-[18px] font-semibold"
            >
              <Download className="w-5 h-5" />
              {lang === "pt" ? "Baixar Versão Estável" : "Download Official Release"}
            </a>
            <a
              href="https://github.com/marcosferreirarj/pspFreeShop"
              className="inline-flex items-center justify-center gap-2.5 px-10 py-4 text-base glass-btn rounded-[18px] font-semibold"
            >
              <GithubIcon className="w-5 h-5" />
              GitHub
            </a>
          </div>

          {/* Scroll hint */}
          <div className="mt-16 flex flex-col items-center gap-2 text-white/25 text-xs">
            <span>{lang === "pt" ? "rolar para explorar" : "scroll to explore"}</span>
            <ChevronDown className="w-4 h-4 animate-bounce" />
          </div>
        </div>
      </section>

      {/* ── XMB Divider ── */}
      <div className="xmb-divider mx-8 my-2" />

      {/* ── App Preview ── */}
      <AppPreview lang={lang} />

      {/* ── XMB Divider ── */}
      <div className="xmb-divider mx-8 my-2" />

      {/* ── Features ── */}
      <section className="py-[100px] relative z-10" id="features">
        <div className="max-w-[1200px] mx-auto px-8">
          <div className="text-center mb-20 scroll-reveal">
            <h2 className="font-outfit text-5xl font-extrabold">
              {lang === "pt" ? (
                <>
                  Funcionalidades{" "}
                  <span className="accent-text">Premium</span>
                </>
              ) : (
                <>
                  Premium{" "}
                  <span className="accent-text">Features</span>
                </>
              )}
            </h2>
            <p className="text-muted-foreground mt-4 text-lg max-w-xl mx-auto">
              {lang === "pt"
                ? "Tudo que você precisa para aproveitar seu PSP ao máximo."
                : "Everything you need to get the most out of your PSP."}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: <Gamepad2 className="w-9 h-9 drop-shadow-[0_0_8px_rgba(157,78,221,0.7)]" />,
                titlePt: "Biblioteca Completa",
                titleEn: "Full Library",
                descPt: "Milhares de títulos de todas as regiões, organizados por nome e tamanho.",
                descEn: "Thousands of titles from all regions, organized by name and size.",
              },
              {
                icon: <PackagePlus className="w-9 h-9 drop-shadow-[0_0_8px_rgba(229,0,122,0.7)]" />,
                titlePt: "Expansões & DLCs",
                titleEn: "DLCs & Expansions",
                descPt: "Conteúdo adicional oficial pronto para ser instalado no seu memory stick.",
                descEn: "Official additional content ready to install on your memory stick.",
              },
              {
                icon: <RefreshCcw className="w-9 h-9 drop-shadow-[0_0_8px_rgba(0,168,107,0.7)]" />,
                titlePt: "Updates Automáticos",
                titleEn: "Auto Updates",
                descPt: "O app verifica automaticamente se seus jogos instalados possuem patches disponíveis.",
                descEn: "The app automatically checks if your installed games have available patches.",
              },
              {
                icon: <Zap className="w-9 h-9 drop-shadow-[0_0_8px_rgba(0,112,209,0.7)]" />,
                titlePt: "Fluxo One-Click",
                titleEn: "One-Click Flow",
                descPt: "Download, extração (pkg2zip) e transferência para o drive USB automática.",
                descEn: "Automated download, extraction (pkg2zip), and USB drive transfer.",
              },
            ].map((feat, i) => (
              <SpotlightCard
                key={i}
                className="scroll-reveal p-10 text-center rounded-[20px]"
                style={{ transitionDelay: `${i * 80}ms` } as React.CSSProperties}
              >
                {/* PSP button badge */}
                <div
                  className={`absolute top-4 right-5 text-lg font-black opacity-20 ${BADGE_COLORS[i]}`}
                >
                  {FEATURE_BADGES[i]}
                </div>

                <div className="w-[68px] h-[68px] rounded-2xl flex items-center justify-center mx-auto mb-7 bg-gradient-to-br from-purple-500/15 to-cyan-400/8 border border-white/10 shadow-[inset_0_1px_0_rgba(255,255,255,0.15),0_8px_20px_rgba(0,0,0,0.3)] text-white">
                  {feat.icon}
                </div>

                <h3 className="font-outfit text-xl font-bold mb-3">
                  {lang === "pt" ? feat.titlePt : feat.titleEn}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {lang === "pt" ? feat.descPt : feat.descEn}
                </p>
              </SpotlightCard>
            ))}
          </div>
        </div>
      </section>

      {/* ── XMB Divider ── */}
      <div className="xmb-divider mx-8 my-2" />

      {/* ── How to Start ── */}
      <section className="py-[100px] relative z-10 px-8" id="guide">
        <div className="max-w-[860px] mx-auto">
          <SpotlightCard className="scroll-reveal p-10 md:p-16 rounded-[28px]">
            <h2 className="font-outfit text-4xl md:text-5xl font-bold text-center mb-16">
              {lang === "pt" ? "Como Começar?" : "How to Start?"}
            </h2>

            <div className="flex flex-col gap-0">
              {[
                {
                  sym: "○", symColor: "text-[#e80000]",
                  titlePt: "Baixe o executável", titleEn: "Download the EXE",
                  descPt: "Vá até as releases e baixe o PSPFreeshop.zip.",
                  descEn: "Go to releases and download PSPFreeshop.zip.",
                },
                {
                  sym: "□", symColor: "text-[#e5007a]",
                  titlePt: "Conecte seu PSP", titleEn: "Connect your PSP",
                  descPt: "Ative a conexão USB no console e selecione o drive no app.",
                  descEn: "Enable USB connection on the console and select the drive in the app.",
                },
                {
                  sym: "△", symColor: "text-[#00a86b]",
                  titlePt: "Escolha e Jogue", titleEn: "Pick and Play",
                  descPt: "Procure o jogo que você quer e clique em baixar. O app faz o resto.",
                  descEn: "Search for the game you want and click download. The app does the rest.",
                },
              ].map((step, i, arr) => (
                <div key={i} className="relative flex gap-8 items-start">
                  {/* Vertical connector */}
                  {i < arr.length - 1 && (
                    <div
                      className="absolute left-[1.65rem] top-12 bottom-0 w-px"
                      style={{
                        background:
                          "linear-gradient(180deg,rgba(255,255,255,0.1) 0%,transparent 100%)",
                      }}
                    />
                  )}

                  {/* PSP symbol badge */}
                  <div className="shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center bg-white/5 border border-white/10 shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]">
                    <span className={`text-2xl font-black ${step.symColor}`}>
                      {step.sym}
                    </span>
                  </div>

                  <div className={`pb-14 ${i === arr.length - 1 ? "pb-0" : ""}`}>
                    <strong className="block font-outfit text-xl mb-2 text-foreground">
                      {lang === "pt" ? step.titlePt : step.titleEn}
                    </strong>
                    <p className="text-muted-foreground leading-relaxed">
                      {lang === "pt" ? step.descPt : step.descEn}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-14 text-center">
              <a
                href="https://github.com/marcosferreirarj/pspFreeShop/releases"
                className="inline-flex items-center gap-2.5 px-10 py-4 btn-primary text-white rounded-[16px] font-semibold text-sm"
              >
                <Download className="w-4 h-4" />
                {lang === "pt" ? "Baixar Agora" : "Download Now"}
              </a>
            </div>
          </SpotlightCard>
        </div>
      </section>

      {/* ── Support & Social ── */}
      <section className="py-[80px] relative z-10 px-8">
        <div className="max-w-[1200px] mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <SpotlightCard className="scroll-reveal p-10 rounded-2xl text-center">
              <h4 className="font-outfit text-2xl font-bold mb-8">
                {lang === "pt" ? "Código Aberto" : "Open Source"}
              </h4>
              <p className="text-muted-foreground text-sm mb-8 leading-relaxed">
                {lang === "pt"
                  ? "Contribua, reporte bugs ou acompanhe o desenvolvimento no GitHub."
                  : "Contribute, report bugs, or follow the development on GitHub."}
              </p>
              <div className="flex justify-center gap-4">
                <a
                  href="https://github.com/marcosferreirarj/pspFreeShop"
                  className="glass-btn w-14 h-14 !p-0 justify-center rounded-full"
                >
                  <GithubIcon className="w-6 h-6" />
                </a>
                <a
                  href="https://github.com/marcosferreirarj/pspFreeShop"
                  className="glass-btn gap-2 px-5 rounded-full text-sm"
                >
                  <ExternalLink className="w-4 h-4" />
                  {lang === "pt" ? "Ver Repositório" : "View Repo"}
                </a>
              </div>
            </SpotlightCard>

            <SpotlightCard
              className="scroll-reveal p-10 rounded-2xl text-center"
              style={{ "--delay": "100ms" } as React.CSSProperties}
            >
              <h4 className="font-outfit text-2xl font-bold mb-8">
                {lang === "pt" ? "Apoie o Projeto" : "Support the Project"}
              </h4>
              <p className="text-muted-foreground text-sm mb-8 leading-relaxed">
                {lang === "pt"
                  ? "Feito com amor pela comunidade PSP. Toda ajuda é muito bem-vinda."
                  : "Made with love for the PSP community. Every bit of support matters."}
              </p>
              <div className="flex justify-center gap-4">
                <a
                  href="#"
                  className="glass-btn w-14 h-14 !p-0 justify-center rounded-full border-[rgba(255,85,102,0.3)] text-[#ff5566] hover:bg-[rgba(255,85,102,0.1)] hover:border-[#ff5566] hover:shadow-[0_0_20px_rgba(255,85,102,0.3)]"
                >
                  <Heart className="w-6 h-6" />
                </a>
                <a
                  href="#"
                  className="glass-btn w-14 h-14 !p-0 justify-center rounded-full border-[rgba(255,85,102,0.3)] text-[#ff5566] hover:bg-[rgba(255,85,102,0.1)] hover:border-[#ff5566] hover:shadow-[0_0_20px_rgba(255,85,102,0.3)]"
                >
                  <Coffee className="w-6 h-6" />
                </a>
              </div>
            </SpotlightCard>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="mt-8 py-12 border-t border-white/8 relative z-10 px-8"
        style={{ background: "rgba(5,2,15,0.7)", backdropFilter: "blur(20px)" }}
      >
        <div className="max-w-[1200px] mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            {/* Brand */}
            <div>
              <div className="font-orbitron text-lg font-black tracking-tighter uppercase drop-shadow-[0_0_16px_rgba(157,78,221,0.4)] mb-2">
                pspFreeShop <span className="accent-text">Enhanced</span>
              </div>
              <p className="text-muted-foreground text-xs">
                {lang === "pt"
                  ? "© 2026 · Todos os direitos reservados."
                  : "© 2026 · All rights reserved."}
              </p>
            </div>

            {/* PSP button symbols — footer decoration */}
            <div className="flex gap-5 text-xl font-black opacity-30 select-none">
              <span className="text-[#0070d1]">×</span>
              <span className="text-[#e80000]">○</span>
              <span className="text-[#e5007a]">□</span>
              <span className="text-[#00a86b]">△</span>
            </div>

            {/* Links */}
            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <a
                href="https://github.com/marcosferreirarj/pspFreeShop"
                className="hover:text-white transition-colors flex items-center gap-1.5"
              >
                <GithubIcon className="w-4 h-4" />
                GitHub
              </a>
              <a
                href="https://github.com/marcosferreirarj/pspFreeShop/releases"
                className="hover:text-white transition-colors flex items-center gap-1.5"
              >
                <Download className="w-4 h-4" />
                Releases
              </a>
              <a
                href="https://github.com/marcosferreirarj/pspFreeShop/issues"
                className="hover:text-white transition-colors"
              >
                Issues
              </a>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-white/5 text-center text-xs text-muted-foreground">
            {lang === "pt"
              ? "Desenvolvido com ❤️ para a comunidade · pspFreeShop não é afiliado à Sony Interactive Entertainment."
              : "Made with ❤️ for the community · pspFreeShop is not affiliated with Sony Interactive Entertainment."}
          </div>
        </div>
      </footer>
    </>
  );
}
