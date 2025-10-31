# Product Brief: aido

**Date:** 2025-10-30
**Author:** Pedro
**Status:** Draft for PM Review

---

## Executive Summary

O Aido é uma **plataforma de automação inteligente de documentos**, interna e segura, que utiliza um sistema de agentes de IA (Google ADK) para resolver o problema crônico de ineficiência e perda de conhecimento na criação de manuais de processo. Ao transformar fontes não estruturadas (como vídeos e conversas) em documentação padronizada no formato `.docx`, o Aido visa reduzir custos operacionais, preservar o conhecimento estratégico da empresa e liberar colaboradores para tarefas de maior valor. O projeto é uma iniciativa de inovação interna com alta visibilidade e prazos de entrega agressivos, começando com um MVP focado em provar a viabilidade da arquitetura de agentes e entregar valor rapidamente.

---

## Problem Statement

O processo atual de documentação de processos na área de controladoria é inconsistente e, em grande parte, manual. Processos críticos frequentemente existem apenas em formatos voláteis como vídeos tutoriais ou no conhecimento tácito de colaboradores, e muitos processos simples nem chegam a ser documentados.

Esta abordagem resulta em:
*   **Falha na Criação de Documentação**: A ineficiência do processo manual é tão alta que, frequentemente, os vídeos não são convertidos em manuais, deixando o conhecimento sem registro formal.
*   **Ineficiência Operacional**: Horas de trabalho de colaboradores qualificados são gastas em tarefas repetitivas de transcrição e estruturação, quando a documentação é criada.
*   **Inconsistência e Risco**: Os poucos manuais criados carecem de padronização, gerando erros e retrabalho. Além disso, a confidencialidade dos dados impede o uso de ferramentas de IA externas que poderiam mitigar o problema.

---

## Proposed Solution

O Aido é uma **plataforma de automação inteligente de documentos** que resolve o problema da documentação ao **utilizar um sistema de agentes de IA (Google ADK) para transformar fontes não estruturadas, como vídeos e conversas, em manuais de processo padronizados e de alta qualidade.**

Diferente das soluções existentes, que são genéricas e baseadas em nuvem pública, o Aido irá operar como uma **ferramenta interna, segura e auditável, capaz de manusear dados confidenciais.** Seu principal diferencial é a **arquitetura de agentes especializados** que não apenas transcrevem, mas também compreendem, estruturam e mantêm o conhecimento ao longo do tempo.

Isso garante que a empresa possa **reduzir drasticamente o tempo e o custo da documentação, preservar seu conhecimento estratégico e liberar seus colaboradores para tarefas de maior valor agregado.**

---

## Target Users

### Primary User Segment

- **Perfil**: Analistas e estagiários da área de controladoria e finanças.
- **Problema Atual**: São responsáveis por documentar novos processos ou atualizar os existentes, mas o fazem manually a partir de vídeos ou reuniões, um processo lento e propenso a erros.
- **Objetivo**: Querem uma forma rápida e confiável de gerar manuais padronizados para garantir a consistência e liberar tempo para tarefas mais analíticas.

### Secondary User Segment

- **Perfil**: Colaboradores de qualquer departamento da empresa (Engenharia, Operações, RH, etc.) que precisam documentar ou consumir processos, incluindo equipes internacionais.
- **Problema Atual**: Enfrentam problemas semelhantes de documentação, com o desafio adicional da barreira do idioma e da falta de um padrão global.
- **Objetivo**: Acessar uma ferramenta centralizada para criar e encontrar documentação de processos confiável, independentemente do departamento ou localização.

---

## Goals and Success Metrics

### Business Objectives

- **Redução de Custo**: Diminuir em X% as horas gastas na criação e padronização de documentação.
- **Preservação de Conhecimento**: Garantir que 100% dos novos processos (originados de vídeo, áudio, ou texto) sejam documentados na plataforma.
- **Validação Estratégica**: Provar a viabilidade de soluções de IA internas para a diretoria.

### User Success Metrics

- **Redução do Tempo por Tarefa**: Reduzir o tempo médio para criar ou padronizar um manual em 75%.
- **Adoção da Ferramenta**: X% dos colaboradores da área de controladoria utilizando o 'aido' para todas as novas documentações.
- **Qualidade Percebida**: Obter um feedback positivo de 90% dos usuários sobre a qualidade e padronização dos manuais gerados.

### Key Performance Indicators (KPIs)

1.  **Redução do Tempo por Tarefa (%)**: Mede o ganho de eficiência.
2.  **Taxa de Adoção da Ferramenta (%)**: Mede a relevância da ferramenta para os usuários.
3.  **Índice de Satisfação do Usuário (%)**: Mede a qualidade da experiência e dos resultados.
4.  **Taxa de Cobertura de Documentação (%)**: Mede o impacto na preservação do conhecimento.

---

## Strategic Alignment and Financial Impact

### Financial Impact

O principal impacto financeiro será a **redução de custos operacionais** pela diminuição de horas de trabalho manual. Ao automatizar a criação de documentação, colaboradores qualificados são liberados para atividades de maior valor agregado. Uma estimativa inicial sugere uma **redução de até 75% no tempo** para produzir um manual.

### Company Objectives Alignment

O projeto está diretamente alinhado com o objetivo da empresa de **fomentar a inovação interna** e desenvolver soluções de IA seguras e proprietárias. Ele serve como um caso de uso estratégico para validar a abordagem de IA interna em paralelo às negociações com grandes plataformas externas.

### Strategic Initiatives

