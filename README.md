# 🕰️ Звонилка для уроков (School Bell Timer)

Простое приложение на **Python 3** для Linux, которое:

- Отображает **текущий урок или перемену** в виде **круговой диаграммы** в реальном времени.
- Проигрывает **звуковой сигнал** при начале каждого нового периода.
- Имеет **тёмную тему оформления** и работает без интернета.
- Поддерживает **расписание по дням недели** через простой текстовый файл.

> 💡 Идеально для школьных компьютеров, учеников и учителей!  
> ✅ Работает **только на Linux** (требуется свободное ПО и графическая среда: X11 или Wayland).

---

## 📦 Содержимое репозитория

- `simple_timer.py` — основной скрипт (окно с диаграммой).
- `timer.py` — расширенная версия с иконкой в трее (требует GNOME AppIndicator).
- `schedule.txt` — пример расписания звонков.
- `bell.wav`, `bell2.wav` — звуковые файлы (урок / перемена).
- `bell.png` — иконка приложения.
- `run-bell.sh` — скрипт-обёртка для запуска из ярлыка.
- `LICENSE` — лицензия (GNU GPL v3 или ваша).

---

## ⚙️ Требования

- **ОС**: Linux (Debian/Ubuntu, Fedora, Arch и др.)
- **Python 3.8+**
- **Графическая среда**: GNOME, KDE, XFCE и др. (с поддержкой X11 или Wayland)
- **Зависимости системы**:
  ```bash
  sudo apt install python3-pip python3-venv  # Debian/Ubuntu
  ```

---

## 🛠️ Установка и настройка

### 1. Клонируйте репозиторий

```bash
git clone https://ваш-репозиторий/school-bell.git
cd school-bell
```

### 2. Создайте виртуальное окружение

> ⚠️ Современные дистрибутивы (Ubuntu 24.04+, Debian 12+) блокируют `pip` в системном Python. Используйте `venv`!

```bash
python3 -m venv bell-env
source bell-env/bin/activate
```

### 3. Установите зависимости

```bash
pip install PyQt5 matplotlib pygame
```

### 4. Настройте расписание

Отредактируйте файл `schedule.txt` под своё расписание:

```txt
# Понедельник
MON
08:00-08:45 Урок 1
08:45-08:55 Перемена
...
```

Правила:
- Дни: `MON`, `TUE`, ..., `FRI`.
- Время: `ЧЧ:ММ-ЧЧ:ММ`.
- Название обязательно (например, `Перемена`, `Математика`).

---

## ▶️ Запуск

### Вариант 1: Простое окно (рекомендуется для начала)

```bash
source bell-env/bin/activate
QT_QPA_PLATFORM=xcb python simple_timer.py
```

> 💡 `QT_QPA_PLATFORM=xcb` обходит проблемы с Wayland в GNOME.

### Вариант 2: С иконкой в трее (требует GNOME AppIndicator)

```bash
# Установите поддержку трея (GNOME)
sudo apt install gnome-shell-extension-appindicator

# Перезапустите оболочку: Alt+F2 → r
QT_QPA_PLATFORM=xcb python timer.py
```
---

## 🔊 Звуки

Приложение воспроизводит:
- `bell.wav` — при начале **любого нового периода** (можно заменить на свой).
- Чтобы использовать разные звуки для урока/перемены — измените код в `simple_timer.py`.

Формат: **WAV (16-bit PCM)**. MP3 не поддерживается без дополнительных библиотек.

---

## 🖥️ Ярлык в меню приложений

### 1. Сделайте скрипт исполняемым

```bash
chmod +x run-bell.sh
```

### 2. Установите `.desktop`-файл

🚀 Давай сделаем всё по порядку:

---

## 1️⃣ `.desktop`-файл — для запуска из меню приложений

Создайте файл **`school-bell.desktop`** в корне проекта:

```ini
[Desktop Entry]
Name=Звонилка для уроков
Comment=Круговая диаграмма уроков и перемен с звуковым оповещением
Exec=/home/user/Programs/Python_run/run-bell.sh
Icon=/home/user/Programs/Python_run/bell.png
Terminal=false
Type=Application
Categories=Education;Utility;
StartupNotify=true
Keywords=школа;звонок;урок;перемена;таймер;
```

> 🔁 Замените `/home/user/Programs/Python_run/` на ваш реальный путь (узнать: `pwd` в папке проекта).

### Установка:
```bash
# Сделать исполняемым
chmod +x school-bell.desktop

# Установить в меню приложений
cp school-bell.desktop ~/.local/share/applications/

# Обновить кэш
update-desktop-database ~/.local/share/applications
```

Теперь ищи «Звонилка для уроков» в меню!

---

