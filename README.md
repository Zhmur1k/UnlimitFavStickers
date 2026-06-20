<div align="center">
  <h1>
    <img src="sticker.webp" width="60" valign="middle" alt="Icon"> 
    UnlimitFavStickers
  </h1>
  <p>
    <a href="#-описание-ru">🇷🇺 Русский</a> •
    <a href="#-description-en">🇬🇧 English</a>
  </p>

  [![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)](https://github.com/Zhmur1k/UnlimitFavStickers)
  [![Min Telegram](https://img.shields.io/badge/Telegram-12.5.1+-blue?style=flat-square&logo=telegram)](https://github.com/Zhmur1k/UnlimitFavStickers)
  [![Author](https://img.shields.io/badge/author-@Mr__Zhmurik-9cf?style=flat-square&logo=telegram)](https://t.me/Mr_Zhmurik)
  [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
</div>

---

## 🇷🇺 Описание (RU)

Плагин для **AyuGram** и **ExteraGram**, который снимает встроенное ограничение Telegram на количество избранных стикеров (по умолчанию — 5). Стикеры больше не зависят от серверной синхронизации и хранятся локально в JSON-файле на устройстве.

### ✨ Возможности

| | Функция | Описание |
|:---:|---|---|
| 🔓 | **Без лимита** | Добавляйте любое количество избранных стикеров |
| 💾 | **Локальное хранение** | Данные сохраняются в JSON на устройстве, независимо от сервера |
| 🔄 | **Авто-восстановление** | После сброса данных приложения стикеры восстанавливаются из бэкапа в «Загрузках» |
| 📦 | **Импорт при установке** | Существующие избранные стикеры автоматически переносятся в локальную базу |
| 🔔 | **Уведомления** | Всплывающие уведомления при добавлении и удалении (можно отключить) |
| ⚙️ | **Настройки в UI** | Раздел настроек прямо в экране «Стикеры и эмодзи» Telegram |
| 🛡️ | **Надёжность** | Атомарная запись (`.tmp` → `.bak` → основной), потокобезопасный доступ |
| 🧹 | **Авто-очистка** | При запуске удаляет осиротевшие записи из базы данных |

### 🚀 Установка

1. Откройте **AyuGram** или **ExteraGram**.
2. Перейдите в **Настройки → Плагины**.
3. Нажмите `+` и выберите файл `unlifavstick.plugin`.
4. Включите плагин.

### ⚙️ Настройки

После установки зайдите в **Настройки → Стикеры и эмодзи** → раздел **UnlimitFavStickers**.
- **Показывать уведомления** — включает или выключает всплывающее уведомление при добавлении/удалении стикера из избранного.
- Там же отображается текущее количество сохранённых избранных стикеров.

### 🛠 Как это работает

Плагин перехватывает методы `MediaDataController` через рефлексию и подменяет стандартную логику:

| Метод | Что делает хук |
|---|---|
| `addRecentSticker` | Перехватывает добавление/удаление в избранное, пишет в локальную БД |
| `getRecentStickers` | Возвращает стикеры из локальной БД вместо серверного списка |
| `processLoadedRecentDocuments` | Подменяет список стикеров при обновлении UI |
| `isStickerInFavorites` | Проверяет статус стикера по локальной БД |
| `StickersActivity.fillItems` | Добавляет раздел настроек плагина в экран «Стикеры и эмодзи» |
| `StickersActivity.onClick` | Обрабатывает переключатель уведомлений |
| `StickersActivity.createView` | Fallback-bootstrap для установки UI-хуков при открытии экрана |

*При первом запуске плагин автоматически импортирует уже существующие избранные стикеры в локальную базу.*

### 📁 Хранение данных

```text
/data/data/<telegram_package>/files/stickers.json      ← Основной файл
/data/data/<telegram_package>/files/stickers.json.bak  ← Резервная копия
/sdcard/Download/unlifavstick_backup.json              ← Внешний бэкап
```

<details>
<summary><b>Структура JSON-базы (нажмите, чтобы развернуть)</b></summary>

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
      "size": 0,
      "attrs": [
        { "type": "TL_documentAttributeSticker", "alt": "😀", "set_id": 789, "set_hash": 0 },
        { "type": "TL_documentAttributeImageSize", "w": 512, "h": 512 }
      ]
    }
  }
}
```
</details>

База поддерживает несколько аккаунтов: у каждого свой список ID стикеров. Стикеры хранятся в общем словаре и автоматически очищаются, если больше ни один аккаунт их не использует.

### 🛡 Надёжность

- **Атомарная запись:** Данные пишутся во временный `.tmp`-файл, затем атомарно заменяют основной — исключает повреждение при сбоях.
- **Тройное резервирование:** При каждом сохранении данные дублируются в `.bak`-файл и в папку «Загрузки».
- **Авто-восстановление:** Если основной файл отсутствует, плагин автоматически восстанавливает базу из внешнего бэкапа.
- **Потокобезопасность:** Все операции с базой данных защищены `threading.RLock()`.
- **Отложенная запись:** Сохранение на диск откладывается на 1 секунду после последней операции для снижения нагрузки.

### 📌 Требования

| Параметр | Значение |
|---|---|
| **Минимальная версия Telegram** | `12.5.1` |
| **Поддерживаемые клиенты** | AyuGram, ExteraGram |
| **Android** | `6.0+` (API 23+) |
| **Разрешения** | `WRITE_EXTERNAL_STORAGE` (для резервного копирования в «Загрузки») |

---

## 🇬🇧 Description (EN)

A plugin for **AyuGram** and **ExteraGram** that removes Telegram's built-in limit on favorite stickers (default: 5). Stickers are no longer tied to server synchronization — they are stored locally in a JSON file on the device.

### ✨ Features

| | Feature | Description |
|:---:|---|---|
| 🔓 | **No limit** | Add an unlimited number of favorite stickers |
| 💾 | **Local storage** | Data is saved to an on-device JSON file, independent of the server |
| 🔄 | **Auto-restore** | After an app data wipe, stickers are restored from a Downloads folder backup |
| 📦 | **Import on install** | Existing favorite stickers are automatically migrated to the local DB |
| 🔔 | **Notifications** | Optional toast notifications when adding or removing a sticker |
| ⚙️ | **Native settings UI** | Plugin settings are integrated into Telegram's "Stickers & Emoji" screen |
| 🛡️ | **Reliability** | Atomic writes (`.tmp` → `.bak` → main), thread-safe access |
| 🧹 | **Auto-cleanup** | Removes orphaned sticker records from the database on startup |

### 🚀 Installation

1. Open **AyuGram** or **ExteraGram**.
2. Go to **Settings → Plugins**.
3. Tap `+` and select the `unlifavstick.plugin` file.
4. Enable the plugin.

### ⚙️ Settings

After installation, go to **Settings → Stickers & Emoji** → the **UnlimitFavStickers** section.
- **Show notifications** — toggles toast notifications when adding/removing a sticker from favorites.
- The section also displays the current number of saved favorite stickers.

### 🛠 How it works

The plugin intercepts `MediaDataController` methods via reflection and replaces the default logic:

| Method | Hook behavior |
|---|---|
| `addRecentSticker` | Intercepts add/remove from favorites, writes to local DB |
| `getRecentStickers` | Returns stickers from local DB instead of the server list |
| `processLoadedRecentDocuments` | Replaces the sticker list on UI updates |
| `isStickerInFavorites` | Checks sticker status against local DB |
| `StickersActivity.fillItems` | Injects the plugin settings section into "Stickers & Emoji" |
| `StickersActivity.onClick` | Handles the notifications toggle |
| `StickersActivity.createView` | Fallback bootstrap to install UI hooks when the screen opens |

*On first run, the plugin automatically imports any existing favorite stickers into the local database.*

### 📁 Data storage

```text
/data/data/<telegram_package>/files/stickers.json      ← Main file
/data/data/<telegram_package>/files/stickers.json.bak  ← Backup file
/sdcard/Download/unlifavstick_backup.json              ← External backup
```

<details>
<summary><b>JSON Database Structure (Click to expand)</b></summary>

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
      "size": 0,
      "attrs": [
        { "type": "TL_documentAttributeSticker", "alt": "😀", "set_id": 789, "set_hash": 0 },
        { "type": "TL_documentAttributeImageSize", "w": 512, "h": 512 }
      ]
    }
  }
}
```
</details>

The database supports multiple accounts, each with its own sticker ID list. Stickers are stored in a shared dictionary and automatically cleaned up when no account references them.

### 🛡 Reliability

- **Atomic writes:** Data is written to a temporary `.tmp` file, then atomically replaces the main file — preventing corruption during app crashes.
- **Triple backup:** On every save, data is copied to a `.bak` file and to the Downloads folder.
- **Auto-restore:** If the main file is missing, the plugin automatically restores the DB from the external backup.
- **Thread safety:** All operations are protected by `threading.RLock()`.
- **Deferred writes:** Disk saves are delayed by 1 second after the last operation to reduce I/O load.

### 📌 Requirements

| Parameter | Value |
|---|---|
| **Minimum Telegram version** | `12.5.1` |
| **Supported clients** | AyuGram, ExteraGram |
| **Android** | `6.0+` (API 23+) |
| **Permissions** | `WRITE_EXTERNAL_STORAGE` (for Downloads backup) |

---

## 📜 Changelog

### v1.0.0
- Initial release
- Local sticker database with triple backup redundancy
- Auto-import of existing favorites on first install
- Native settings section in the "Stickers & Emoji" screen

---

## 🤝 Contributing

Bug reports and suggestions — open an [Issue](https://github.com/Zhmur1k/UnlimitFavStickers/issues). Pull Requests are welcome!

---

## 📄 License

[MIT License](LICENSE)

---

<div align="center">
  <b>Made with ❤️ by <a href="https://t.me/Mr_Zhmurik">@Mr_Zhmurik</a></b>
</div>
