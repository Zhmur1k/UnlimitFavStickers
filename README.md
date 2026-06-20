# UnlimitFavStickers

> **Плагин для AyuGram / ExteraGram**  
> *Plugin for AyuGram / ExteraGram*

[![Version](https://img.shields.io/badge/version-1.4.2-blue)](https://github.com/)
[![Min Telegram](https://img.shields.io/badge/min%20Telegram-11.12.0-blue)](https://github.com/)
[![Author](https://img.shields.io/badge/author-@Mr__Zhmurik-9cf)](https://t.me/Mr_Zhmurik)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🇷🇺 Описание

**UnlimitFavStickers** снимает встроенное ограничение Telegram на количество избранных стикеров (по умолчанию — 5) и сохраняет их локально, независимо от синхронизации с сервером.

### ✨ Возможности

| Функция | Описание |
|---|---|
| 🔓 **Без лимита** | Добавляйте неограниченное количество избранных стикеров |
| 💾 **Локальное хранение** | Стикеры сохраняются в JSON-файл на устройстве |
| 🔄 **Авто-восстановление** | После сброса данных приложения стикеры восстанавливаются из резервной копии в папке `Загрузки` |
| 🔔 **Уведомления** | Опциональные всплывающие уведомления при добавлении/удалении стикера |
| ⚙️ **Настройки в интерфейсе** | Пункт настроек интегрирован прямо в экран «Стикеры и эмодзи» Telegram |
| 🛡️ **Надёжность** | Атомарная запись (`.tmp` → `.bak` → основной файл), потокобезопасный доступ |
| 🧹 **Авто-очистка** | При запуске удаляет «осиротевшие» записи из базы данных |

---

## 🇬🇧 Description

**UnlimitFavStickers** removes Telegram's built-in limit on the number of favorite stickers (default: 5) and stores them locally, independent of server synchronization.

### ✨ Features

| Feature | Description |
|---|---|
| 🔓 **No limit** | Add an unlimited number of favorite stickers |
| 💾 **Local storage** | Stickers are saved to a JSON file on-device |
| 🔄 **Auto-restore** | After app data wipe, stickers are restored from a backup in the `Downloads` folder |
| 🔔 **Notifications** | Optional toast notifications when adding/removing stickers |
| ⚙️ **Native settings UI** | Plugin settings are integrated directly into Telegram's "Stickers & Emoji" screen |
| 🛡️ **Reliability** | Atomic writes (`.tmp` → `.bak` → main file), thread-safe access |
| 🧹 **Auto-cleanup** | Removes orphaned sticker records from the database on startup |

---

## 📦 Установка / Installation

### RU
1. Откройте **AyuGram** или **ExteraGram**
2. Перейдите в **Настройки → Плагины**
3. Нажмите «+» и выберите файл `unlifavstick.plugin`
4. Включите плагин — готово!

### EN
1. Open **AyuGram** or **ExteraGram**
2. Go to **Settings → Plugins**
3. Tap "+" and select `unlifavstick.plugin`
4. Enable the plugin — done!

---

## ⚙️ Настройки / Settings

После установки зайдите в **Настройки → Стикеры и эмодзи**.  
After installation, go to **Settings → Stickers & Emoji**.

В разделе **UnlimitFavStickers** вы найдёте:  
In the **UnlimitFavStickers** section you will find:

- ✅ **Показывать уведомления / Show notifications** — включает/выключает всплывающие уведомления при добавлении и удалении стикеров из избранных

---

## 🔧 Как это работает / How it works

### Хуки / Hooks

Плагин перехватывает методы `MediaDataController` через рефлексию:

| Метод | Действие |
|---|---|
| `addRecentSticker` | Перехватывает добавление/удаление в избранное, сохраняет в локальную БД |
| `getRecentStickers` | Возвращает стикеры из локальной БД вместо серверных |
| `processLoadedRecentDocuments` | Подменяет список при обновлении UI |
| `isStickerInFavorites` | Проверяет статус стикера по локальной БД |
| `StickersActivity.fillItems` | Добавляет секцию настроек плагина в список «Стикеры и эмодзи» |
| `StickersActivity.onClick` | Обрабатывает нажатие на переключатель уведомлений |
| `StickersActivity.createView` | Fallback-bootstrap для установки UI-хуков при открытии экрана |

### Хранение данных / Data storage

```
/data/data/<telegram_package>/files/stickers.json      ← основной файл
/data/data/<telegram_package>/files/stickers.json.bak  ← резервная копия
/sdcard/Download/unlifavstick_backup.json              ← внешний бэкап
```

Структура базы данных:

```json
{
  "accounts": {
    "123456789": ["id1", "id2", "id3"]
  },
  "stickers": {
    "id1": {
      "id": 123,
      "access_hash": 456,
      "dc_id": 1,
      "mime_type": "image/webp",
      "attrs": [...]
    }
  }
}
```

---

## 🛡️ Надёжность / Reliability

- **Атомарная запись**: данные пишутся во временный `.tmp`-файл, затем атомарно заменяют основной — исключает потерю данных при сбое
- **Тройной уровень резервирования**: основной файл → `.bak` → `/sdcard/Download/`
- **Авто-восстановление**: если основной файл отсутствует (сброс данных приложения), плагин автоматически восстанавливает данные из папки `Загрузки`
- **Потокобезопасность**: все операции с БД защищены `threading.RLock()`
- **Отложенная запись**: сохранение откладывается на 1 секунду — снижает нагрузку на I/O при частых операциях

---

## 📋 Требования / Requirements

| Параметр | Значение |
|---|---|
| Минимальная версия Telegram | 11.12.0 |
| Поддерживаемые клиенты | AyuGram, ExteraGram |
| Android | 6.0+ (API 23+) |
| Разрешения | `WRITE_EXTERNAL_STORAGE` (для резервного копирования в `Загрузки`) |

---

## 📝 Changelog

### v1.4.2 (текущая / current)
- Полный рефакторинг: `StickersDB`, хуки, UI-интеграция разделены на чёткие классы
- Настройки плагина вынесены в нативный экран «Стикеры и эмодзи»
- `StickersActivityBootstrapHook` как fallback для установки UI-хуков
- `weakref` для предотвращения утечек памяти
- Полная типизация (type hints)
- Надёжный поиск методов через несколько вариантов сигнатур

### v2.0.7
- Удалены: умная сортировка, мультиаккаунтный режим (вызывали баги интерфейса)
- Добавлена кнопка настроек в ActionBar
- Безопасные уведомления через `show_success`/`show_error`
- Авто-очистка orphaned-записей при загрузке

---

## 🤝 Вклад / Contributing

Баги и предложения — в [Issues](../../issues).  
Bug reports and suggestions — open an [Issue](../../issues).

Pull Request'ы приветствуются!  
Pull Requests are welcome!

---

## 📄 Лицензия / License

[MIT License](LICENSE) — свободное использование и модификация.

---

## 👤 Автор / Author

**@Mr_Zhmurik** — [Telegram](https://t.me/Mr_Zhmurik)
