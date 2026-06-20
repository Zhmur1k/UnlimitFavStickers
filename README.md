<div align="center">
  <h1>
    <img src="sticker.webp" width="60" valign="middle" alt="Icon">
    UnlimitFavStickers
  </h1>

  <p>
    <a href="#-description-en">English</a> •
    <a href="#-опис-uk">Українська</a> •
    <a href="#-описание-ru">Русский</a>
  </p>

  <p>
    <a href="https://github.com/Zhmur1k/UnlimitFavStickers">
      <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version">
    </a>
    <a href="https://github.com/Zhmur1k/UnlimitFavStickers">
      <img src="https://img.shields.io/badge/Telegram-12.5.1+-blue?style=flat-square&logo=telegram" alt="Minimum Telegram version">
    </a>
    <a href="https://t.me/Mr_Zhmurik">
      <img src="https://img.shields.io/badge/author-@Mr__Zhmurik-9cf?style=flat-square&logo=telegram" alt="Author">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
    </a>
  </p>
</div>

---

## 🇬🇧 Description (EN)

**UnlimitFavStickers** is a plugin for **AyuGram** and **ExteraGram** that removes Telegram's built-in favorite stickers limit. Instead of relying only on Telegram's server-side favorite stickers list, the plugin keeps your favorites in a local JSON database on the device.

It integrates into the regular Telegram sticker flow: adding, removing, checking, and displaying favorite stickers continues to work from the normal interface, but without the default limit.

### ✨ Features

| | Feature | Description |
|:---:|---|---|
| 🔓 | **No favorite limit** | Add as many favorite stickers as you want |
| 💾 | **Local storage** | Favorite stickers are saved in a local JSON database |
| 🔄 | **Auto-restore** | If the main database is missing, the plugin can restore it from the Downloads backup |
| 📦 | **Import on first launch** | Existing Telegram favorite stickers are imported into the local database |
| 🔔 | **Optional notifications** | Shows add/remove notifications, with a switch to disable them |
| ⚙️ | **Settings integration** | Adds a plugin section to Telegram's Stickers settings screen |
| 👥 | **Multi-account support** | Keeps a separate favorite sticker list for each Telegram account |
| 🛡️ | **Safer saving** | Uses delayed, thread-safe saving with `.tmp` and `.bak` files |
| 🧹 | **Database cleanup** | Removes sticker records that are no longer used by any account |
| 🌐 | **Localization** | Built-in English, Ukrainian, and Russian interface strings |

### 🚀 Installation

1. Open **AyuGram** or **ExteraGram**.
2. Go to **Settings → Plugins**.
3. Tap `+` and select `unlifavstick.plugin`.
4. Enable the plugin.
5. Restart the app if your plugin loader asks you to do so.

### ⚙️ Settings

After installation, open **Settings → Stickers & Emoji** and find the **UnlimitFavStickers** section.

| Setting | Description |
|---|---|
| **Show notifications** | Enables or disables notifications when a sticker is added to or removed from favorites |
| **Favorite stickers count** | Shows how many favorite stickers are currently saved by the plugin |

### 🛠 How It Works

The plugin hooks Telegram's sticker-related methods through reflection and replaces the favorite stickers logic with its own local database.

| Method | Hook behavior |
|---|---|
| `MediaDataController.addRecentSticker` | Handles adding and removing favorite stickers, then writes changes to the local DB |
| `MediaDataController.getRecentStickers` | Returns favorite stickers from the local DB |
| `MediaDataController.processLoadedRecentDocuments` | Replaces the favorite stickers list during UI updates |
| `MediaDataController.isStickerInFavorites` | Checks whether a sticker is saved as favorite in the local DB |
| `StickersActivity.fillItems` | Adds the plugin settings block to the Stickers settings screen |
| `StickersActivity.onClick` | Handles the notification toggle |
| `StickersActivity.createView` | Fallback bootstrap for installing UI hooks when the screen opens |

On first launch, the plugin imports the already existing Telegram favorite stickers into its local database.

### 📁 Data Storage

```text
/data/data/<telegram_package>/files/stickers.json
/data/data/<telegram_package>/files/stickers.json.bak
/sdcard/Download/unlifavstick_backup.json
```

