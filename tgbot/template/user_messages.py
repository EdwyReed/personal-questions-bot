"""
User-facing messages for the bot.

This file contains all the text messages that are sent to users.
"""

# Start command messages
START_BOT_NOT_CONFIGURED = "Бот не настроен должным образом. Пожалуйста, свяжитесь с разработчиком: @edwy_reed"
START_ADMIN_GREETING = "Привет. Ты админ Капкана. Сюда летят шёпоты, стоны и идеи. Иногда — боль. Иногда — просто пустота."
START_USER_BLOCKED = "Ты не можешь больше писать. Капкан закрылся."

# Welcome messages
WELCOME_MESSAGE_1 = """<b>Это не просто эхо.</b>
Это почтовый ящик для твоих мыслей, фантазий, боли, радости и случайных признаний.

Хочешь предложить идею для текста? Пиши.
Хочешь просто поговорить? Кричи. Шепчи. Плачь.
Капкан слушает. Иногда отвечает.

Никто не узнает, что это был(а) ты."""

WELCOME_MESSAGE_2 = """<b>Шёлковое эхо слушает.</b>
Хочешь — идею для сцены.
Хочешь — голос в пустоту.

Заржавевшее железо капкана всё впитает.❤️‍🩹"""

# New question messages
NEW_QUESTION_PROMPT = """<b>Шёлковое эхо ждёт.</b>
Пиши, если не в кого больше кричать."""

# Question sent confirmation
QUESTION_SENT = "Капкан принял."
QUESTION_DELIVERY_ERROR = "Сообщение не дошло. Возможно, получатель исчез."

# User block/unblock messages
USER_UNBLOCKED = "Ты снова можешь писать в капкан."

# Error messages
INVALID_MESSAGE_FORMAT = "Формат сообщения не распознан. Попробуй ещё."


"""
Button labels for the bot.

This file contains all the text labels for buttons used in the bot's keyboards.
"""

# Question answer buttons
GENERATE_IMAGE_BUTTON = "📸 Сгенерировать изображение"
BLOCK_AUTHOR_BUTTON = "⛔️ Заблокировать автора"
UNBLOCK_AUTHOR_BUTTON = "👍 Разблокировать автора"
NEW_QUESTION_BUTTON = "✉️ Отправить новое сообщение"