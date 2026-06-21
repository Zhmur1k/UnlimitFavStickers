import copy
import json
import os
import shutil
import threading
import weakref
from typing import Callable

from android_utils import log
from base_plugin import BasePlugin, HookFilter, MethodHook, hook_filters
from hook_utils import find_class, get_private_field
from java import jclass
from ui.bulletin import BulletinHelper
from ui.settings import Header, Switch

# Метаданные плагина
__id__ = "unlifavstick"
__name__ = "UnlimitFavStickers"
__description__ = """Removes favorite stickers limit
Знімає ліміт улюблених стікерів
Снимает лимит избранных стикеров"""
__author__ = "@Mr_Zhmurik"
__version__ = "1.0.0"
__icon__ = "unlifavstick/0"
__app_version__ = ">=12.5.1"
__sdk_version__ = ">=1.4.3.3"

# Константы
TYPE_FAVE = 2
DB_SAVE_DELAY_SEC = 1.0
EXTERNAL_BACKUP_NAME = "unlifavstick_backup.json"
ROW_PLUGIN_BULLETIN = 100_001
SETTING_SHOW_BULLETIN = "show_bulletin"

# Стандартные Java-классы
Integer = jclass("java.lang.Integer")
Boolean = jclass("java.lang.Boolean")
Object = jclass("java.lang.Object")
ArrayList = jclass("java.util.ArrayList")
TLRPC = jclass("org.telegram.tgnet.TLRPC")
UItem = jclass("org.telegram.ui.Components.UItem")

# Локализация
TRANSLATIONS = {
    "en": {
        "removed": "Sticker removed from favorites",
        "added": "Sticker added to favorites",
        "show_bulletin": "Show notifications",
        "bulletin_sub": "When adding or removing a sticker from favorites",
        "fav_count": "Favorite stickers: {}",
        "main_settings": "Main settings"
    },
    "ru": {
        "removed": "Стикер удалён из избранных",
        "added": "Стикер добавлен в избранные",
        "show_bulletin": "Показывать уведомления",
        "bulletin_sub": "При добавлении и удалении стикера из избранного",
        "fav_count": "Избранных стикеров: {}",
        "main_settings": "Основные настройки"
    },
    "uk": {
        "removed": "Стікер видалено з улюблених",
        "added": "Стікер додано до улюблених",
        "show_bulletin": "Показувати сповіщення",
        "bulletin_sub": "При добавленні та видаленні стікера з улюблених",
        "fav_count": "Улюблених стікерів: {}",
        "main_settings": "Основні налаштування"
    }
}

def get_app_language() -> str:
    """Определяем язык интерфейса Telegram"""
    try:
        LocaleController = find_class("org.telegram.messenger.LocaleController")
        if LocaleController:
            instance = LocaleController.getInstance()
            # Пробуем получить shortName (ru, uk, en)
            locale_info = instance.getCurrentLocaleInfo()
            if locale_info and hasattr(locale_info, "shortName"):
                return str(locale_info.shortName).lower()
            # Если не вышло, берем стандартную локаль Java
            locale = instance.getCurrentLocale()
            if locale:
                return str(locale.getLanguage()).lower()
    except Exception as e:
        log(f"unlifavstick lang error: {e}")
    return "en"

def tr(key: str, *args) -> str:
    lang = get_app_language()
    lang_key = "uk" if lang.startswith("uk") else ("ru" if lang.startswith("ru") else "en")
    text = TRANSLATIONS.get(lang_key, TRANSLATIONS["en"]).get(key, key)
    return text.format(*args) if args else text

# Хелперы для работы с Java-рефлексией
def _resolve_declared_method(clazz, name: str, *param_types):
    try:
        java_clazz = clazz if hasattr(clazz, "getName") else clazz.getClass()
        method = java_clazz.getDeclaredMethod(name, *param_types)
        method.setAccessible(True)
        return method
    except Exception:
        return None

def _documents_to_java_list(documents: list):
    result = ArrayList()
    for doc in documents:
        result.add(doc)
    return result

# Сериализация и десериализация стикеров
def get_sticker_id(sticker) -> int | None:
    if not sticker:
        return None
    if getattr(sticker, "document", None):
        sticker = sticker.document
    return int(sticker.id) if getattr(sticker, "id", None) is not None else None