<details>
<summary><b>JSON database structure</b></summary>

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
        {
          "type": "TL_documentAttributeSticker",
          "alt": "😀",
          "set_id": 789,
          "set_hash": 0
        },
        {
          "type": "TL_documentAttributeImageSize",
          "w": 512,
          "h": 512
        }
      ]
    }
  }
}
```
</details>

The database supports multiple accounts. Each account has its own list of sticker IDs, while sticker document data is stored once in a shared dictionary.

### 🛡 Reliability

- **Delayed saving:** database writes are delayed by 1 second after changes to reduce disk load.
- **Backup file:** the previous database is kept as `stickers.json.bak`.
- **Temporary file:** data is first written to `stickers.json.tmp`, then moved into place.
- **External backup:** a copy is saved as `Downloads/unlifavstick_backup.json`.
- **Auto-restore:** if the main file is missing, the plugin tries to restore from the external backup.
- **Thread safety:** database operations are protected with `threading.RLock()`.

### 📌 Requirements

| Parameter | Value |
|---|---|
| **Minimum Telegram version** | `12.5.1` |
| **Minimum plugin SDK** | `1.4.3.3` |
| **Supported clients** | AyuGram, ExteraGram |
| **Platform** | Android |
| **Storage access** | Needed only for the external backup in Downloads |

---

## 🇺🇦 Опис (UK)

**UnlimitFavStickers** - це плагін для **AyuGram** та **ExteraGram**, який знімає вбудоване обмеження Telegram на кількість улюблених стікерів. Замість використання лише серверного списку Telegram, плагін зберігає улюблені стікери в локальній JSON-базі на пристрої.

Плагін працює у звичайному інтерфейсі Telegram: додавання, видалення, перевірка та показ улюблених стікерів залишаються там само, але без стандартного ліміту.

### ✨ Можливості

| | Функція | Опис |
|:---:|---|---|
| 🔓 | **Без ліміту** | Додавайте стільки улюблених стікерів, скільки потрібно |
| 💾 | **Локальне зберігання** | Улюблені стікери зберігаються в локальній JSON-базі |
| 🔄 | **Автовідновлення** | Якщо основної бази немає, плагін може відновити її з резервної копії в Downloads |
| 📦 | **Імпорт при першому запуску** | Уже наявні улюблені стікери Telegram переносяться в локальну базу |
| 🔔 | **Необов'язкові сповіщення** | Показує сповіщення при додаванні або видаленні, їх можна вимкнути |
| ⚙️ | **Інтеграція в налаштування** | Додає розділ плагіна на екран налаштувань стікерів |
| 👥 | **Підтримка кількох акаунтів** | Для кожного акаунта Telegram зберігається окремий список улюблених |
| 🛡️ | **Надійніше збереження** | Використовує відкладене та потокобезпечне збереження з `.tmp` і `.bak` файлами |
| 🧹 | **Очищення бази** | Видаляє записи стікерів, які більше не використовуються жодним акаунтом |
| 🌐 | **Локалізація** | Вбудовані тексти англійською, українською та російською мовами |

### 🚀 Встановлення

1. Відкрийте **AyuGram** або **ExteraGram**.
2. Перейдіть у **Settings → Plugins**.
3. Натисніть `+` і виберіть `unlifavstick.plugin`.
4. Увімкніть плагін.
5. Перезапустіть застосунок, якщо завантажувач плагінів попросить це зробити.

### ⚙️ Налаштування

Після встановлення відкрийте **Settings → Stickers & Emoji** і знайдіть розділ **UnlimitFavStickers**.

| Налаштування | Опис |
|---|---|
| **Show notifications / Показувати сповіщення** | Вмикає або вимикає сповіщення при додаванні чи видаленні стікера з улюблених |
| **Кількість улюблених стікерів** | Показує, скільки улюблених стікерів зараз збережено плагіном |

### 🛠 Як це працює

Плагін перехоплює методи Telegram, пов'язані зі стікерами, через reflection і замінює логіку улюблених стікерів власною локальною базою.

| Метод | Поведінка хука |
|---|---|
| `MediaDataController.addRecentSticker` | Обробляє додавання та видалення улюблених стікерів, потім записує зміни в локальну БД |
| `MediaDataController.getRecentStickers` | Повертає улюблені стікери з локальної БД |
| `MediaDataController.processLoadedRecentDocuments` | Замінює список улюблених стікерів під час оновлення UI |
| `MediaDataController.isStickerInFavorites` | Перевіряє, чи збережений стікер як улюблений у локальній БД |
| `StickersActivity.fillItems` | Додає блок налаштувань плагіна на екран налаштувань стікерів |
| `StickersActivity.onClick` | Обробляє перемикач сповіщень |
| `StickersActivity.createView` | Запасний bootstrap для встановлення UI-хуків при відкритті екрана |

Під час першого запуску плагін автоматично імпортує вже наявні улюблені стікери Telegram у свою локальну базу.

### 📁 Зберігання даних

```text
/data/data/<telegram_package>/files/stickers.json
/data/data/<telegram_package>/files/stickers.json.bak
/sdcard/Download/unlifavstick_backup.json
```

<details>
<summary><b>Структура JSON-бази</b></summary>

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
        {
          "type": "TL_documentAttributeSticker",
          "alt": "😀",
          "set_id": 789,
          "set_hash": 0
        },
        {
          "type": "TL_documentAttributeImageSize",
          "w": 512,
          "h": 512
        }
      ]
    }
  }
}
```
</details>

