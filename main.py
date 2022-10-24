import os
from random import randint
from pprint import pprint
from RoundTable import LANGUAGE_BTN, LEADERBOARD_KEYBOARD, PLAY_KEYBOARD, WIN_BTN
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from config import BOT_TOKEN
from database import *
from init import LANGUAGE_CODE, LANG_MSG, ME_MSG
from akinator import Akinator



def start(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type == "private":
       user_id = update.effective_user.id
       first_name = update.effective_user.first_name
       last_name = update.effective_user.last_name
       user_name = update.effective_user.username
       addUser(user_id, first_name, last_name, user_name)
       update.message.reply_text(START_MSG.format(first_name), 
                                 parse_mode=ParseMode.MARKDOWN, 
                                 )

    else:
        update.message.reply_text(
        "Hello I'm investigator usuke Aien, Gald to meet you"
        )


def find(update: Update, context: CallbackContext) -> None:
    total_users = totalUsers()
    update.message.reply_text(f"Users : {total_users}")

def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "If you where don't know the char name that you saw but you know what he looks like then, This bot will ask you some questions and give you that char detail. As a detective This is my work. If you found any bug in the bot then contact @Dainkawa my developer.",
         parse_mode=ParseMode.MARKDOWN,
         reply_markup=InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton(
                     text="Start Investigation", callback_data="start_Game"
                     ),
                     InlineKeyboardButton(
                     text="Commands Info", callback_data="Info_IG"
                     ),        
                 ]
             ]
         )
    )

def info(update: Update, context: CallbackContext): 
    update.message.reply_text(
        "*IMPORTANT Message* Without doing /start command bot will not ask you questions. /play - to start the investigation. /language - select your own language. /leaderboard - To see who's on the top. *NOTE* leaderboard shows the global stats not only group stats. Click on start investigation So i can ask you questions usely a shortcut.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                    text="Start investigation", callback_data="start_Game"
                    ),
                ] 
            ]
        )
     )


def play_cmd_handler(update: Update, context: CallbackContext) -> None:
    Fu = Akinator()
    user_id = update.effective_user.id
    msg = update.message.reply_text("Loading...")
    updateTotalGuess(user_id, total_guess=1)
    q = Fu.start_game(language=getLanguage(user_id))
    context.user_data[f"Fu_{user_id}"] = Fu
    context.user_data[f"q_{user_id}"] = q
    context.user_data[f"ques_{user_id}"] = 1
    msg.edit_text(
        q,
        reply_markup=PLAY_KEYBOARD
        )


def start_Game(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        if query.data == "start_Game":
            Fu = Akinator()
            user_id = update.effective_user.id
            updateTotalGuess(user_id, total_guess=1)
            q = Fu.start_game(language=getLanguage(user_id))
            context.user_data[f"Fu_{user_id}"] = Fu
            context.user_data[f"q_{user_id}"] = q
            context.user_data[f"ques_{user_id}"] = 1
            query.message.edit_text(
                    q,
                    reply_markup=PLAY_KEYBOARD

            )  
    except BadRequest as excp:
        if excp.message == "Message can't be edited":
            pass



def play_callback_handler(update: Update, context:CallbackContext) -> None:
    user_id = update.effective_user.id
    user = cq['from_user']['id']
    Fu = context.user_data[f"Fu_{user_id}"]
    q = context.user_data[f"q_{user_id}"]
    updateTotalQuestions(user_id, 1)
    query = update.callback_query
    a = query.data.split('_')[-1]
    if a == '5':
        updateTotalQuestions(user_id, -1)
        try:
            q = Fu.back()
        except akinator.exceptions.CantGoBackAnyFurther:
            query.answer(text="This is the first question. You can't go back any further!", show_alert=True)
            return
    else:
        q = Fu.answer(a)
    query.answer()
    if Fu.progression < 80:
        query.message.edit_text(
        q,
        reply_markup=PLAY_KEYBOARD
        )
        context.user_data[f"Fu_{user_id}"] = Fu
        context.user_data[f"q_{user_id}"] = q
    else:
        Fu.win()
        Fu = Fu.first_guess
        query.message.edit_text(f"It's {Fu['name']} ({Fu['description']})! Was I correct?",
        reply_markup=WIN_BTN
        )

def win(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query
    ans = query.data.split('_')[-1]
    if ans =='y':
        query.message.edit_text("Case solved, Now give me my money.")
        reply_markup=None
    
        updateCorrectGuess(user_id=user_id, correct_guess=1)
    else:
        query.message.edit_text("I think we missed something, lets investigate again",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                    text="Let's see what we've missed", callback_data="start_Game"
                    ),
                ] 
            ]
        )
     )
        updateWrongGuess(user_id=user_id, wrong_guess=1)


