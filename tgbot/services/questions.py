from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.keyboards.questions import question_answer_markup, new_question_markup
from tgbot.template import QUESTION_TEXT_PATTERN, QUESTION_PREFIX_REPLY, QUESTION_PREFIX_ANONYMOUS, QUESTION_SENT, QUESTION_DELIVERY_ERROR


async def send_question(
        message: types.Message,
        repo: RequestsRepo,
        chat_id: int,
        reply_to_message_id: int = None,
):
    original_text = message.text  # cache original text, we use it later to save in db
    message.__config__.allow_mutation = True

    if reply_to_message_id is not None:
        prefix = QUESTION_PREFIX_REPLY
    else:
        prefix = QUESTION_PREFIX_ANONYMOUS

    if message.text:
        message.text = QUESTION_TEXT_PATTERN.format(prefix=prefix, question=message.text)
    elif message.caption:
        message.caption = QUESTION_TEXT_PATTERN.format(prefix=prefix, question=message.caption)

    try:
        markup = question_answer_markup(message.message_id)
        result = await message.send_copy(chat_id, reply_to_message_id=reply_to_message_id, reply_markup=markup)
        await repo.questions.create(
            question_id=message.message_id,
            question_from=message.from_user.id,
            from_message_id=message.message_id,
            question_to=int(chat_id),
            to_message_id=result.message_id,
            text=original_text,
        )

        # Import config here to avoid circular imports
        from tgbot.config import load_config
        config = load_config()

        # Only include the new question markup for non-admin users
        if message.from_user.id != config.tg_bot.admin_id:
            await message.answer(QUESTION_SENT, reply_markup=new_question_markup())
        else:
            await message.answer(QUESTION_SENT)
    except TelegramBadRequest:
        await message.answer(QUESTION_DELIVERY_ERROR)


async def block_user(
        user_id: int,
        question_id: int,
        repo: RequestsRepo,
) -> int:
    """
    Block user by message id

    :param user_id: ID of the user that wants to block the author
    :param question_id: ID of the message that user sent
    :param repo: RequestsRepo instance
    :return: ID of the user_block record
    """
    question = await repo.questions.get_by_filter(question_id=question_id)
    user_block = await repo.user_block.create(user_id=user_id, blocked_user_id=question.question_from)
    return user_block.user_blocked_id