## 2️⃣ Автозапуск при входе в систему

Просто скопируй тот же `.desktop`-файл в автозагрузку:

```bash
mkdir -p ~/.config/autostart
cp school-bell.desktop ~/.config/autostart/
```

✅ Готово! Приложение будет запускаться автоматически при входе.

> 💡 Совет: если не хотите, чтобы окно сразу открывалось, можно модифицировать `run-bell.sh`, чтобы он запускал `timer.py` (с треем), а не `simple_timer.py`.

---

## 3️⃣ Упаковка в AppImage (рекомендуется для Python-приложений)

AppImage — это **один исполняемый файл**, который работает на любом Linux без установки.

### Шаги:

#### a) Установите `python-appimage`
```bash
pip install python-appimage
```

#### b) Создайте `appimage-builder.yml`

В корне проекта создайте файл:

```yaml
version: 1
AppDir:
  path: ./AppDir
  app_info:
    id: ru.school.bell
    name: SchoolBell
    icon: bell
    version: 1.0
    exec: usr/bin/school-bell
    exec_args: $@
  runtime:
    env:
      PYTHONPATH: ${APPDIR}/usr/lib/python3.12/site-packages
  files:
    include:
      - simple_timer.py
      - schedule.txt
      - bell.wav
      - bell.png
      - run-bell.sh
  icons:
    - bell.png
  desktop:
    file: school-bell.desktop
  scripts:
    before_freeze:
      - pip install --target=${APPDIR}/usr/lib/python3.12/site-packages PyQt5 matplotlib pygame
```

> ⚠️ Уточните версию Python (`python3.12` → ваша, например, `python3.10`).

#### c) Собери AppImage

```bash
python -m python_appimage build appimage-builder.yml
```

Через 5–10 минут получишь файл:  
`SchoolBell-x86_64.AppiImage`

Сделай его исполняемым:
```bash
chmod +x SchoolBell-x86_64.AppImage
```

И запускай где угодно! 🎉

---

## 4️⃣ Альтернатива: Flatpak (если нужна интеграция в магазин)

Flatpak сложнее, но даёт лучшую системную интеграцию.

### Кратко:

1. Установи Flatpak:
   ```bash
   sudo apt install flatpak
   flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
   ```

2. Используй [flatpak-builder](https://docs.flatpak.org/en/latest/first-build.html) с манифестом.

Но для **одного пользователя** AppImage проще и быстрее.

---

## 💡 Итог: что выбрать?

| Цель | Решение |
|------|--------|
| Запуск из меню | `.desktop` + `~/.local/share/applications` |
| Автозапуск | Копия в `~/.config/autostart/` |
| Раздача другим | **AppImage** (один файл, без установки) |
| Публикация в магазине | Flatpak (через Flathub) |

---

## 📦 Бонус: обновлённый `run-bell.sh` для автозапуска (с треем!)

Если хочешь, чтобы при автозапуске **не открывалось окно**, а работала **иконка в трее**, измени `run-bell.sh`:

```bash
#!/bin/bash
cd "$(dirname "$0")"
export QT_QPA_PLATFORM=xcb
exec ./bell-env/bin/python timer.py  # ← не simple_timer.py!
```

И убедись, что в системе установлен `gnome-shell-extension-appindicator`.

---

## 🎨 Особенности интерфейса

- **Тёмная тема**: фон `#2e2e2e`, текст белый.
- **Цвета**:
  - 🍊 **Оранжевый** — уроки и занятия.
  - 🌿 **Изумрудный** — перемены.
- Диаграмма обновляется **каждую секунду**.
- При смене периода — **звуковой сигнал**.

---

## ❓ Возможные проблемы и решения

| Проблема | Решение |
|---------|--------|
| `ModuleNotFoundError: No module named 'PyQt5'` | Убедитесь, что вы в `venv`: `source bell-env/bin/activate` |
| Окно не появляется в GNOME/Wayland | Запускайте с `QT_QPA_PLATFORM=xcb` |
| Нет иконки в трее | Установите `gnome-shell-extension-appindicator` |
| Звука нет | Проверьте наличие `bell.wav`, громкость, формат WAV |
| `IndentationError` | Используйте только **пробелы** (4 на уровень), не табы |

---

## 📜 Лицензия

Этот проект распространяется под лицензией **GNU General Public License v3.0** — см. файл [`LICENSE`](LICENSE).

> ❤️ Свободное ПО для свободного образования!

---

## 🙌 Автор

Автор: **Vadimyar**  
GitHub: [@vadimyar](https://github.com/vadimyar)

---

> «Пусть каждый звонок напоминает: знания — это свобода!»

*Сделано с ❤️ на Linux с использованием свободного ПО*
