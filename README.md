# agentx

Modularny framework do budowy agentów AI (LLM) z pętlą **plan → execute → verify**, pamięcią (session + long-term), routingiem narzędzi, politykami bezpieczeństwa i telemetryką. Projekt jest podzielony na czytelne “klocki”, żeby łatwo było dodawać nowe strategie planowania, nowe narzędzia i kolejne integracje (API, bazy danych, wektory, APM).

---

## TL;DR

- **API / Gateway**: przyjmuje requesty i mapuje je na runtime agenta
- **Orchestrator**: prowadzi pętlę agentową (plan → execute → verify → repeat)
- **Planner**: rozbija zadania na kroki (LLM lub heurystyki)
- **Tools**: rejestr, router i executor do wywołań narzędzi
- **Critique/Verifier**: walidacja jakości i zgodności z politykami
- **Memory**: kontekst sesyjny + pamięć długoterminowa
- **Response Composer**: składa finalną odpowiedź (formatowanie, trace)
- **Policies**: access control + safety + schematy
- **Telemetry**: eventy, metryki, tracing / correlation id



---

## Struktura projektu

agentx/
├─ pyproject.toml # lub setup.cfg / requirements.txt – meta i zależności
├─ README.md
├─ .env.example # przykładowe zmienne środowiskowe (API keys itd.)
├─ .gitignore
├─ src/
│ └─ agentx/
│ ├─ init.py
│ ├─ config/
│ │ ├─ init.py
│ │ ├─ settings.py # globalne ustawienia, limity, ścieżki itd.
│ │ └─ logging_config.py # konfiguracja logowania
│ │
│ ├─ api/
│ │ ├─ init.py
│ │ ├─ gateway.py # 1) API / Gateway – wejściowy handler requestów
│ │ ├─ models.py # DTO: Request, Response, Metadata
│ │ └─ rate_limiting.py # rate limiting, ew. middleware
│ │
│ ├─ core/
│ │ ├─ init.py
│ │ ├─ orchestrator.py # 2) Orchestrator / Agent Runtime
│ │ ├─ loop.py # logika pętli: plan → execute → verify → repeat
│ │ ├─ types.py # Step, Plan, ToolCall, ToolResult itd.
│ │ ├─ errors.py # Timeout, PolicyError, ToolError…
│ │ └─ budget.py # token/cost/timeouts/retry policy
│ │
│ ├─ memory/
│ │ ├─ init.py
│ │ ├─ context_builder.py # 3) Memory & Context Builder
│ │ ├─ long_term_store.py # interfejs i implementacje pamięci LT
│ │ ├─ session_store.py # pamięć sesyjna/krótkoterminowa
│ │ └─ profiles.py # profil usera, preferencje, uprawnienia
│ │
│ ├─ planning/
│ │ ├─ init.py
│ │ ├─ base.py # 4) abstrakcyjny Planner
│ │ ├─ llm_planner.py # Planner na bazie LLM
│ │ └─ heuristics.py # reguły / heurystyki decomposition
│ │
│ ├─ tools/
│ │ ├─ init.py
│ │ ├─ base.py # Tool, ToolResult, ToolError
│ │ ├─ registry.py # rejestr narzędzi + policy gating
│ │ ├─ router.py # 5) Tool Router – wybór narzędzi
│ │ └─ executor.py # 5) Tool Executor – wywołania + normalizacja
│ │
│ ├─ critique/
│ │ ├─ init.py
│ │ ├─ base.py # 6) abstrakcyjny Critic / Verifier
│ │ ├─ llm_critic.py # weryfikacja przy pomocy LLM
│ │ ├─ policy_checks.py # zgodność z politykami
│ │ └─ validators.py # sanity checks / brak danych / walidacja
│ │
│ ├─ response/
│ │ ├─ init.py
│ │ ├─ composer.py # 7) Response Composer
│ │ ├─ formatting.py # styl, markdown, cytowania, załączniki
│ │ └─ trace.py # explain/trace dla debug/devtools
│ │
│ ├─ policies/
│ │ ├─ init.py
│ │ ├─ access_control.py # kto ma dostęp do jakich narzędzi/zasobów
│ │ ├─ safety.py # safety / content filters / guardrails
│ │ └─ schemas.py # definicje polityk / schematy (np. Pydantic)
│ │
│ ├─ telemetry/
│ │ ├─ init.py
│ │ ├─ events.py # definicje eventów telemetryjnych
│ │ ├─ metrics.py # metryki (czas, koszty, sukces/fail)
│ │ └─ tracing.py # correlation id, trace id, integracje APM
│ │
│ ├─ agents/
│ │ ├─ init.py
│ │ ├─ base.py # Agent = planner + tools + policies
│ │ └─ examples.py # przykładowe konfiguracje agentów
│ │
│ └─ utils/
│ ├─ init.py
│ ├─ llm_client.py # adaptery do różnych LLM (OpenAI, lokalne, itd.)
│ ├─ serialization.py # json, msgpack, Pydantic, itp.
│ └─ time.py # helpery timeoutów / zegarów
│
└─ tests/
├─ init.py
├─ test_orchestrator.py
├─ test_planner.py
├─ test_tools.py
├─ test_memory.py
└─ ...
---