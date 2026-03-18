import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================
# ТОКЕН БОТА (вставьте свой)
# ==============================
BOT_TOKEN = "8527254808:AAFwxXa42esSXIfLE1snOdEUGExVB4Cuasc"

# ==============================
# КАТЕГОРИИ И МОДЕЛИ
# ==============================

# Структура категорий с соответствием папкам
CATEGORIES = {
    "🤖 Роботы-пылесосы": {
        "folder": "robots",
        "models": [
            "F9 Pro",
            "Серия F10",
            "F20",
            "F21",
            "F21 Plus",
            "D9 Max",
            "D9 Max Gen 2",
            "D9 Plus",
            "D10 Plus",
            "D10 Plus Gen 2",
            "D10s",
            "D10s Pro & D10s Plus",
            "Серия D20",
            "D30 Ultra",
            "L10s Pro",
            "L10s Plus & L10s Pro Gen 2",
            "L10 Ultra & L10 Prime",
            "L10s Ultra",
            "L10s Pro Ultra",
            "L20 Ultra Complete",
            "L30 Ultra",
            "L40",
            "L40 Ultra CE & L40s Ultra",
            "L40 Ultra AE",
            "L40s Pro Ultra",
            "X40 Ultra Complete",
            "Серия X50",
            "Matrix10 Ultra",
            "Aqua10 Ultra Roller Complete"
        ]
    },
    
    "🔋 Вертикальные пылесосы": {
        "folder": "vertical",
        "models": [
            "U10 & U20",
            "R10 & R10 Pro",
            "R10 Pro Aqua",
            "R10s Essential",
            "R10s & R10s Pro",
            "R10s Aqua",
            "R20 Essential",
            "R20",
            "R20 Aqua",
            "Z10 Station",
            "Z20 Essential",
            "Z20 & Z30",
            "Z20 AC & Z30 AC",
            "Z40 Station",
            "E10"
        ]
    },

    "💦 Моющие пылесосы": {
        "folder": "wash",
        "models": [
            "G10 & G10 Combo",
            "G10 Pro",
            "H11 Core",
            "H12 & H12 Core",
            "H12S",
            "H12S AE",
            "H12 Pro & H12 Dual",
            "H12 FlexReach",
            "H12 Pro FlexReach",
            "H12 Dual FlexReach",
            "H13 Pro",
            "H14 Dual",
            "H15 Pro Heat"
        ]
    },

    "🌿 Роботы-газонокосилки": {
        "folder": "mowers",
        "models": [
            "A1 Pro"
        ]
    },

    "✨ Техника для ухода": {
        "folder": "care",
        "models": [
            "Mini",
            "Gleam",
            "Glory",
            "Glory Mix",
            "Glory Master",
            "Pocket",
            "Pocket Ultra",
            "Gusto",
            "Miracle",
            "Miracle Pro",
            "Pilot",
            "Dazzle",
            "AirStyle",
            "AirStyle Pro",
            "AirStyle Pro Hi",
            "Aero Straight",
            "Hair Removal",
            "S7"
        ]
    },
    
    "🌡️ Климат": {
        "folder": "climate",
        "models": [
            "PM10 & PM20",
            "PM30",
            "H40 & H40 Essential",
            "AP10",
            "HT30 Ultra"
        ]
    },
    
    "🍗 Аэрогрили": {
        "folder": "airfry",
        "models": [
            "AF30"
        ]
    },

    "🏠 Для дома": {
        "folder": "home",
        "models": [
            "S10",
            "DF10 & DF10 Pro"
        ]
    },
}

# Создаем список категорий для удобства
CATEGORY_ITEMS = list(CATEGORIES.items())

# Путь к папке с PDF-файлами
PDF_BASE_PATH = r"C:\dreame_learn\pdfs"

# ==============================
# ФУНКЦИИ ДЛЯ СОЗДАНИЯ КЛАВИАТУР
# ==============================

def create_main_keyboard():
    """Создает главную клавиатуру с категориями"""
    keyboard = []
    
    # Сортируем чтобы роботы-пылесосы были первыми
    categories = list(CATEGORIES.keys())
    if "🤖 Роботы-пылесосы" in categories:
        categories.remove("🤖 Роботы-пылесосы")
        categories.insert(0, "🤖 Роботы-пылесосы")
    
    # Создаем кнопки для каждой категории
    for i, category_name in enumerate(categories):
        model_count = len(CATEGORIES[category_name]["models"])
        display_text = f"{category_name} [{model_count}]"
        # Используем короткое имя папки для callback
        folder_name = CATEGORIES[category_name]["folder"]
        keyboard.append([InlineKeyboardButton(display_text, callback_data=f"cat_{folder_name}")])
    
    # Добавляем кнопку помощи
    keyboard.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    
    return InlineKeyboardMarkup(keyboard)