База підтримує кілька акаунтів. Кожен акаунт має власний список ID стікерів, а дані документів стікерів зберігаються один раз у спільному словнику.

### 🛡 Надійність

- **Відкладене збереження:** запис у базу відкладається на 1 секунду після змін, щоб зменшити навантаження на диск.
- **Резервний файл:** попередня база зберігається як `stickers.json.bak`.
- **Тимчасовий файл:** дані спочатку записуються в `stickers.json.tmp`, а потім переміщуються на місце основної бази.
- **Зовнішня копія:** копія зберігається як `Downloads/unlifavstick_backup.json`.
- **Автовідновлення:** якщо основного файлу немає, плагін намагається відновити базу із зовнішньої копії.
- **Потокобезпечність:** операції з базою захищені через `threading.RLock()`.

### 📌 Вимоги

| Параметр | Значення |
|---|---|
| **Мінімальна версія Telegram** | `12.5.1` |
| **Мінімальна версія plugin SDK** | `1.4.3.3` |
| **Підтримувані клієнти** | AyuGram, ExteraGram |
| **Платформа** | Android |
| **Доступ до сховища** | Потрібен лише для зовнішньої резервної копії в Downloads |

---

## 🇷🇺 Описание (RU)

**UnlimitFavStickers** - это плагин для **AyuGram** и **ExteraGram**, который снимает встроенное ограничение Telegram на количество избранных стикеров. Вместо использования только серверного списка Telegram, плагин хранит избранные стикеры в локальной JSON-базе на устройстве.

Плагин работает внутри обычного интерфейса Telegram: добавление, удаление, проверка и отображение избранных стикеров остаются там же, но без стандартного лимита.

### ✨ Возможности

| | Функция | Описание |
|:---:|---|---|
| 🔓 | **Без лимита** | Добавляйте любое количество избранных стикеров |
| 💾 | **Локальное хранение** | Избранные стикеры сохраняются в локальной JSON-базе |
| 🔄 | **Авто-восстановление** | Если основная база отсутствует, плагин может восстановить её из бэкапа в Downloads |
| 📦 | **Импорт при первом запуске** | Уже существующие избранные стикеры Telegram переносятся в локальную базу |
| 🔔 | **Необязательные уведомления** | Показывает уведомления при добавлении или удалении, их можно отключить |
| ⚙️ | **Интеграция в настройки** | Добавляет раздел плагина на экран настроек стикеров |
| 👥 | **Поддержка нескольких аккаунтов** | Для каждого аккаунта Telegram хранится отдельный список избранных |
| 🛡️ | **Более надёжное сохранение** | Использует отложенное и потокобезопасное сохранение с `.tmp` и `.bak` файлами |
| 🧹 | **Очистка базы** | Удаляет записи стикеров, которые больше не используются ни одним аккаунтом |
| 🌐 | **Локализация** | Встроенные тексты на английском, украинском и русском языках |

