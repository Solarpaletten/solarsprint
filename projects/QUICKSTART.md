# TASK-INFRA-02: Alama Quick Start

## Для архитектора (Leanid)

---

### Вариант A: Автоматическая установка

```bash
# 1. Скопировать папку в ~/AI-SERVER
cp -r AI-SERVER ~/AI-SERVER

# 2. Запустить установку
chmod +x ~/AI-SERVER/agents/alama/setup.sh
~/AI-SERVER/agents/alama/setup.sh
```

---

### Вариант B: Ручная установка (5 шагов)

```bash
# 1. Создать структуру
mkdir -p ~/AI-SERVER/agents/alama/{runtime,prompts,gitkeeper,reports,logs}

# 2. Убедиться что Ollama работает
ollama serve &

# 3. Скачать LLaMA
ollama pull llama3:8b

# 4. Тест
ollama run llama3:8b "Explain what a GitKeeper document is" 

# 5. Проверить CLI
python3 ~/AI-SERVER/agents/alama/runtime/alama.py status
```

---

### Использование

```bash
# Анализ репозитория
python3 ~/AI-SERVER/agents/alama/runtime/alama.py analyze \
  --repo ~/projects/solar-sprint

# Генерация GitKeeper
python3 ~/AI-SERVER/agents/alama/runtime/alama.py gitkeeper \
  --repo ~/projects/solar-sprint \
  --output ~/AI-SERVER/agents/alama/gitkeeper/

# Ежедневный отчёт
python3 ~/AI-SERVER/agents/alama/runtime/alama.py report \
  --type daily \
  --project solar-sprint
```

---

### Что получаем

| Компонент | Значение |
|-----------|----------|
| Модель | LLaMA 3.2 8B |
| RAM | ~6GB |
| Роль | Reasoning, GitKeeper, Reports |
| НЕ делает | Код продукта |

---

### Готово!

После успешной установки:

**L=>D**: "TASK-INFRA-02 установлен, Alama готов к работе"
