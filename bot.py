import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================
# КАТЕГОРИИ И МОДЕЛИ
# ==============================

# Словарь с категориями и моделями
# Формат: "Категория": {"Название модели": "ссылка"}
CATEGORIES = {
    "🤖 Роботы-пылесосы": {
        "F9 Pro": "https://drive.google.com/file/d/13wR8298IxvStbAgVth3qDSNjZXAdJ1oo/view?usp=sharing",
        "Серия F10": "https://drive.google.com/file/d/1sy6nVkmlPsFiBfTqgA-aUIv2fFlWlMe-/view?usp=sharing",
        "F20": "https://drive.google.com/file/d/16iClR2rCSxol9e7Y0MaS_wZA-smvqguI/view?usp=drive_link",
        "F21": "https://drive.google.com/file/d/1r6rgzsu7JUPmkEL0G2O0ZJf1Nbfi_Z6L/view?usp=drive_link",
        "F21 Plus": "https://drive.google.com/file/d/1DzbMNFHMA6UMFvvuYZjMj3i6bcKzcF1_/view?usp=drive_link",
        "D9 Max": "https://drive.google.com/file/d/1wBjsxSqBmUPBjTmX746QBpt5-DuR_3RW/view?usp=sharing",
        "D9 Max Gen 2": "https://drive.google.com/file/d/1gTLwFyc3xi0ML-u2jeneAG4P-kfq8L21/view?usp=sharing",
        "D9 Plus": "https://drive.google.com/file/d/12qiVcKDveHIU_f8Tla4c2yM6AM0nOmrO/view?usp=sharing",
        "D10 Plus": "https://drive.google.com/file/d/1Rt4YEIy9arwYRJTLmqJxQg1poEGOY7dn/view?usp=sharing",
        "D10 Plus Gen 2": "https://drive.google.com/file/d/1votHcznDR7swe5zsFMudfFTLwAYxS3-h/view?usp=sharing",
        "D10s": "https://drive.google.com/file/d/116E7XKRvzPOzTL0_XbbhzxdpIl764X8m/view?usp=sharing",
        "D10s Pro & D10s Plus": "https://drive.google.com/file/d/1KqHR4iqWNS9xGUHQQwIC6c2yME03I1xK/view?usp=sharing",
        "Серия D20": "https://drive.google.com/file/d/1xoLmc19FdZ1KO6QwmSQOurjlq9m627Z1/view?usp=sharing",
        "D30 Ultra": "https://drive.google.com/file/d/1h09RyyVI3U_eSUv4rLhf8AYF1CHutqIB/view?usp=sharing",
        "L10s Pro": "https://drive.google.com/file/d/1lS4GvYu2N9grGjpkIuD7OdGN8ighc7mT/view?usp=sharing",
        "L10s Plus & L10s Pro Gen 2": "https://drive.google.com/file/d/14mVqy3pRrSCXRmk3FAm_FhX4BRS8pJQ6/view?usp=sharing",
        "L10 Ultra & L10 Prime": "https://drive.google.com/file/d/1oJsTXZWjRif2nkwlKd4lhlJfJd277-I1/view?usp=sharing",
        "L10s Ultra": "https://drive.google.com/file/d/1NYmzDMmTlKwu1zfpKjx4Hj3RCe-V5GTW/view?usp=sharing",
        "L10s Pro Ultra": "https://drive.google.com/file/d/1REboK4uDTxr-6OkQkkLEhLxhMf6vJiBs/view?usp=sharing",
        "L20 Ultra Complete": "https://drive.google.com/file/d/1zOy89Qk9_8Z7znmPZnsB-Mzu6tZCOC2h/view?usp=sharing",
        "L30 Ultra": "https://drive.google.com/file/d/1iE5qjzi_hG3B78gckgKnwHIUmnthCcwG/view?usp=sharing",
        "L40": "https://drive.google.com/file/d/1utwXSMpuqN8tayfsSVq4SBQdBPeslYLw/view?usp=sharing",
        "L40 Ultra CE & L40s Ultra": "https://drive.google.com/file/d/1Zl0vstqYpY352WXco99xM-IfLulrlYjE/view?usp=sharing",
        "L40 Ultra AE": "https://drive.google.com/file/d/1PjfGgxi3s-ORL6Hjp6EegOJFlwHZWntD/view?usp=sharing",
        "L40s Pro Ultra": "https://drive.google.com/file/d/1VDzSg2dt-QKLLrHt7Tyh21c-p9BqUvU0/view?usp=sharing",
        "X40 Ultra Complete": "https://drive.google.com/file/d/1ZnzT0SfkNYqOfIcUIry3hbHrKWaiOMLn/view?usp=sharing",
        "Серия X50": "https://drive.google.com/file/d/1DXNdbdL-S9hpqVzLh5nKhnWEBqQwMIiX/view?usp=sharing",
        "Matrix10 Ultra": "https://drive.google.com/file/d/1v9Mq4HcEMHPWjde8Hs5RmVf1tB1QysxG/view?usp=sharing",
        "Aqua10 Ultra Roller Complete": "https://drive.google.com/file/d/1MQH2gjmZbcNh3tPGRXx-AXJOW5D76BVh/view?usp=sharing",
        # ДОБАВЛЯЙ НОВЫЕ МОДЕЛИ СЮДА
        # "Новая модель": "https://drive.google.com/...",
    },
    
    "🔋 Вертикальные пылесосы": {
        "U10 & U20": "https://drive.google.com/file/d/1FU47npYBwANB3We5TxodDRxMCi_PfB-2/view?usp=sharing",
        "R10 & R10 Pro": "https://drive.google.com/file/d/1Y0Cc2PHNcDv-qzA1dZmWE5f1h6c65Ibh/view?usp=sharing",
        "R10 Pro Aqua": "https://drive.google.com/file/d/1sMrU6wg8wewy8UmFWWQum0N3ujl9WqlZ/view?usp=sharing",
        "R10s Essential": "https://drive.google.com/file/d/18iNmkZYaFkAgtIOXo17omRGLNPZa87y9/view?usp=sharing",
        "R10s & R10s Pro": "https://drive.google.com/file/d/1X7T3BmiTP_L8LfcADoT7l7dYy7fV-xzz/view?usp=sharing",
        "R10s Aqua": "https://drive.google.com/file/d/189t5xtKhEQVGC-BFOp6rUokouZAtucf7/view?usp=sharing",
        "R20 Essential": "https://drive.google.com/file/d/1bE5C5noY_0QeT_u2z2xbcQ-ytXhyICHH/view?usp=sharing",
        "R20": "https://drive.google.com/file/d/1vcD0W8v8ZcW6eyuETZn0xPFtTRI5f_IP/view?usp=sharing",
        "R20 Aqua": "https://drive.google.com/file/d/17Bb3ntnLFX5DjV2Lx7VHMcy_Q-SuXuoT/view?usp=sharing",
        "Z10 Station": "https://drive.google.com/file/d/1a3kfIBwz48PaXAHocRsrG9qc32_rTtt9/view?usp=sharing",
        "Z20 Essential": "https://drive.google.com/file/d/1p4qVkD_OBQ4sKQxsO5P9z26JfXwBFDVx/view?usp=sharing",
        "Z20 & Z30": "https://drive.google.com/file/d/1FfiAdLziAA-U2_KxwYzLzZFEU_9Zhohu/view?usp=sharing",
        "Z20 AC & Z30 AC": "https://drive.google.com/file/d/1eJWOgOH-CpglP1JQNiBZ_j0ne7UEW8Ad/view?usp=sharing",
        "Z40 Station": "https://drive.google.com/file/d/1DIrcAoRze1hTcL2GBXu1g3QcGMSZJNJo/view?usp=sharing",
        "E10": "https://drive.google.com/file/d/1Q351DBeXaZUuX1tgGwzVsMrdWvraiwPN/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },

        "💦 Моющие пылесосы": {
        "G10 & G10 Combo": "https://drive.google.com/file/d/1MqAig9fKesw0TUZggfHuC2QUAXaZZsP3/view?usp=sharing",
        "G10 Pro": "https://drive.google.com/file/d/1S_VUpB5JlF6UG9YYVC3GvNC6Y6EXQ0IV/view?usp=sharing",
        "H11 Core": "https://drive.google.com/file/d/1dG_6bVJmmPRS-za51t4NbvAkcLTREhAB/view?usp=sharing",
        "H12 & H12 Core": "https://drive.google.com/file/d/109pLAe7zgOG3kWduEiNy5xZy8hx8XikA/view?usp=sharing",
        "H12S": "https://drive.google.com/file/d/1Is7XTMDEa-_1IJ_KAAE7aPs8VHP65aWe/view?usp=sharing",
        "H12S AE": "https://drive.google.com/file/d/1pp9Ry8HnYlT7AsiQQIN7X6vR0Hon78a-/view?usp=sharing",
        "H12 Pro & H12 Dual": "https://drive.google.com/file/d/17_s6yJfy4HVJGMPcvGURMGYJC0Q5wANv/view?usp=sharing",
        "H12 FlexReach": "https://drive.google.com/file/d/1COScv0C26KiiMbzjh4OoXwzNV5IcxTkH/view?usp=sharing",
        "H12 Pro FlexReach": "https://drive.google.com/file/d/1mSDOTl4St2lSI5X9tZ6jVzUvWSfrnu0P/view?usp=sharing",
        "H12 Dual FlexReach": "https://drive.google.com/file/d/1aYwXkr5JY8h1JpJS7db3xHs8a-KEa4yY/view?usp=sharing",
        "H13 Pro": "https://drive.google.com/file/d/1aYwXkr5JY8h1JpJS7db3xHs8a-KEa4yY/view?usp=sharing",
        "H14 Dual": "https://drive.google.com/file/d/1PBogCf1CE05zMixTaZpicE45r5PlPLwu/view?usp=sharing",
        "H15 Pro Heat": "https://drive.google.com/file/d/1r5HFJVRUDPQj9lL0ENld-vY3vZ5P5RO5/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },

    "🌿 Роботы-газонокосилки": {
        "A1 Pro": "https://drive.google.com/file/d/1lWlK8bxwg55hk-cxuC4ufZ5fJvgoGR_Q/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },

    "✨ Техника для ухода": {
        "Mini": "https://drive.google.com/file/d/1h8gF6RRdx9sByoTDmHjouPbUGTnXw2NB/view?usp=sharing",
        "Gleam": "https://drive.google.com/file/d/1Gt5DPdOap7oSWOpD8zQfn0Y4-0oZ5HSD/view?usp=sharing",
        "Glory": "https://drive.google.com/file/d/1aTPvu7VKsgt056MsJkO8qg7TpE8-CJ1X/view?usp=sharing",
        "Glory Mix": "https://drive.google.com/file/d/1AwPVFenkaG-NVl0zufGUEzSQYrXHkS2u/view?usp=sharing",
        "Glory Master": "https://drive.google.com/file/d/11P2i1089RdeSVWutM_zUGCVa9w_Pxdsc/view?usp=sharing",
        "Pocket": "https://drive.google.com/file/d/14SPXV7CNyiRXIBkC0LTz0SnQt5aAdgZP/view?usp=sharing",
        "Pocket Ultra": "https://drive.google.com/file/d/11JNsWC8u_rrOLt5YwcgIlASxpa2giqBF/view?usp=sharing",
        "Gusto": "https://drive.google.com/file/d/1p1SKo0Ue9WtQbOUyEJYD2-bvkKhbYyJa/view?usp=sharing",
        "Miracle": "https://drive.google.com/file/d/16RBqYGBc46qt_VegWHqZ6i_qxgk2WeLH/view?usp=sharing",
        "Miracle Pro": "https://drive.google.com/file/d/1OyInKC4XWuTpGPH896JlQJ93SQJTHT-N/view?usp=sharing",
        "Pilot": "https://drive.google.com/file/d/1ASrlxeR_RpPx33-hDT3zeqIacaQnJJjg/view?usp=sharing",
        "Dazzle": "https://drive.google.com/file/d/1EUipnwwGm8qzGKZUiCPV4d_yY8T4xeQe/view?usp=sharing",
        "AirStyle": "https://drive.google.com/file/d/1ODzX8nIFE25Vn1xe4k0dHfv09NUa1keF/view?usp=sharing",
        "AirStyle Pro": "https://drive.google.com/file/d/1ZG4Q_JSJmf56B-vSwFWQDVIEqeonccxx/view?usp=sharing",
        "AirStyle Pro Hi": "https://disk.yandex.ru/i/olq0VW3gPYt89Q",
        "Aero Straight": "https://drive.google.com/file/d/1mSQL-aGY3pWKg7OgU5QO3xEusLuPA1ge/view?usp=sharing",
        "Hair Removal": "https://drive.google.com/file/d/18lpPBEhpzPuuQT9TcDov9T3lZ9Kzn8wJ/view?usp=sharing",
        "S7": "https://drive.google.com/file/d/1yxitvnxo3cqcxgaMWGhFBviQnhtTUNcA/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },
    
    "🌡️ Климат": {
        "PM10 & PM20": "https://drive.google.com/file/d/1oyKd_w74F_xDrZ35nR0RaztHmznvN8qu/view?usp=sharing",
        "PM30": "https://drive.google.com/file/d/1j9ffL1VKCPUZVvk1SFUWQuLo9bvG6-I8/view?usp=sharing",
        "H40 & H40 Essential": "https://drive.google.com/file/d/1NGEZFnKBrh7TfPnwh5NgK67oIpxkhvp9/view?usp=sharing",
        "AP10": "https://drive.google.com/file/d/1EF1IeQ4D7JxSs0RgZlCb1pPEKZvHQLPX/view?usp=sharing",
        "HT30 Ultra": "https://drive.google.com/file/d/1MqBIguhks73Nms-7ugvl3NFFzigZGWmW/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },
    
    "🍗 Аэрогрили": {
        "AF30": "https://drive.google.com/file/d/1m5vy8vibl9xKRUel40szD-qTf9EPkYIm/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ АЭРОГРИЛЕЙ ЗДЕСЬ
        # "Пример аэрогриля": "https://drive.google.com/...",
    },

    "🏠 Для дома": {
        "S10": "https://drive.google.com/file/d/19LdvfW8IVe1T6trhgimYk764z1V2-uZp/view?usp=sharing",
        "DF10 & DF10 Pro": "https://drive.google.com/file/d/1RWR_zJW1Jhm7hpFnw1aWgAHGUwc__Qc0/view?usp=sharing",
        # ДОБАВЬ МОДЕЛИ ДЛЯ ЭТОЙ КАТЕГОРИИ ЗДЕСЬ
        # "Пример модели": "https://drive.google.com/...",
    },
}

# Маппинг коротких имен категорий для callback_data
CATEGORY_SHORT_NAMES = {
    "🤖 Роботы-пылесосы": "robots",
    "✨ Техника для ухода": "care",
    "🌿 Роботы-газонокосилки": "mowers",
    "💦 Моющие пылесосы": "wash",
    "🌡️ Климат": "climate",
    "🏠 Для дома": "home",
    "🔋 Вертикальные пылесосы": "vertical",
    "🍗 Аэрогрили": "airfry",
}

# Обратный маппинг
SHORT_TO_FULL_CATEGORY = {v: k for k, v in CATEGORY_SHORT_NAMES.items()}

# ==============================
# ФУНКЦИИ ДЛЯ СОЗДАНИЯ КЛАВИАТУР
# ==============================

def create_main_keyboard():
    """Создает главную клавиатуру с категориями"""
    keyboard = []
    categories = list(CATEGORIES.keys())
    
    # Сортируем категории, чтобы "🤖 Роботы-пылесосы" была первой
    if "🤖 Роботы-пылесосы" in categories:
        categories.remove("🤖 Роботы-пылесосы")
        categories.insert(0, "🤖 Роботы-пылесосы")
    
    # Создаем кнопки категорий (по 1 в ряд)
    for category_name in categories:
        model_count = len(CATEGORIES[category_name])
        short_name = CATEGORY_SHORT_NAMES.get(category_name, "unknown")
        display_text = f"{category_name} [{model_count}]" if model_count > 0 else f"{category_name} [0]"
        keyboard.append([InlineKeyboardButton(display_text, callback_data=f"cat_{short_name}")])
    
    # Добавляем кнопку помощи
    keyboard.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    
    return InlineKeyboardMarkup(keyboard)

def create_category_keyboard(category_short_name):
    """Создает клавиатуру с моделями выбранной категории"""
    category_name = SHORT_TO_FULL_CATEGORY.get(category_short_name)
    if not category_name:
        # Если передан callback_name, ищем полное имя с эмодзи
        for full_name in CATEGORIES.keys():
            if category_short_name in full_name:
                category_name = full_name
                break
    
    if not category_name:
        # Если категория не найдена
        keyboard = [
            [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    models = CATEGORIES.get(category_name, {})
    
    if not models:
        # Если категория пустая
        keyboard = [
            [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    keyboard = []
    models_list = list(models.keys())
    
    # Создаем кнопки моделей (по 1 в ряд для читаемости)
    for i, model_name in enumerate(models_list):
        # Обрезаем длинные названия моделей
        display_name = model_name[:30] + "..." if len(model_name) > 30 else model_name
        # Используем индекс вместо полного имени в callback_data
        keyboard.append([InlineKeyboardButton(display_name, callback_data=f"model_{category_short_name}_{i}")])
    
    # Добавляем кнопки навигации
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    keyboard.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    
    return InlineKeyboardMarkup(keyboard)

# ==============================
# ОБРАБОТЧИКИ КОМАНД
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение с категориями"""
    user = update.effective_user
    
    # Подсчитываем общую статистику
    total_categories = len(CATEGORIES)
    total_models = sum(len(models) for models in CATEGORIES.values())
    
    # Краткое приветствие
    await update.message.reply_text(
        f"👋 *Привет, {user.first_name}!*\n\n"
        f"*Каталог техники*\n"
        f"▫️ Категорий: {total_categories}\n"
        f"▫️ Моделей: {total_models}\n\n"
        f"Выберите категорию:",
        reply_markup=create_main_keyboard(),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await help_command_callback(update, context)
        return
    
    if query.data == "back_to_main":
        await show_main_menu(update, context)
        return
    
    if query.data.startswith("cat_"):
        await show_category_models(update, context)
        return
    
    if query.data.startswith("model_"):
        await show_model_pdf(update, context)

# ==============================
# ФУНКЦИИ ОТОБРАЖЕНИЯ
# ==============================

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает главное меню с категориями"""
    query = update.callback_query
    
    total_categories = len(CATEGORIES)
    total_models = sum(len(models) for models in CATEGORIES.values())
    
    await query.edit_message_text(
        f"📁 *Каталог техники*\n\n"
        f"▫️ Категорий: {total_categories}\n"
        f"▫️ Моделей: {total_models}\n\n"
        f"Выберите категорию:",
        reply_markup=create_main_keyboard(),
        parse_mode='Markdown'
    )

async def show_category_models(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает модели выбранной категории"""
    query = update.callback_query
    
    # Получаем короткое имя категории
    category_short_name = query.data.replace("cat_", "")
    
    category_name = SHORT_TO_FULL_CATEGORY.get(category_short_name)
    if not category_name:
        await query.edit_message_text("Категория не найдена")
        return
    
    models = CATEGORIES[category_name]
    
    if not models:
        await query.edit_message_text(
            f"{category_name}\n\n"
            "В этой категории пока нет моделей.\n"
            "Модели будут добавлены позже.",
            reply_markup=create_category_keyboard(category_short_name),
            parse_mode='Markdown'
        )
        return
    
    await query.edit_message_text(
        f"{category_name}\n\n"
        f"*Доступно моделей: {len(models)}*\n"
        f"Выберите модель:",
        reply_markup=create_category_keyboard(category_short_name),
        parse_mode='Markdown'
    )

async def show_model_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает информацию о модели с кнопкой для открытия PDF"""
    query = update.callback_query
    
    # Получаем данные из callback
    parts = query.data.split("_")
    if len(parts) != 3:
        await query.edit_message_text("Ошибка данных")
        return
    
    category_short_name = parts[1]
    try:
        model_index = int(parts[2])
    except ValueError:
        await query.edit_message_text("Ошибка в данных модели")
        return
    
    category_name = SHORT_TO_FULL_CATEGORY.get(category_short_name)
    if not category_name or category_name not in CATEGORIES:
        await query.edit_message_text("Категория не найдена")
        return
    
    models = CATEGORIES[category_name]
    models_list = list(models.items())
    
    if model_index < 0 or model_index >= len(models_list):
        await query.edit_message_text("Модель не найдена")
        return
    
    model_name, pdf_url = models_list[model_index]
    
    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton("📄 ОТКРЫТЬ PDF", url=pdf_url)],
        [InlineKeyboardButton(f"◀️ Назад к {category_name.split()[0]}", callback_data=f"cat_{category_short_name}")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение
    await query.edit_message_text(
        text=f"{category_name}\n"
             f"*{model_name}*\n\n"
             f"Нажмите кнопку ниже для открытия PDF:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ==============================
# КОМАНДА ПОМОЩИ
# ==============================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
    ]
    
    await update.message.reply_text(
        "❓ *Помощь*\n\n"
        "*Навигация:*\n"
        "1. Выберите категорию\n"
        "2. Выберите модель\n"
        "3. Нажмите '📄 ОТКРЫТЬ PDF'\n\n"
        "*PDF презентации:*\n"
        "• Открываются в браузере\n"
        "• Доступны для скачивания\n\n"
        "*Проблемы?*\n"
        "• Проверьте интернет\n"
        "• Попробуйте другой браузер",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def help_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки помощи из callback"""
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
    ]
    
    await query.edit_message_text(
        text="❓ *Помощь*\n\n"
             "*Как пользоваться:*\n"
             "1. Выберите категорию\n"
             "2. Выберите модель\n"
             "3. Нажмите кнопку PDF\n\n"
             "Все просто! 👍",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ==============================
# СТАТИСТИКА
# ==============================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает статистику по каталогу"""
    total_categories = len(CATEGORIES)
    total_models = sum(len(models) for models in CATEGORIES.values())
    
    stats_text = "📊 *Статистика:*\n\n"
    
    for category_name, models in CATEGORIES.items():
        model_count = len(models)
        stats_text += f"{category_name}: {model_count}\n"
    
    stats_text += f"\n*Итого:* {total_models} моделей"
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# ==============================
# КОМАНДА ДЛЯ ДОБАВЛЕНИЯ НОВЫХ МОДЕЛЕЙ
# ==============================

async def add_model_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Инструкция по добавлению новых моделей"""
    
    help_text = (
        "📝 *Добавление моделей*\n\n"
        "*Формат:*\n"
        "```python\n"
        "'🤖 Роботы-пылесосы': {\n"
        "    'Новая модель': 'https://...',\n"
        "},\n"
        "```\n\n"
        "*Категории:*\n"
    )
    
    for category in CATEGORIES.keys():
        count = len(CATEGORIES[category])
        help_text += f"• {category} ({count})\n"
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ==============================
# КОМАНДА КАТАЛОГ (показать все категории)
# ==============================

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает все категории"""
    total_models = sum(len(models) for models in CATEGORIES.values())
    
    catalog_text = "📂 *Все категории:*\n\n"
    
    for category_name, models in CATEGORIES.items():
        model_count = len(models)
        if model_count > 0:
            catalog_text += f"{category_name} - {model_count} моделей\n"
        else:
            catalog_text += f"{category_name} - пусто\n"
    
    catalog_text += f"\n*Всего моделей:* {total_models}"
    
    await update.message.reply_text(catalog_text, parse_mode='Markdown')

# ==============================
# ЗАПУСК БОТА
# ==============================

def main() -> None:
    """Запуск бота"""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("addhelp", add_model_help))
    application.add_handler(CommandHandler("catalog", catalog_command))
    
    # Регистрируем обработчики callback'ов
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("=" * 40)
    print("🤖 Бот запущен")
    print("=" * 40)
    
    # Выводим информацию
    total_models = sum(len(models) for models in CATEGORIES.values())
    print(f"Категорий: {len(CATEGORIES)}")
    print(f"Моделей: {total_models}")
    
    print("\n📋 Команды:")
    print("/start - начать")
    print("/help - помощь")
    print("/stats - статистика")
    print("/catalog - все категории")
    print("/addhelp - как добавлять модели")
    print("=" * 40)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()