### 🚀 Установка

1. Откройте **AyuGram** или **ExteraGram**.
2. Перейдите в **Settings → Plugins**.
3. Нажмите `+` и выберите `unlifavstick.plugin`.
4. Включите плагин.
5. Перезапустите приложение, если загрузчик плагинов попросит это сделать.

### ⚙️ Настройки

После установки откройте **Settings → Stickers & Emoji** и найдите раздел **UnlimitFavStickers**.

| Настройка | Описание |
|---|---|
| **Show notifications / Показывать уведомления** | Включает или выключает уведомления при добавлении или удалении стикера из избранного |
| **Количество избранных стикеров** | Показывает, сколько избранных стикеров сейчас сохранено плагином |

### 🛠 Как это работает

Плагин перехватывает методы Telegram, связанные со стикерами, через reflection и заменяет логику избранных стикеров собственной локальной базой.

| Метод | Что делает хук |
|---|---|
| `MediaDataController.addRecentSticker` | Обрабатывает добавление и удаление избранных стикеров, затем записывает изменения в локальную БД |
| `MediaDataController.getRecentStickers` | Возвращает избранные стикеры из локальной БД |
| `MediaDataController.processLoadedRecentDocuments` | Подменяет список избранных стикеров при обновлении UI |
| `MediaDataController.isStickerInFavorites` | Проверяет, сохранён ли стикер как избранный в локальной БД |
| `StickersActivity.fillItems` | Добавляет блок настроек плагина на экран настроек стикеров |
| `StickersActivity.onClick` | Обрабатывает переключатель уведомлений |
| `StickersActivity.createView` | Запасной bootstrap для установки UI-хуков при открытии экрана |

При первом запуске плагин автоматически импортирует уже существующие избранные стикеры Telegram в свою локальную базу.

### 📁 Хранение данных

```text
/data/data/<telegram_package>/files/stickers.json
/data/data/<telegram_package>/files/stickers.json.bak
/sdcard/Download/unlifavstick_backup.json
```

<details>
<summary><b>Структура JSON-базы</b></summary>

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
        {
          "type": "TL_documentAttributeSticker",
          "alt": "😀",
          "set_id": 789,
          "set_hash": 0
        },
        {
          "type": "TL_documentAttributeImageSize",
          "w": 512,
          "h": 512
        }
      ]
    }
  }
}
```
</details>

База поддерживает несколько аккаунтов. У каждого аккаунта есть свой список ID стикеров, а данные документов стикеров хранятся один раз в общем словаре.

### 🛡 Надёжность

- **Отложенное сохранение:** запись в базу откладывается на 1 секунду после изменений, чтобы снизить нагрузку на диск.
- **Резервный файл:** предыдущая база сохраняется как `stickers.json.bak`.
- **Временный файл:** данные сначала записываются в `stickers.json.tmp`, затем перемещаются на место основной базы.
- **Внешняя копия:** копия сохраняется как `Downloads/unlifavstick_backup.json`.
- **Авто-восстановление:** если основного файла нет, плагин пытается восстановить базу из внешней копии.
- **Потокобезопасность:** операции с базой защищены через `threading.RLock()`.

### 📌 Требования

| Параметр | Значение |
|---|---|
| **Минимальная версия Telegram** | `12.5.1` |
| **Минимальная версия plugin SDK** | `1.4.3.3` |
| **Поддерживаемые клиенты** | AyuGram, ExteraGram |
| **Платформа** | Android |
| **Доступ к хранилищу** | Нужен только для внешнего бэкапа в Downloads |

---

## 📜 Changelog

### v1.0.0

- Initial release.
- Local favorite stickers database.
- Automatic import of existing favorites.
- Backup copy in Downloads.
- Settings block in Telegram's Stickers settings screen.
- English, Ukrainian, and Russian localization.

---

## 🤝 Contributing

Bug reports and suggestions are welcome in [Issues](https://github.com/Zhmur1k/UnlimitFavStickers/issues). Pull requests are welcome too.

---

## 📄 License

[MIT License](LICENSE)

---

<div align="center">
  <b>Made with ❤️ by <a href="https://t.me/Mr_Zhmurik">@Mr_Zhmurik</a></b>
</div>
