# UnlimitFavStickers

**UnlimitFavStickers** is a plugin that removes the favorite stickers limit and lets you keep a larger personal collection of favorite stickers.

The plugin keeps your favorites available inside Telegram's regular sticker interface, imports your existing favorite stickers on first launch, and adds a small settings block where you can enable or disable add/remove notifications.

## Features

- Removes the favorite stickers limit.
- Keeps favorite stickers separated by Telegram account.
- Imports your existing favorite stickers automatically when the plugin starts for the first time.
- Shows the correct favorite state for stickers.
- Updates the favorite stickers list immediately after adding or removing a sticker.
- Adds a plugin block to the Stickers settings screen.
- Shows the current number of saved favorite stickers.
- Optional notifications when stickers are added to or removed from favorites.
- Interface text is localized in English, Ukrainian, and Russian.
- Stores a local JSON database and creates a backup copy in Downloads.

## Requirements

- Telegram app version: `12.5.1` or newer.
- Plugin SDK version: `1.4.3.3` or newer.
- Android device with a compatible plugin loader.

## Installation

1. Download `unlifavstick.plugin`.
2. Install it through your plugin loader.
3. Enable the plugin.
4. Restart Telegram if your plugin loader asks you to do so.
5. Open stickers and use favorites as usual.

## Settings

Open the plugin settings or Telegram's Stickers settings screen. The plugin adds:

- **Show notifications**: enables or disables small notifications when a sticker is added to or removed from favorites.
- **Favorite stickers count**: shows how many favorite stickers are currently saved by the plugin.

## Data Storage

The plugin stores favorite stickers locally in a JSON file inside the app's private files directory.

For extra safety, it also creates a backup file:

```text
Downloads/unlifavstick_backup.json
```

If the main local database is missing, the plugin tries to restore favorites from this backup.

## Privacy

UnlimitFavStickers does not send your sticker data anywhere. Favorite stickers are stored locally on your device.

## Compatibility Notes

This plugin uses Telegram internal classes and methods. Because of that, future Telegram updates may require a plugin update if Telegram changes the sticker system internally.

## Author

Created by **@Mr_Zhmurik**.

## Version

Current version: `1.0.0`

---

# UnlimitFavStickers українською

**UnlimitFavStickers** - це плагін, який знімає обмеження на кількість улюблених стікерів і дозволяє зберігати більшу особисту колекцію.

Плагін працює всередині звичайного інтерфейсу стікерів Telegram, автоматично імпортує вже додані улюблені стікери під час першого запуску та додає невеликий блок налаштувань для керування сповіщеннями.

## Можливості

- Знімає ліміт улюблених стікерів.
- Зберігає улюблені стікери окремо для кожного акаунта Telegram.
- Автоматично імпортує вже наявні улюблені стікери під час першого запуску.
- Правильно показує, чи доданий стікер до улюблених.
- Оновлює список улюблених одразу після додавання або видалення стікера.
- Додає блок плагіна на екран налаштувань стікерів.
- Показує поточну кількість збережених улюблених стікерів.
- Має необов'язкові сповіщення при додаванні або видаленні стікера з улюблених.
- Має локалізацію англійською, українською та російською мовами.
- Зберігає локальну JSON-базу та створює резервну копію в Downloads.

## Вимоги

- Версія Telegram: `12.5.1` або новіша.
- Версія Plugin SDK: `1.4.3.3` або новіша.
- Android-пристрій із сумісним завантажувачем плагінів.

## Встановлення

1. Завантажте `unlifavstick.plugin`.
2. Встановіть його через ваш завантажувач плагінів.
3. Увімкніть плагін.
4. Перезапустіть Telegram, якщо завантажувач плагінів попросить це зробити.
5. Відкрийте стікери та користуйтеся улюбленими як зазвичай.

## Налаштування

Відкрийте налаштування плагіна або екран налаштувань стікерів у Telegram. Плагін додає:

- **Показувати сповіщення**: вмикає або вимикає невеликі сповіщення при додаванні чи видаленні стікера з улюблених.
- **Кількість улюблених стікерів**: показує, скільки стікерів зараз збережено плагіном.

## Зберігання даних

Плагін зберігає улюблені стікери локально у JSON-файлі всередині приватної папки файлів застосунку.

Для додаткової безпеки він також створює резервну копію:

```text
Downloads/unlifavstick_backup.json
```

Якщо основна локальна база відсутня, плагін спробує відновити улюблені стікери з цієї резервної копії.

## Приватність

UnlimitFavStickers нікуди не надсилає ваші дані про стікери. Улюблені стікери зберігаються локально на вашому пристрої.

## Примітки щодо сумісності

Плагін використовує внутрішні класи та методи Telegram. Через це майбутні оновлення Telegram можуть потребувати оновлення плагіна, якщо Telegram змінить внутрішню систему стікерів.

## Автор

Створено **@Mr_Zhmurik**.

## Версія

Поточна версія: `1.0.0`

---

# UnlimitFavStickers на русском

**UnlimitFavStickers** - это плагин, который снимает ограничение на количество избранных стикеров и позволяет хранить большую личную коллекцию.

Плагин работает внутри обычного интерфейса стикеров Telegram, автоматически импортирует уже добавленные избранные стикеры при первом запуске и добавляет небольшой блок настроек для управления уведомлениями.

## Возможности

- Снимает лимит избранных стикеров.
- Хранит избранные стикеры отдельно для каждого аккаунта Telegram.
- Автоматически импортирует уже существующие избранные стикеры при первом запуске.
- Правильно показывает, добавлен ли стикер в избранное.
- Обновляет список избранных сразу после добавления или удаления стикера.
- Добавляет блок плагина на экран настроек стикеров.
- Показывает текущее количество сохранённых избранных стикеров.
- Поддерживает необязательные уведомления при добавлении или удалении стикера из избранного.
- Имеет локализацию на английском, украинском и русском языках.
- Хранит локальную JSON-базу и создаёт резервную копию в Downloads.

## Требования

- Версия Telegram: `12.5.1` или новее.
- Версия Plugin SDK: `1.4.3.3` или новее.
- Android-устройство с совместимым загрузчиком плагинов.

## Установка

1. Скачайте `unlifavstick.plugin`.
2. Установите его через ваш загрузчик плагинов.
3. Включите плагин.
4. Перезапустите Telegram, если загрузчик плагинов попросит это сделать.
5. Откройте стикеры и пользуйтесь избранным как обычно.

## Настройки

Откройте настройки плагина или экран настроек стикеров в Telegram. Плагин добавляет:

- **Показывать уведомления**: включает или отключает небольшие уведомления при добавлении или удалении стикера из избранного.
- **Количество избранных стикеров**: показывает, сколько стикеров сейчас сохранено плагином.

## Хранение данных

Плагин хранит избранные стикеры локально в JSON-файле внутри приватной папки файлов приложения.

Для дополнительной безопасности он также создаёт резервную копию:

```text
Downloads/unlifavstick_backup.json
```

Если основная локальная база отсутствует, плагин попробует восстановить избранные стикеры из этой резервной копии.

## Приватность

UnlimitFavStickers никуда не отправляет данные о ваших стикерах. Избранные стикеры хранятся локально на вашем устройстве.

## Примечания по совместимости

Плагин использует внутренние классы и методы Telegram. Поэтому будущие обновления Telegram могут потребовать обновления плагина, если Telegram изменит внутреннюю систему стикеров.

## Автор

Создано **@Mr_Zhmurik**.

## Версия

Текущая версия: `1.0.0`
