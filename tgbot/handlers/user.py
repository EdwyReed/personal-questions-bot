import logging
import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.keyboards.questions import unblock_author_markup, new_question_markup
from tgbot.misc.states import QuestionStates
from tgbot.misc.callback_data import AnswerCallbackData
from tgbot.config import load_config
from tgbot.services.questions import block_user
from tgbot.template import (
    START_BOT_NOT_CONFIGURED, START_ADMIN_GREETING, START_USER_BLOCKED,
    WELCOME_MESSAGE_1, WELCOME_MESSAGE_2, NEW_QUESTION_PROMPT, USER_UNBLOCKED
)

user_router = Router()
config = load_config()


@user_router.message(CommandStart())
async def user_start(
        message: Message, command: CommandObject, repo: RequestsRepo, state: FSMContext,
):
    """
    Handle the '/start' command and direct all messages to the admin.

    :param: message: The incoming message object from the user.
    :param: command: The command object representing the '/start' command with arguments.
    :param: repo: The RequestsRepo object for managing database requests.
    :param: state: The FSMContext object for managing conversation state.
    :return: None
    """
    # Get the admin ID from config
    admin_id = config.tg_bot.admin_id

    if not admin_id:
        logging.error("No admin ID configured. Please set the ADMIN environment variable.")
        await message.answer(START_BOT_NOT_CONFIGURED)
        return

    # Check if the user is the admin
    if message.from_user.id == admin_id:
        await message.answer(START_ADMIN_GREETING)
        return

    # Check if user is blocked by admin
    user_is_blocked = await repo.user_block.get_by_filter(
        user_id=admin_id, blocked_user_id=message.from_user.id
    )
    if user_is_blocked:
        await message.reply(START_USER_BLOCKED)
        return

    await message.answer(WELCOME_MESSAGE_1)


    await asyncio.sleep(1.5)

    await message.answer(WELCOME_MESSAGE_2)

    # Set the admin ID as the recipient for all messages
    await state.set_data({QuestionStates.USER_ID_PARAM: str(admin_id)})
    await state.set_state(QuestionStates.WAIT_FOR_QUESTION_STATE)


@user_router.callback_query(Text(startswith=AnswerCallbackData.block_author))
async def clb_block_author_handler(call: CallbackQuery, repo: RequestsRepo):
    """
    Handle the user's request to block the author of the question.

    :param: message: The incoming message object from the user.
    :param: repo: The RequestsRepo object for managing database requests.
    :return: None

    Notes:
        - This function blocks the author of the question.
    """
    logging.info("User %s sent block author request", call.from_user.id)

    # get message ID from callback data
    message_id = int(call.data.split("=")[1])
    user_block_id = await block_user(call.from_user.id, message_id, repo)
    markup = unblock_author_markup(user_block_id)
    await call.message.edit_text(text=call.message.text, reply_markup=markup)


@user_router.callback_query(Text(startswith=AnswerCallbackData.unblock_author))
async def clb_unblock_author_handler(call: CallbackQuery, repo: RequestsRepo):
    """
    Handle the user's request to block the author of the question.

    :param: message: The incoming message object from the user.
    :param: repo: The RequestsRepo object for managing database requests.
    :return: None

    Notes:
        - This function blocks the author of the question.
    """
    logging.info("User %s sent unblock author request", call.from_user.id)

    user_block_id = call.data.split("=")[1]
    await repo.user_block.delete(user_blocked_id=int(user_block_id))

    await call.message.edit_text(text=call.message.text, reply_markup=None)
    await call.answer(USER_UNBLOCKED, show_alert=True)


@user_router.callback_query(Text(AnswerCallbackData.new_question))
async def clb_new_question_handler(call: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    """
    Handle the user's request to send a new question.

    :param: call: The incoming callback query from the user.
    :param: state: The FSMContext object for managing conversation state.
    :return: None

    Notes:
        - This function sets the state to WAIT_FOR_QUESTION_STATE and prompts the user to enter a new question.
    """
    logging.info("User %s sent new question request", call.from_user.id)

    # Get the admin ID from config
    admin_id = config.tg_bot.admin_id

    if not admin_id:
        logging.error("No admin ID configured. Please set the ADMIN environment variable.")
        await call.answer(START_BOT_NOT_CONFIGURED, show_alert=True)
        return

    # Check if user is blocked by admin
    user_is_blocked = await repo.user_block.get_by_filter(
        user_id=admin_id, blocked_user_id=call.from_user.id
    )
    if user_is_blocked:
        await call.answer(START_USER_BLOCKED, show_alert=True)
        return

    await call.message.answer(NEW_QUESTION_PROMPT)

    # Set the admin ID as the recipient for all messages
    await state.set_data({QuestionStates.USER_ID_PARAM: str(admin_id)})
    await state.set_state(QuestionStates.WAIT_FOR_QUESTION_STATE)
    await call.answer()
