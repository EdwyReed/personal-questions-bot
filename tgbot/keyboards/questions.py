from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.callback_data import AnswerCallbackData
from tgbot.template import GENERATE_IMAGE_BUTTON, BLOCK_AUTHOR_BUTTON, UNBLOCK_AUTHOR_BUTTON, NEW_QUESTION_BUTTON


def question_answer_markup(question_id: int):
    """
    The function returns the keyboard with the buttons "Generate image" and "Block author".

    :param question_id: ID of the message to be answered.
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=GENERATE_IMAGE_BUTTON,
                    callback_data=AnswerCallbackData.generate_image_callback(question_id),
                )
            ],
            [
                InlineKeyboardButton(
                    text=BLOCK_AUTHOR_BUTTON,
                    callback_data=AnswerCallbackData.block_author_callback(question_id),
                )
            ],
        ]
    )
    return markup


def unblock_author_markup(author_id: int):
    """
    The function returns the keyboard with the buttons "Generate image" and "Block author".

    :param author_id: ID of the user who is the author of the question.
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=UNBLOCK_AUTHOR_BUTTON,
                    callback_data=AnswerCallbackData.unblock_author_callback(author_id),
                )
            ],
        ]
    )
    return markup


def new_question_markup():
    """
    The function returns the keyboard with the "Send new question" button.

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=NEW_QUESTION_BUTTON,
                    callback_data=AnswerCallbackData.new_question_callback(),
                )
            ],
        ]
    )
    return markup