def serialize_sticker(sticker) -> dict | None:
    if not sticker:
        return None
    try:
        if getattr(sticker, "document", None):
            sticker = sticker.document
        if not sticker or getattr(sticker, "id", None) is None:
            return None

        data = {
            "id": int(sticker.id),
            "access_hash": int(sticker.access_hash) if getattr(sticker, "access_hash", None) else 0,
            "dc_id": int(sticker.dc_id) if getattr(sticker, "dc_id", None) else 0,
            "mime_type": str(sticker.mime_type) if getattr(sticker, "mime_type", None) else "",
            "size": int(sticker.size) if getattr(sticker, "size", None) else 0,
            "attrs": []
        }

        attrs = getattr(sticker, "attributes", None)
        if not attrs:
            return data

        for i in range(attrs.size()):
            attr = attrs.get(i)
            if not attr:
                continue

            attr_type = attr.getClass().getSimpleName()
            item = {"type": str(attr_type)}

            if "TL_documentAttributeSticker" in attr_type:
                item["alt"] = str(attr.alt) if getattr(attr, "alt", None) else ""
                s_set = getattr(attr, "stickerset", None)
                if s_set:
                    item["set_id"] = int(s_set.id) if getattr(s_set, "id", None) else 0
                    item["set_hash"] = int(s_set.access_hash) if getattr(s_set, "access_hash", None) else 0
            elif "TL_documentAttributeImageSize" in attr_type or "TL_documentAttributeVideo" in attr_type:
                if getattr(attr, "w", None) is not None: item["w"] = int(attr.w)
                if getattr(attr, "h", None) is not None: item["h"] = int(attr.h)
                if getattr(attr, "duration", None) is not None: item["duration"] = int(attr.duration)

            data["attrs"].append(item)
        return data
    except Exception as e:
        log(f"serialize_sticker error: {e}")
        return None

def deserialize_sticker(data: dict):
    if not data:
        return None
    try:
        doc = TLRPC.TL_document()
        doc.id = data.get("id", 0)
        doc.access_hash = data.get("access_hash", 0)
        doc.dc_id = data.get("dc_id", 0)
        doc.mime_type = data.get("mime_type", "")
        doc.size = data.get("size", 0)
        doc.date = 0
        doc.thumbs = ArrayList()
        doc.video_thumbs = ArrayList()
        doc.attributes = ArrayList()

        try:
            doc.file_reference = jclass("[B")(0)
        except Exception:
            pass

        for attr_data in data.get("attrs", []):
            attr_type = attr_data.get("type", "")
            if "TL_documentAttributeSticker" in attr_type:
                attr = TLRPC.TL_documentAttributeSticker()
                attr.alt = attr_data.get("alt", "")
                if "set_id" in attr_data:
                    s_set = TLRPC.TL_inputStickerSetID()
                    s_set.id = attr_data["set_id"]
                    s_set.access_hash = attr_data.get("set_hash", 0)
                    attr.stickerset = s_set
                doc.attributes.add(attr)
            elif "TL_documentAttributeImageSize" in attr_type:
                attr = TLRPC.TL_documentAttributeImageSize()
                attr.w = attr_data.get("w", 512)
                attr.h = attr_data.get("h", 512)
                doc.attributes.add(attr)
            elif "TL_documentAttributeVideo" in attr_type:
                attr = TLRPC.TL_documentAttributeVideo()
                attr.w = attr_data.get("w", 512)
                attr.h = attr_data.get("h", 512)
                attr.duration = attr_data.get("duration", 0)
                doc.attributes.add(attr)

        return doc
    except Exception as e:
        log(f"deserialize_sticker error: {e}")
        return None