def create_category_keyboard(folder_name):
    """Создает клавиатуру с моделями выбранной категории"""
    # Находим категорию по имени папки
    category_name = None
    category_index = None
    models = None
    
    for i, (name, data) in enumerate(CATEGORY_ITEMS):
        if data["folder"] == folder_name:
            category_name = name
            category_index = i
            models = data["models"]
            break
    
    if not models:
        return create_main_keyboard()
    
    keyboard = []
    
    # Создаем кнопки для каждой модели
    for i, model_name in enumerate(models):
        # Обрезаем длинные названия
        display_name = model_name[:35] + "..." if len(model_name) > 35 else model_name
        # Используем folder_name и индекс модели
        keyboard.append([InlineKeyboardButton(display_name, callback_data=f"model_{folder_name}_{i}")])
    
    # Добавляем кнопки навигации
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")])
    keyboard.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    
    return InlineKeyboardMarkup(keyboard)

# ==============================
# ОБРАБОТЧИКИ КОМАНД
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение с категориями"""
    user = update.effective_user
    
    # Подсчитываем статистику
    total_categories = len(CATEGORIES)
    total_models = sum(len(cat["models"]) for cat in CATEGORIES.values())
    
    welcome_text = (
        f"👋 *Привет, {user.first_name}!*\n\n"
        f"📁 *Каталог техники Dreame*\n"
        f"▫️ Категорий: {total_categories}\n"
        f"▫️ Моделей: {total_models}\n\n"
        f"Выберите категорию:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=create_main_keyboard(),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Получен callback: {query.data}")
    
    if query.data == "help":
        await show_help(query)
    
    elif query.data == "back_to_main":
        await show_main_menu(query)
    
    elif query.data.startswith("cat_"):
        await show_category(query)
    
    elif query.data.startswith("model_"):
        await send_pdf_file(query)
    
    else:
        logger.warning(f"Неизвестный callback: {query.data}")

async def show_main_menu(query):
    """Показывает главное меню"""
    total_categories = len(CATEGORIES)
    total_models = sum(len(cat["models"]) for cat in CATEGORIES.values())
    
    await query.edit_message_text(
        f"📁 *Каталог техники*\n\n"
        f"▫️ Категорий: {total_categories}\n"
        f"▫️ Моделей: {total_models}\n\n"
        f"Выберите категорию:",
        reply_markup=create_main_keyboard(),
        parse_mode='Markdown'
    )

async def show_category(query):
    """Показывает модели выбранной категории"""
    # Получаем имя папки из callback (cat_robots, cat_vertical и т.д.)
    folder_name = query.data.replace("cat_", "")
    
    # Находим категорию по имени папки
    category_name = None
    for name, data in CATEGORY_ITEMS:
        if data["folder"] == folder_name:
            category_name = name
            models = data["models"]
            break
    
    if not category_name:
        await query.edit_message_text("Категория не найдена")
        return
    
    await query.edit_message_text(
        f"{category_name}\n\n"
        f"*Доступно моделей: {len(models)}*\n"
        f"Выберите модель:",
        reply_markup=create_category_keyboard(folder_name),
        parse_mode='Markdown'
    )

async def send_pdf_file(query):
    """Отправляет PDF-файл пользователю"""
    # Парсим данные из callback (model_robots_0, model_vertical_5 и т.д.)
    parts = query.data.split("_")
    if len(parts) != 3:
        await query.message.reply_text("Ошибка в данных модели")
        return
    
    folder_name = parts[1]
    try:
        model_index = int(parts[2])
    except ValueError:
        await query.message.reply_text("Ошибка в индексе модели")
        return
    
    # Находим категорию и модель по folder_name
    category_name = None
    category_data = None
    for name, data in CATEGORY_ITEMS:
        if data["folder"] == folder_name:
            category_name = name
            category_data = data
            break
    
    if not category_data:
        await query.message.reply_text("Категория не найдена")
        return
    
    models = category_data["models"]
    if model_index < 0 or model_index >= len(models):
        await query.message.reply_text("Модель не найдена")
        return
    
    model_name = models[model_index]
    
    # Формируем путь к файлу
    file_name = f"{model_name}.pdf"
    # Убираем недопустимые символы из имени файла
    safe_file_name = "".join(c for c in file_name if c not in r'<>:"/\|?*').strip()
    file_path = os.path.join(PDF_BASE_PATH, folder_name, safe_file_name)
    
    try:
        # Проверяем существует ли файл
        if os.path.exists(file_path):
            # Открываем и отправляем файл
            with open(file_path, 'rb') as pdf_file:
                await query.message.reply_document(
                    document=pdf_file,
                    filename=f"{model_name}.pdf",
                    caption=f"📄 *{model_name}*\n{category_name}",
                    parse_mode='Markdown'
                )
            
            # Отправляем подтверждение с кнопкой назад
            keyboard = [[
                InlineKeyboardButton("◀️ Назад к моделям", callback_data=f"cat_{folder_name}")
            ]]
            await query.message.reply_text(
                "✅ PDF успешно отправлен!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            # Если файл не найден, показываем доступные файлы для отладки
            await handle_file_not_found(query, file_path, folder_name, model_name, folder_name)
            
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await query.message.reply_text(f"❌ Ошибка при отправке файла: {str(e)}")

async def handle_file_not_found(query, file_path, folder_name, model_name, folder_name_for_back):
    """Обрабатывает ситуацию, когда файл не найден"""
    folder_path = os.path.join(PDF_BASE_PATH, folder_name)
    
    error_text = f"❌ Файл для модели *{model_name}* не найден.\n\n"
    error_text += f"🔍 Искали: `{file_path}`\n\n"
    
    # Проверяем существует ли папка
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        if files:
            error_text += f"📁 В папке `{folder_name}` найдены файлы:\n"
            # Показываем первые 10 файлов
            for f in files[:10]:
                error_text += f"   • {f}\n"
            if len(files) > 10:
                error_text += f"   ... и ещё {len(files) - 10} файлов\n"
        else:
            error_text += f"📁 Папка `{folder_name}` пуста\n"
    else:
        error_text += f"📁 Папка `{folder_name}` не существует!\n"
        error_text += f"   Создайте папку: {folder_path}\n"
    
    keyboard = [[
        InlineKeyboardButton("◀️ Назад к моделям", callback_data=f"cat_{folder_name_for_back}")
    ]]
    
    await query.message.reply_text(
        error_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def show_help(query):
    """Показывает справку"""
    help_text = (
        "❓ *Помощь*\n\n"
        "*Как пользоваться:*\n"
        "1. Выберите категорию техники\n"
        "2. Выберите нужную модель\n"
        "3. Бот отправит PDF-файл с инструкцией\n\n"
        "*Команды:*\n"
        "• /start - начать работу\n"
        "• /help - эта справка\n"
        "• /stats - статистика каталога\n\n"
        "*Поддержка:*\n"
        "Если файл не отправляется, проверьте:\n"
        "• Название модели точно совпадает с файлом\n"
        "• Файл есть в нужной папке на сервере"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")]]
    await query.edit_message_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает статистику по каталогу"""
    total_categories = len(CATEGORIES)
    total_models = sum(len(cat["models"]) for cat in CATEGORIES.values())
    
    stats_text = "📊 *Статистика каталога:*\n\n"
    
    for category_name, category_data in CATEGORIES.items():
        model_count = len(category_data["models"])
        stats_text += f"{category_name}: {model_count} моделей\n"
    
    stats_text += f"\n*Всего:* {total_models} моделей в {total_categories} категориях"
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    keyboard = [[InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")]]
    
    await update.message.reply_text(
        "❓ *Помощь*\n\n"
        "Бот для получения PDF-инструкций по технике Dreame.\n\n"
        "Используйте /start для начала работы.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ==============================
# ЗАПУСК БОТА
# ==============================

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Регистрируем обработчик callback-запросов (кнопки)
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Проверяем существование базовой папки с PDF
    print("\n" + "="*50)
    print("🔍 Проверка папок с PDF...")
    print("="*50)
    
    if os.path.exists(PDF_BASE_PATH):
        print(f"✅ Папка с PDF найдена: {PDF_BASE_PATH}")
        
        # Проверяем подпапки
        for category_name, category_data in CATEGORIES.items():
            folder_path = os.path.join(PDF_BASE_PATH, category_data["folder"])
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                pdf_files = [f for f in files if f.lower().endswith('.pdf')]
                print(f"   📁 {category_data['folder']}: {len(pdf_files)} PDF файлов")
                
                # Проверяем соответствие моделей
                models = category_data["models"]
                found_models = []
                missing_models = []
                
                for model in models:
                    expected_file = f"{model}.pdf"
                    if expected_file in files or expected_file.lower() in [f.lower() for f in files]:
                        found_models.append(model)
                    else:
                        missing_models.append(model)
                
                if missing_models:
                    print(f"      ⚠️ Отсутствуют {len(missing_models)} файлов")
            else:
                print(f"   ⚠️ Папка {folder_path} не существует!")
    else:
        print(f"❌ Папка с PDF не найдена: {PDF_BASE_PATH}")
        print("Создайте папку и положите в неё PDF-файлы")
    
    # Запускаем бота
    print("\n" + "="*50)
    print("🤖 Бот для каталога Dreame запущен!")
    print("="*50)
    print(f"📁 Категорий: {len(CATEGORIES)}")
    print(f"📄 Всего моделей: {sum(len(cat['models']) for cat in CATEGORIES.values())}")
    print(f"📂 Путь к PDF: {PDF_BASE_PATH}")
    print("="*50 + "\n")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
