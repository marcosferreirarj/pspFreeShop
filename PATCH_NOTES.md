# 🚀 PSP Freeshop - Patch Notes (Nova Versão Standalone)

Esta é a maior e mais completa atualização do **PSP Freeshop** até o momento! Abaixo estão todas as novidades, melhorias de estabilidade e novos recursos adicionados.

## ✨ Novas Funcionalidades e Abas

- **🎮 Suporte Completo a DLCs e Updates:**
  - Foi adicionado suporte definitivo para download de Updates e DLCs.
  - Implementação de feedback visual e progresso em tempo real durante o download e a extração dos pacotes, tudo integrado confortavelmente na interface do usuário.
  - Correção na detecção do ID dos títulos (Title ID), garantindo que os updates e conteúdos adicionais sejam sempre vinculados ao jogo correspondente.

- **🎨 Nova Aba de Temas Customizados (Themes):**
  - Adicionada aba exclusiva para instalação de *Temas Customizados (.ptf)* direto para o console.
  - Agora a aplicação acompanha dezenas de temas pré-carregados para personalização imediata do seu PSP, sem precisar de downloads extras!

- **🔍 Sistema de Detecção de Conteúdo Instalado:**
  - O aplicativo agora varre o Cartão SD / Memória local e **identifica automaticamente** tudo o que você já tem instalado. 
  - As abas mostram claramente não apenas os Jogos instalados, mas também **Updates, DLCs e Temas** já presentes no sistema.

## 🛠️ Correções de Bugs (Bug Fixes)

- **Correção Geral no Sistema de Rolagem e Buscas:**
  - Resolvido um problema irritante (Scroll Bug) em que a busca não retornava ao topo da lista, escondendo resultados.
  - Adicionado botão **"Limpar Filtros / Clear Filters"** em todas as abas, permitindo restaurar o estado padrão do aplicativo com facilidade.
  - O menu de opções de clique com botão direito ("Excluir Jogo") foi devidamente isolado — a opção agora aparece exclusivamente quando você está explorando os Itens Instalados.

## ⚡ Otimizações Técnicas (Performance)

- **Redução Massiva no Consumo de Memória (RAM):**
  - Refatoração na arquitetura de cache e renderização de listas para consumir significativamente menos memória.
  - Todas as Capas de Jogos (.jpg/.png) sofreram um processo de sanitização e **super compressão**, eliminando artes que não estavam na base de dados, reduzindo brutalmente o tamanho e o tempo de carregamento do app!

- **Novo Sistema Global de Filtros e Busca:**
  - O mecanismo de busca passou por uma forte otimização, trabalhando uniformemente na triagem das quatro divisões da plataforma (Jogos, DLCs, Updates e Temas).

## 📦 Agora é 100% Standalone (Portátil)

Nesta versão você não precisa de mais nada além do `.exe`!  
O processo de construção foi completamente redesenhado:
- **Tudo Incluído:** Arquivos como `PSP_DLCS.tsv`, `PSP_UPDATES.tsv`, `PSP_THEMES.tsv`, o extraidor `pkg2zip`, todas as Capas Comprimidas e os Temas locais foram **embutidos diretamente dentro do executável**.
- **Maior Praticidade:** Basta executar `PSPFreeshop.exe` de qualquer lugar, em qualquer computador, sem extrair pastas ou depender do repositório no Github.

## 🌐 Novidades Extras da Comunidade
- **Novo Site do Projeto:** Uma página com Web Design Moderno em Glassmorphism e adaptação para PT-BR/EN, trazendo links fáceis para versões e facilitando novos usuários conhecerem o aplicativo.