# Локальная база данных стикеров (JSON)
class StickersDB:
    def __init__(self, db_path: str, show_bulletin: Callable[[], bool]):
        self._db_path = db_path
        self._save_timer = None
        self._lock = threading.RLock()
        self._cache = {}
        self.show_bulletin = show_bulletin
        self._stickers = {"accounts": {}, "stickers": {}}
        self._load()
        self.cleanup()

    def _downloads_backup_path(self) -> str:
        Env = jclass("android.os.Environment")
        download_dir = Env.getExternalStoragePublicDirectory(Env.DIRECTORY_DOWNLOADS)
        return os.path.join(str(download_dir.getAbsolutePath()), EXTERNAL_BACKUP_NAME)

    def _load(self) -> None:
        with self._lock:
            self._cache.clear()

            # Восстановление из бэкапа, если файла нет
            if not os.path.exists(self._db_path):
                try:
                    ext_path = self._downloads_backup_path()
                    if os.path.exists(ext_path):
                        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
                        shutil.copy2(ext_path, self._db_path)
                        log("StickersDB: restored from backup")
                except Exception as e:
                    log(f"StickersDB: restore error: {e}")

            # Загрузка основного JSON или резервного .bak
            for path in (self._db_path, f"{self._db_path}.bak"):
                if os.path.exists(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            self._stickers = json.load(f)
                            return
                    except Exception as e:
                        log(f"StickersDB: failed to load {path}: {e}")

            self._stickers = {"accounts": {}, "stickers": {}}

    def _save_task(self, snapshot: dict) -> None:
        tmp_path = f"{self._db_path}.tmp"
        bak_path = f"{self._db_path}.bak"
        try:
            os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, ensure_ascii=False, indent=2)

            if os.path.exists(self._db_path):
                if os.path.exists(bak_path):
                    os.remove(bak_path)
                os.rename(self._db_path, bak_path)

            os.replace(tmp_path, self._db_path)

            # Копируем в "Загрузки" для надежности
            try:
                shutil.copy2(self._db_path, self._downloads_backup_path())
            except Exception:
                pass
        except Exception as e:
            log(f"StickersDB save error: {e}")
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass

    def _schedule_save(self) -> None:
        with self._lock:
            if self._save_timer:
                self._save_timer.cancel()
            self._save_timer = threading.Timer(DB_SAVE_DELAY_SEC, self._save_task, [copy.deepcopy(self._stickers)])
            self._save_timer.start()

    def get_all_stickers(self, account) -> list:
        acc = str(account)
        with self._lock:
            if acc in self._cache:
                return list(self._cache[acc])

            ids = self._stickers.get("accounts", {}).get(acc, [])
            if not ids:
                return []

            documents = []
            storage = self._stickers.get("stickers", {})
            for sid in reversed(ids):
                raw = storage.get(sid)
                if raw:
                    doc = deserialize_sticker(raw)
                    if doc:
                        documents.append(doc)

            self._cache[acc] = documents
            return list(documents)

    def add_sticker(self, sticker, account) -> None:
        serialized = serialize_sticker(sticker)
        if not serialized:
            return

        sid = str(serialized["id"])
        acc = str(account)
        with self._lock:
            self._stickers.setdefault("stickers", {})[sid] = serialized
            acc_ids = self._stickers.setdefault("accounts", {}).setdefault(acc, [])
            if sid not in acc_ids:
                acc_ids.append(sid)
                self._cache.pop(acc, None)
                self._schedule_save()

    def remove_sticker(self, sticker, account) -> None:
        sticker_id = get_sticker_id(sticker)
        if sticker_id is None:
            return

        sid = str(sticker_id)
        acc = str(account)
        with self._lock:
            acc_ids = self._stickers.get("accounts", {}).get(acc, [])
            if sid in acc_ids:
                acc_ids.remove(sid)
                self._cache.pop(acc, None)
                self._schedule_save()

            storage = self._stickers.get("stickers", {})
            if sid in storage:
                # Удаляем сам стикер из базы только если он больше не используется на других аккаунтах
                if not any(sid in ids for ids in self._stickers.get("accounts", {}).values()):
                    del storage[sid]
                    self._schedule_save()

    def cleanup(self) -> None:
        with self._lock:
            try:
                used = {str(x) for ids in self._stickers.get("accounts", {}).values() for x in ids}
                storage = self._stickers.get("stickers", {})
                orphans = [sid for sid in list(storage.keys()) if sid not in used]
                for sid in orphans:
                    del storage[sid]
                if orphans:
                    self._schedule_save()
            except Exception as e:
                log(f"StickersDB cleanup error: {e}")

    def is_sticker_favorite(self, sticker, account) -> bool:
        sticker_id = get_sticker_id(sticker)
        if sticker_id is None:
            return False
        return str(sticker_id) in self._stickers.get("accounts", {}).get(str(account), [])

    def count_stickers(self, account) -> int:
        return len(self._stickers.get("accounts", {}).get(str(account), []))