def me(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    profile_pic = update.effective_user.get_profile_photos(limit=1).photos
    if len(profile_pic) == 0:
        profile_pic = "https://telegra.ph/file/a65ee7219e14f0d0225a9.png"
    else:
        profile_pic = profile_pic[0][1]
    
    user = getUser(user_id)
    update.message.reply_photo(photo= profile_pic, 
                               caption=ME_MSG.format(user["user_name"],                                                    
                                                     user["user_id"],
                                                     LANG_CODE[user["Fu_lang"]],
                                                     getTotalGuess(user_id),
                                                     getCorrectGuess(user_id),
                                                     getWrongGuess(user_id),
                                                     getUnfinishedGuess(user_id),
                                                     getTotalQuestions(user_id),
                                                     ),
                               parse_mode=ParseMode.HTML)



def set_lang(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    lang_code = query.data.split('_')[-1]
    user_id = update.effective_user.id
    updateLanguage(user_id, lang_code)
    query.edit_message_text(f"Language Successfully changed to {LANG_CODE[lang_code]} !")


def lang(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    update.message.reply_text(LANG_MSG.format(LANG_CODE[getLanguage(user_id)]),
                                parse_mode=ParseMode.HTML,
                                reply_markup=LANG_BTN)


def del_data(context:CallbackContext, user_id: int):
    del context.user_data[f"Fu_{user_id}"]
    del context.user_data[f"q_{user_id}"]


def lead(update: Update, _:CallbackContext) -> None:
    update.message.reply_text(
        text="Check Leaderboard on specific categories in Tetris.",
        reply_markup=LEADERBOARD_KEYBOARD
    )


def get_lead_total(lead_list: list, lead_category: str) -> str:
    lead = f'Top 10 {lead_category} are :\n'
    for i in lead_list:
        lead = lead+f"{i[0]} : {i[1]}\n"
    return lead


def cb_handler(update: Update, context:CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split('_')[-1]
    #print(data)
    if data == 'cguess':
        text = get_lead_total(getLead("correct_guess"), 'correct guesses')
        query.edit_message_text(
            text= text,
            reply_markup=LEADERBOARD_KEYBOARD
        )
    elif data == 'tguess':
        text = get_lead_total(getLead("total_guess"), 'total guesses')
        query.edit_message_text(
            text= text,
            reply_markup=LEADERBOARD_KEYBOARD
        )
    elif data == 'wguess':
        text = get_lead_total(getLead("wrong_guess"), 'wrong guesses')
        query.edit_message_text(
            text= text,
            reply_markup=LEADERBOARD_KEYBOARD
        )
    elif data == 'tquestions':
        text = get_lead_total(getLead("total_questions"), 'total questions')
        query.edit_message_text(
            text= text,
            reply_markup=LEADERBOARD_KEYBOARD
        )



def main():
    updater = Updater(token=BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start, run_async=True))
    dp.add_handler(CommandHandler('info', info, run_async=True))
    dp.add_handler(CommandHandler('find', find, run_async=True))
    dp.add_handler(CommandHandler('me', me, run_async=True))
    dp.add_handler(CommandHandler('play', play_cmd_handler, run_async=True))
    dp.add_handler(CommandHandler('language', lang, run_async=True))
    dp.add_handler(CommandHandler('help', help, run_async=True))
    dp.add_handler(CommandHandler('leaderboard', lead, run_async=True))

    dp.add_handler(CallbackQueryHandler(set_lang, pattern=r"Fu_set_lang_", run_async=True))
    dp.add_handler(CallbackQueryHandler(start_Game, pattern=r"start_Game", run_async=True))
    dp.add_handler(CallbackQueryHandler(play_callback_handler, pattern=r"Fu_play_", run_async=True))
    dp.add_handler(CallbackQueryHandler(win, pattern=r"Fu_win_", run_async=True))
    dp.add_handler(CallbackQueryHandler(cb_handler, pattern=r"Fu_lead_", run_async=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
