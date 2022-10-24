from init import LANG_CODE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


LANG_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(LANG_CODE['en'], callback_data='Fu_set_lang_en'),
            InlineKeyboardButton(LANG_CODE['ar'], callback_data='Fu_set_lang_ar'),
            InlineKeyboardButton(LANG_CODE['cn'], callback_data='Fu_set_lang_cn'),
            InlineKeyboardButton(LANG_CODE['de'], callback_data='Fu_set_lang_de')
         ],
         [
            InlineKeyboardButton(LANG_CODE['es'], callback_data='Fu_set_lang_es'),
            InlineKeyboardButton(LANG_CODE['fr'], callback_data='Fu_set_lang_fr'),
            InlineKeyboardButton(LANG_CODE['il'], callback_data='Fu_set_lang_il'),
            InlineKeyboardButton(LANG_CODE['it'], callback_data='Fu_set_lang_it')
         ],
         [
            InlineKeyboardButton(LANG_CODE['jp'], callback_data='Fu_set_lang_jp'),
            InlineKeyboardButton(LANG_CODE['kr'], callback_data='Fu_set_lang_kr'),
            InlineKeyboardButton(LANG_CODE['nl'], callback_data='Fu_set_lang_nl'),
            InlineKeyboardButton(LANG_CODE['pl'], callback_data='Fu_set_lang_pl')
         ],
         [
            InlineKeyboardButton(LANG_CODE['pt'], callback_data='Fu_set_lang_p'),
            InlineKeyboardButton(LANG_CODE['ru'], callback_data='Fu_set_lang_ru'),
            InlineKeyboardButton(LANG_CODE['tr'], callback_data='Fu_set_lang_tr'),
            InlineKeyboardButton(LANG_CODE['id'], callback_data='Fu_set_lang_id')
         ],

    ]
)


PLAY_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Yes", callback_data='Fu_play_0'),
            InlineKeyboardButton("No", callback_data='Fu_play_1'),
            InlineKeyboardButton("Probably", callback_data='Fu_play_3')
        ],
        [
            InlineKeyboardButton("I don't know", callback_data='Fu_play_2'),
            InlineKeyboardButton("Probably Not", callback_data='Fu_play_4')
        ],
        [   InlineKeyboardButton("Back", callback_data= 'Fu_play_5')
        ]
    ]
)

AKI_WIN_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Yes", callback_data='Fu_win_y'),
            InlineKeyboardButton("No", callback_data='Fu_win_n'),
        ]
    ]
)


LEADERBOARD_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Total Guesses", callback_data='Fu_lead_tguess'),
            InlineKeyboardButton("Correct Guesses", callback_data='Fu_lead_cguess'),
        ],
        [
            InlineKeyboardButton("Wrong Guesses", callback_data='Fu_lead_wguess'),
            InlineKeyboardButton("Total Questions", callback_data='Fu_lead_tquestions'),
        ]
    ]
)