# Хуки для MediaDataController
class ChangeFavoriteStickerHook(MethodHook):
    def __init__(self, media_instance, db: StickersDB, get_account_id: Callable[[], str]):
        self.media_instance = media_instance
        self.db = db
        self.get_account_id = get_account_id

    def before_hooked_method(self, param):
        try:
            if not param.args or len(param.args) < 5 or param.args[0] != TYPE_FAVE:
                return

            sticker = param.args[2]
            is_remove = param.args[4]
            if not sticker:
                return

            account_id = self.get_account_id()
            if is_remove:
                self.db.remove_sticker(sticker, account_id)
                if self.db.show_bulletin():
                    BulletinHelper.show_error(tr("removed"))
            else:
                self.db.add_sticker(sticker, account_id)
                if self.db.show_bulletin():
                    BulletinHelper.show_success(tr("added"))

            # Обновляем UI в Telegram
            favorites = _documents_to_java_list(self.db.get_all_stickers(account_id))
            try:
                self.media_instance.processLoadedRecentDocuments(TYPE_FAVE, favorites, False, 0, False)
            except Exception:
                pass

            param.setResult(None)
        except Exception as e:
            log(f"ChangeFavoriteStickerHook error: {e}")


class GetFavoriteStickersHook(MethodHook):
    def __init__(self, db: StickersDB, get_account_id: Callable[[], str]):
        self.db = db
        self.get_account_id = get_account_id

    def after_hooked_method(self, param):
        try:
            if not param.args or param.args[0] != TYPE_FAVE:
                return
            favorites = self.db.get_all_stickers(self.get_account_id())
            param.setResult(_documents_to_java_list(favorites))
        except Exception as e:
            log(f"GetFavoriteStickersHook error: {e}")


class ProcessLoadedRecentDocumentsHook(MethodHook):
    def __init__(self, db: StickersDB, get_account_id: Callable[[], str]):
        self.db = db
        self.get_account_id = get_account_id

    def before_hooked_method(self, param):
        try:
            if not param.args or len(param.args) < 3 or param.args[0] != TYPE_FAVE or param.args[2]:
                return
            favorites = self.db.get_all_stickers(self.get_account_id())
            param.args[1] = _documents_to_java_list(favorites)
        except Exception as e:
            log(f"ProcessLoadedRecentDocumentsHook error: {e}")


class IsStickerInFavoritesHook(MethodHook):
    def __init__(self, is_favorite: Callable, get_account_id: Callable[[], str]):
        self._is_favorite = is_favorite
        self._get_account_id = get_account_id

    def before_hooked_method(self, param):
        try:
            if not param.args:
                return
            sticker = param.args[0]
            if not sticker:
                param.setResult(False)
                return
            param.setResult(self._is_favorite(sticker, self._get_account_id()))
        except Exception as e:
            log(f"IsStickerInFavoritesHook error: {e}")
            param.setResult(False)


# Интеграция настроек в StickersActivity
class StickersActivityReflection:
    @staticmethod
    def resolve_fill_items_method(clazz):
        java_clazz = clazz if hasattr(clazz, "getName") else clazz.getClass()
        adapter = jclass("org.telegram.ui.Components.UniversalAdapter")
        for al_type in (ArrayList, ArrayList.getClass(), find_class("java.util.ArrayList")):
            if not al_type: continue
            method = _resolve_declared_method(java_clazz, "fillItems", al_type, adapter)
            if method: return method
        return None

    @staticmethod
    def resolve_on_click_method(clazz):
        java_clazz = clazz if hasattr(clazz, "getName") else clazz.getClass()
        view = jclass("android.view.View")
        uitem = jclass("org.telegram.ui.Components.UItem")
        return _resolve_declared_method(java_clazz, "onClick", uitem, view, Integer.TYPE, jclass("java.lang.Float").TYPE, jclass("java.lang.Float").TYPE)

    @staticmethod
    def resolve_create_view_method(clazz):
        return _resolve_declared_method(clazz, "createView", jclass("android.content.Context"))