O Aido suporta a iniciativa de **transformação digital** da área de controladoria e finanças, além de ser um piloto para a aplicação de IA generativa em outros departamentos da empresa, reforçando a cultura de **melhoria contínua e excelência operacional**.

---

## MVP Scope

### Core Features (Must Have)

O MVP foca em replicar o fluxo do protótipo dentro da nova arquitetura, dividido pelas seguintes entregas de sprint:

1.  **Implementação do ADK (Sprint até 31/10)**: Implementar a estrutura base com 3 agentes (`whisper_agent`, `create_agent`, `update_agent`) gerenciados por um orquestrador.
2.  **Memória (Sprint até 21/11)**: Integrar o banco de dados Postgres para persistir o histórico das conversas e documentos.
3.  **UI Simples (Sprint até 08/12)**: Desenvolver uma interface de usuário funcional em inglês para interação básica.
4.  **Geração de .docx**: Como parte dos agentes `create` e `update`, implementar a geração do manual em formato `.docx` a partir de um template.

### Out of Scope for MVP

- **Suporte a Múltiplos Idiomas na UI**: A interface será exclusivamente em inglês no MVP.
- **Dashboards e Análises Avançadas**: Funcionalidades de análise preditiva ou dashboards de BI.
- **UI com Componentes Avançados**: O uso de bibliotecas como Shadcn é uma melhoria pós-MVP.
- **Geração de Outros Formatos**: O foco é exclusivamente na saída `.docx`.

### MVP Success Criteria

O MVP será um sucesso quando o fluxo completo (transcrição -> estruturação -> geração .docx -> revisão) for executado com sucesso dentro da arquitetura de agentes do Google ADK, em um ambiente pronto para deploy no Google Cloud.

---

## Post-MVP Vision

### Phase 2 Features

- **Melhoria da UI/UX**: Implementação de uma interface mais rica com componentes profissionais (ex: Shadcn).
- **Suporte a Múltiplos Idiomas**: Expandir a capacidade de processamento e a UI para outros idiomas, alavancando o potencial global da ferramenta.
- **Editor Interativo**: Permitir que o usuário edite o manual gerado diretamente na interface antes de exportar.

### Long-term Vision

A visão de longo prazo para o Aido é se tornar a **plataforma central de gestão de conhecimento de processos da empresa**. Ele evoluiria de uma ferramenta de documentação para um **ecossistema de agentes autônomos** que não apenas documentam, mas também analisam, otimizam e potencialmente executam processos digitais.

### Expansion Opportunities

- **Expansão Departamental**: Levar a solução para outros departamentos como Engenharia, Operações e RH.
- **Análise Preditiva**: Integrar módulos de IA para analisar os processos documentados e sugerir melhorias ou prever falhas.
- **Integração com Outros Sistemas**: Conectar o Aido a outros sistemas da empresa (ERP, CRM) para enriquecer a documentação com dados em tempo real.

---

## Technical Considerations

### Platform Requirements

A aplicação será desenvolvida como uma **aplicação web** e implantada no **Google Cloud**.

### Technology Preferences

- **Backend**: Python, Google Agent Development Kit (ADK)
- **Transcrição**: OpenAI Whisper
- **IA Generativa**: Modelos do Google (via AIService)
- **Banco de Dados**: PostgreSQL (para a memória do agente)
- **Geração de Documentos**: Biblioteca `python-docx-template`

### Architecture Considerations

A arquitetura será baseada em um **orquestrador central** que gerencia 3 agentes especializados como ferramentas:
1.  `whisper_agent`: Responsável pela transcrição.
2.  `create_agent`: Gera novos manuais a partir de fontes não estruturadas.
3.  `update_agent`: Atualiza e refina manuais existentes.

---

## Constraints and Assumptions

### Constraints

- **Prazos Agressivos**: O projeto é dividido em sprints curtos com entregas rápidas.
- **UI em Inglês**: A interface do MVP deve ser desenvolvida exclusivamente em inglês.
- **Formato de Saída**: A saída final deve ser obrigatoriamente um arquivo `.docx`.
- **Melhores Práticas**: A implementação deve seguir as 25 melhores práticas para o ADK, conforme documento de referência.

### Key Assumptions

- O Google ADK é flexível o suficiente para implementar o padrão de orquestrador e agentes especializados conforme desejado.
- O template `.docx` para a geração dos manuais é um arquivo fixo e será fornecido.
- A performance do Whisper e dos modelos de IA do Google é suficiente para atender às necessidades de velocidade do fluxo.

---

## Risks and Open Questions

### Key Risks

- **Prazo do Sprint 1 (Risco Alto)**: A implementação da arquitetura ADK completa até 31/10 é extremamente ambiciosa e pode exigir simplificações.
- **Desenvolvedor Único (Risco Médio)**: O projeto depende de um único desenvolvedor, criando um ponto de falha.
- **Complexidade da Integração**: A integração entre os diferentes componentes (Whisper, ADK, Postgres, Docx) pode ser mais complexa do que o esperado.

### Open Questions

- Como o template `.docx` será gerenciado e fornecido aos agentes `create` e `update` de forma dinâmica?
- Qual será o formato exato do JSON que a IA deve gerar para ser compatível com o template `.docx`?
- Como será o fluxo de feedback do usuário para o agente `update` dentro da UI?

### Areas Needing Further Research

{{research_areas}}

---

## Appendices

### A. Research Summary

{{research_summary}}

### B. Stakeholder Input

{{stakeholder_input}}

### C. References

{{references}}

---

_This Product Brief serves as the foundational input for Product Requirements Document (PRD) creation._

_Next Steps: Handoff to Product Manager for PRD development using the `workflow prd` command._
