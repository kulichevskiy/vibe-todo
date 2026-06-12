# Упражнения

Эти упражнения мы делаем на лекции. Каждое привязано к одному блоку. Все упражнения — на твоём личном форке репо.

---

## E1 — Чтение diff: шум прячет баги

**Блок:** Дисциплина + чтение diff

Коммит `290093f` (`refactor: rename internal variables for consistency`) выглядит как безобидная косметика — агент «причесал» весь файл, переименовав переменные «для красоты». 31 строка вставок, 31 удалений.

Но это ловушка. Среди десятков невинных переименований спряталось одно, которое **молча ломает все сохранённые задачи**. Подпись коммита врёт: это переименование не «internal variable».

```bash
git log --oneline
git show 290093f        # или найди коммит #9 в логе и подставь его хэш
```

Вопросы для тебя:
1. Сколько строк изменено — и сколько из них реально меняют поведение, а не просто причёсывают?
2. Найди переименование, которое трогает **не внутреннюю переменную, а формат данных** — ключ в сохранённом JSON. Почему оно ломает старые задачи?
3. Почему такой баг почти невозможно поймать на глаз именно в этом коммите?
4. Как сформулировать запрос к AI, чтобы он так больше не делал?

<details>
<summary>Хочешь увидеть баг живьём</summary>

```bash
git checkout 142e3f9                                  # версия до рефакторинга
python3 todo.py add "купить молоко" --priority high --due 2026-06-01
git checkout 290093f                                  # коммит #9
python3 todo.py list                                  # → KeyError: 'title'
git checkout -                                         # вернуться обратно
```

Задача, сохранённая со старым ключом `text`, падает после «безобидного» переименования в `title`.
</details>

---

## E2 — Откат незакоммиченного: `git restore`

**Блок:** Откат

Симулируй AI-факап: открой `todo.py` и испорти что-нибудь (удали пару строк, переименуй функцию — всё что угодно). **Не коммить.**

```bash
git status     # видишь "modified: todo.py"
git diff       # видишь, что ты наменял
git restore todo.py
git status     # чисто
python3 todo.py list   # снова работает
```

Главное правило: пока ты не закоммитил — `git restore` спасает всё одной командой.

---

## E3 — Откат уже закоммиченного: `git reset --hard`

**Блок:** Откат

Теперь сделай факап и **закоммить его**:

```bash
echo "broken stuff" >> todo.py
git add todo.py
git commit -m "AI: experimental change"
python3 todo.py list   # сломано
```

Теперь надо откатить уже из истории:

```bash
git log --oneline
git reset --hard HEAD~1   # откатываемся на 1 коммит назад
git log --oneline         # плохой коммит исчез
python3 todo.py list      # снова работает
```

⚠️ `reset --hard` теряет незакоммиченную работу. Используй только когда уверен.

---

## E4 — Полный feature-флоу: ветка → push → PR → merge

**Блок:** Ветки + PR + Code Review

Сделай свою маленькую фичу через всю цепочку — так, как это происходит в реальной работе.

```bash
git switch -c feature/my-name
```

Теперь добавь себя в `README.md` — одну строчку в новую секцию `## Студенты`:

```bash
# отредактируй README.md
git add README.md
git commit -m "add: моё имя в студентов"
git push -u origin feature/my-name
```

После push: GitHub в твоём форке покажет жёлтую плашку **"Compare & pull request"**. Жми её.

В PR:
1. Заполни **title** ясно: «Добавил себя в список студентов»
2. **Description** в одну строчку: «Это моё первое PR-упражнение»
3. Жми **Create pull request**
4. Открой вкладку **Files changed** — это и есть code review
5. Оставь сам себе один inline-комментарий (нажми на `+` напротив строки)
6. Замержи кнопкой **Squash and merge**
7. Удали ветку кнопкой **Delete branch**

Локально:
```bash
git switch main
git pull
git branch -d feature/my-name   # локальная ветка тоже удалилась
```

---

## E5 — Конфликт (опционально, если осталось время)

**Блок:** Конфликты

Симулируем конфликт: две ветки трогают одну и ту же строку в `README.md`.

```bash
git switch main
git switch -c feature/title-a
# в README.md замени первую строку на "# vibe-todo (улучшенная версия)"
git add README.md && git commit -m "title: improved"

git switch main
git switch -c feature/title-b
# в README.md замени первую строку на "# vibe-todo — лучший todo в мире"
git add README.md && git commit -m "title: best"

# теперь пытаемся смержить обе в main:
git switch main
git merge feature/title-a       # ок
git merge feature/title-b       # КОНФЛИКТ
```

В VS Code откроется файл с маркерами `<<<<<<<` `=======` `>>>>>>>`.

Опции:
- Жми **Accept Current Change / Incoming / Both** в VS Code merge editor
- Или `git merge --abort` — кнопка эвакуации, всё откатывается

После разрешения:
```bash
git add README.md
git commit       # сообщение «merge ...» уже подготовлено
```