class StickersActivitySettings:
    @staticmethod
    def _item_id(item) -> int:
        try: return int(item.id)
        except Exception:
            try: return int(item.getId())
            except Exception: return -1

    @staticmethod
    def _already_injected(items) -> bool:
        for i in range(items.size()):
            if StickersActivitySettings._item_id(items.get(i)) == ROW_PLUGIN_BULLETIN:
                return True
        return False

    @staticmethod
    def _build_plugin_rows(plugin, get_account_id: Callable[[], str]):
        show_bulletin = plugin.get_setting(SETTING_SHOW_BULLETIN, True)
        count = plugin.db.count_stickers(get_account_id())
        return [
            UItem.asHeader(__name__),
            UItem.asCheck(ROW_PLUGIN_BULLETIN, tr("show_bulletin")).setChecked(show_bulletin),
            UItem.asShadow(tr("fav_count", count)),
        ]

    @staticmethod
    def _is_sticker_set_item(item) -> bool:
        try:
            obj = getattr(item, "object", None)
            return obj and "TL_messages_stickerSet" in obj.getClass().getName()
        except Exception:
            return False

    @staticmethod
    def _my_packs_header_title() -> str | None:
        try:
            LocaleController = find_class("org.telegram.messenger.LocaleController")
            R_string = find_class("org.telegram.messenger.R$string")
            return LocaleController.getString("ChooseStickerMyStickerSets", R_string.ChooseStickerMyStickerSets)
        except Exception:
            return None

    @staticmethod
    def _find_my_packs_insert_index(items, adapter) -> int:
        title = StickersActivitySettings._my_packs_header_title()
        if title:
            for i in range(items.size()):
                if str(getattr(items.get(i), "text", "")) == str(title):
                    return i

        for i in range(items.size()):
            if StickersActivitySettings._is_sticker_set_item(items.get(i)):
                return i

        try:
            white_sections = get_private_field(adapter, "whiteSections")
            if white_sections and white_sections.size() > 0:
                offset = int(getattr(adapter, "itemsOffset", 0) or 0)
                return max(0, int(white_sections.get(0).start) - offset)
        except Exception:
            pass
        return items.size()

    @staticmethod
    def inject_rows(items, adapter, plugin, get_account_id: Callable[[], str]) -> None:
        if not items or StickersActivitySettings._already_injected(items):
            return

        rows = StickersActivitySettings._build_plugin_rows(plugin, get_account_id)
        row_count = len(rows)
        white_sections = get_private_field(adapter, "whiteSections")
        insert_at = StickersActivitySettings._find_my_packs_insert_index(items, adapter)

        # Обычная вставка строк
        for i in range(row_count - 1, -1, -1):
            items.add(insert_at, rows[i])

        # Двигаем секции UI, чтобы не поплыли фоны
        if white_sections:
            for i in range(white_sections.size()):
                sec = white_sections.get(i)
                if sec.start >= insert_at: sec.start += row_count
                if sec.end >= insert_at: sec.end += row_count

            new_sec = jclass("org.telegram.ui.Components.UniversalAdapter$Section")()
            new_sec.start = insert_at
            new_sec.end = insert_at + row_count - 1
            white_sections.add(0, new_sec)

        reorder = get_private_field(adapter, "reorderSections")
        if reorder:
            for i in range(reorder.size()):
                sec = reorder.get(i)
                if sec.start >= insert_at: sec.start += row_count
                if sec.end >= insert_at: sec.end += row_count

        try:
            m = adapter.getClass().getDeclaredMethod("updateReorderSections")
            m.setAccessible(True)
            m.invoke(adapter)
        except Exception:
            pass

    @staticmethod
    def is_stickers_screen(fragment) -> bool:
        try:
            MediaDataController = find_class("org.telegram.messenger.MediaDataController")
            return get_private_field(fragment, "currentType") == MediaDataController.TYPE_IMAGE
        except Exception:
            return True


class StickersFillItemsHook:
    def __init__(self, plugin, get_account_id: Callable[[], str]):
        self._plugin_ref = weakref.ref(plugin)
        self._get_account_id = get_account_id

    @hook_filters(
        HookFilter.Condition("param.thisObject != null"),
        HookFilter.ArgumentNotNull(0),
        HookFilter.ArgumentNotNull(1),
    )
    def after_hooked_method(self, param):
        plugin = self._plugin_ref()
        if plugin and StickersActivitySettings.is_stickers_screen(param.thisObject):
            StickersActivitySettings.inject_rows(param.args[0], param.args[1], plugin, self._get_account_id)


class StickersOnClickHook:
    def __init__(self, plugin):
        self._plugin_ref = weakref.ref(plugin)

    @hook_filters(HookFilter.Condition("param.thisObject != null"), HookFilter.ArgumentNotNull(0))
    def before_hooked_method(self, param):
        try:
            item = param.args[0]
            if not item or StickersActivitySettings._item_id(item) != ROW_PLUGIN_BULLETIN:
                return

            plugin = self._plugin_ref()
            if not plugin:
                return

            new_val = not plugin.get_setting(SETTING_SHOW_BULLETIN, True)
            plugin.set_setting(SETTING_SHOW_BULLETIN, new_val)

            view = param.args[1]
            if view:
                view.setChecked(new_val)

            param.setResult(None)
        except Exception as e:
            log(f"OnClick hook error: {e}")


