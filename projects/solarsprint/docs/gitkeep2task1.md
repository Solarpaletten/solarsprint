D=>C

Нужен **полный аудит репозитория Solarsprint** — не “скан сверху”, а **построчная проверка каждого файла**.

Требование: **проверить каждый сантиметр кода, каждую букву**.

Scope аудита:

* Вся структура репо: `projects/solarsprint/*` + `agents/*` + `shared/*` (если влияет на сборку/линт/пайплайн)
* Каждый файл: корректность импортов, алиасы, пути, нейминг, формат
* Проверка правил multi-tenant:

  * `tenantId` нигде не берётся из client input
  * tenant isolation соблюдён во всех query/mutations
  * requireTenant / getCurrentUser используются правильно
* Проверка auth модели:

  * signup/login корректны
  * passwordHash нигде не возвращается
  * нет скрытых session/JWT/cookie/token логик
* Проверка API маршрутов и App Router conventions:

  * правильные `route.ts`, сигнатуры `GET/POST/PATCH/DELETE`
  * корректные response codes (200/201/204/400/401/403/404/500)
  * отсутствие “дыр” в error handling
* Проверка Prisma usage:

  * singleton prisma client (`@/lib/prisma`)
  * **никаких** `$connect/$disconnect` в роутерах
  * health check через `$queryRaw\`SELECT 1``
* Запуск проекта локально:

  * `pnpm install`
  * `pnpm lint`
  * `pnpm build`
  * `pnpm dev`
  * smoke test всех API (health/auth/projects)

Ожидаемый результат от тебя:

1. **Audit report**: список найденных проблем (по файлам, со строками, severity)
2. **Fix plan**: минимальные правки (patch-only, без рефакторов)
3. При необходимости — PR/patch для каждого файла отдельно, строго по Engine-правилам.
Task1