class StickersActivityBootstrapHook(MethodHook):
    def __init__(self, plugin):
        self._plugin_ref = weakref.ref(plugin)

    def after_hooked_method(self, param):
        plugin = self._plugin_ref()
        if plugin and not plugin._stickers_ui_hooked:
            try:
                plugin._install_stickers_activity_hooks(param.thisObject.getClass())
            except Exception as e:
                log(f"Bootstrap failed: {e}")


# Класс плагина
class UnlimitFavStickersPlugin(BasePlugin):
    _db: StickersDB | None = None

    def create_settings(self):
        return [
            Header(text=tr("main_settings")),
            Switch(
                key=SETTING_SHOW_BULLETIN,
                text=tr("show_bulletin"),
                default=True,
                subtext=tr("bulletin_sub"),
            ),
        ]

    @property
    def db(self) -> StickersDB:
        if self._db is None:
            show_bull = lambda: self.get_setting(SETTING_SHOW_BULLETIN, True)
            try:
                context = jclass("android.app.ActivityThread").currentApplication()
                path = os.path.join(str(context.getFilesDir()), "stickers.json")
            except Exception:
                path = "stickers.json"
            self._db = StickersDB(path, show_bull)
        return self._db

    @staticmethod
    def _selected_account_id() -> str:
        try:
            UserConfig = find_class("org.telegram.messenger.UserConfig")
            u_id = UserConfig.getInstance(UserConfig.selectedAccount).clientUserId
            return str(u_id)
        except Exception:
            return "0"

    def _install_media_hooks(self, media_instance, media_class) -> None:
        TLRPCDocument = find_class("org.telegram.tgnet.TLRPC$Document")
        acc_id = self._selected_account_id

        hooks = (
            ("addRecentSticker", (Integer.TYPE, Object, TLRPCDocument, Integer.TYPE, Boolean.TYPE), ChangeFavoriteStickerHook(media_instance, self.db, acc_id)),
            ("getRecentStickers", (Integer.TYPE,), GetFavoriteStickersHook(self.db, acc_id)),
            ("processLoadedRecentDocuments", (Integer.TYPE, ArrayList, Boolean.TYPE, Integer.TYPE, Boolean.TYPE), ProcessLoadedRecentDocumentsHook(self.db, acc_id)),
            ("isStickerInFavorites", (TLRPCDocument,), IsStickerInFavoritesHook(self.db.is_sticker_favorite, acc_id)),
        )

        for name, sig, hook in hooks:
            try:
                m = media_class.getDeclaredMethod(name, *sig)
                m.setAccessible(True)
                self.hook_method(m, hook)
            except Exception as e:
                log(f"Failed to hook {name}: {e}")

    def _install_stickers_activity_hooks(self, stickers_class) -> None:
        if self._stickers_ui_hooked:
            return

        fill_m = StickersActivityReflection.resolve_fill_items_method(stickers_class)
        if fill_m:
            self.hook_method(fill_m, StickersFillItemsHook(self, self._selected_account_id))

        click_m = StickersActivityReflection.resolve_on_click_method(stickers_class)
        if click_m:
            self.hook_method(click_m, StickersOnClickHook(self))

        self._stickers_ui_hooked = True

    def _import_existing_favorites(self, media_controller) -> None:
        try:
            acc = self._selected_account_id()
            if self.db.get_all_stickers(acc):
                return
            stickers = media_controller.getRecentStickers(TYPE_FAVE)
            if stickers:
                for i in range(stickers.size() - 1, -1, -1):
                    sticker = stickers.get(i)
                    if sticker: self.db.add_sticker(sticker, acc)
        except Exception as e:
            log(f"Import failed: {e}")

    def on_plugin_load(self):
        self._stickers_ui_hooked = False

        try:
            MediaDataController = find_class("org.telegram.messenger.MediaDataController")
            UserConfig = find_class("org.telegram.messenger.UserConfig")
            media_instance = MediaDataController.getInstance(int(UserConfig.selectedAccount))
            media_class = media_instance.getClass()
        except Exception as e:
            log(f"Plugin load aborted: {e}")
            return

        self._install_media_hooks(media_instance, media_class)

        try:
            StickersActivity = find_class("org.telegram.ui.StickersActivity")
            if StickersActivity:
                try:
                    self._install_stickers_activity_hooks(StickersActivity)
                except Exception:
                    pass

                create_view = StickersActivityReflection.resolve_create_view_method(StickersActivity)
                if create_view:
                    self.hook_method(create_view, StickersActivityBootstrapHook(self))
        except Exception as e:
            log(f"StickersActivity hooks error: {e}")

        self._import_existing_favorites(media_instance)