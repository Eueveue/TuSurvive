import random
import copy
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, Updater, MessageHandler, filters
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

field = [[0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,1,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0]]
GameOver = False
what = "start"#input("\n")
ignoreL = False
ignoreR = False
ignoreU = False
ignoreD = False
paralyzed = False
lightnings = 0
died_reason = None
hurricane = False
row = 0
column = 0
allow_move = None
token = "5434057735:AAHppmU3OdFMrvDkbK_tIIAup5JQgoCrvmY"
amount_players = 0
character = None
game_started = False
query = None
chat_id = None
message_id = None
bot = Bot(token=token)
dp = Dispatcher(bot)
async def pick_char(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    colorboard = [
        [
            InlineKeyboardButton("🟥", callback_data="red"),
            InlineKeyboardButton("🟨", callback_data="yellow"),
        ],
        [InlineKeyboardButton("🟩", callback_data="green"),
         InlineKeyboardButton("🟦", callback_data="blue")
        ],
    ]
    reply_markup2 = InlineKeyboardMarkup(colorboard)
    if amount_players != 0 and character == None:
        await update.message.reply_text("Choose a character now", reply_markup=reply_markup2)
    elif character != None:
        await update.message.reply_text("You've already selected...\nDo you want to /end this game and start a new one?")
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    playerboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2\n𝒮𝑜𝑜𝓃", callback_data="2"),
        ],
        [InlineKeyboardButton("3\n𝒮𝑜𝑜𝓃", callback_data="3"),
         InlineKeyboardButton("4\n𝒮𝑜𝑜𝓃", callback_data="4")
        ],
    ]
    global message_id
    reply_markup1 = InlineKeyboardMarkup(playerboard)
    if game_started == False:
        await update.message.reply_text("How many players this time?", reply_markup=reply_markup1)
        message_id = update.effective_message.id
    else:
        await update.message.reply_text("You've already started...\nDo you want to /end this game and start a new one?")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global amount_players, colorboard, character, game_started, query
    query = update.callback_query
    await query.answer()
    if int(query.data) == 1 :
        await query.edit_message_text(text=f"Ok, solo mode then")
        amount_players = 1
        game_started = True
        await pick_char(update, context)
    else:
        await query.edit_message_text(text=f"Ok, {query.data} players then")
        amount_players = int(query.data)
        game_started = True
async def col_char(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global character, query, row, column
    query = update.callback_query
    await query.answer()
    if query.data == "red":
        character = "🟥"
    if query.data == "yellow":
        character = "🟨"
    if query.data == "green":
        character = "🟩"
    if query.data == "blue":
        character = "🟦"
    await query.edit_message_text(text=f"Are you ready {character} ?\nGreat!")
    frame_field = ""
    for line in field:
        for cell in line:
            frame_field += str(cell)
        frame_field += '\n'
        frame_field = frame_field.replace('0', '⬛').replace('1', character)
    row = 2
    column = 2
    await query.edit_message_text(text=f"{frame_field}")
    await pre_move_skript(update, context)


async def dispetcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global query
    query = update.callback_query
    if query.data in ["1","2","3","4"]:
        await button(update, context)
    elif query.data in ["red","yellow","green","blue"]:
        await col_char(update, context)

async def start(update, context):
     await update.message.reply_text("Hello! I see you would like 𝕋𝕦𝕊𝕦𝕣𝕧𝕚𝕧𝕖...\nDo you need any /help ?  ")
     global chat_id, query
     chat_id = update.effective_chat.id

async def help(update, context):
     await update.message.reply_text("/start - starts the bot\n/help - shows general commands\n/game_help - shows all game commands\n/rules - shows rules of the game and how it works\n/st - special thanks, people that helped with the project")


async def special_thanks(update, context):
    await update.message.reply_text("@Helluin4ik\n@TheFazeFox\n@Trifase\n@BiboJoshi\n@clot27\n@Poolitzer")

async def game_help(update, context):
     global character
     await update.message.reply_text('/start_game - select players amount \n/pick_char - select a color of your character, then game starts\n /u, /r, /d, /l - moves up, right, down, left \n /end - quit curent game ')


async def rules(update, context):
     await update.message.reply_text("You and your friends are on a black field. But it is full of dangers! Your task is to survive a meteor shower\u2604 , lightning storm\U0001F329  and make sure that you aren't stuck between meteor fragments\U0001F5FB ! Last survived player is the winner\U0001F3C6!\n\n\u2B1B - simple cell, everyone can step on it\n🪨 - meteor fragment, no one can step on it, if it falls on you, ⠀⠀⠀you lose\n\u26A1 - lightning is too fast, you can't step on it, but it can strike ⠀⠀⠀and you will have 80% chance of lose and 20% of ⠀⠀⠀paralyzation\n\U0001F32A - hurricane, might kill or might save, 50% chance of flew of ⠀⠀⠀the field and 50% chance to get in a random position\n\U0001F40A - 𝒮𝑜𝑜𝓃\n\U0001F381 - 𝒮𝑜𝑜𝓃\n\nNotes:\n- You can't step on other players\n- If you are surrounded by fragments or other players you lose\n   \u2B1B🪨🪨     \u2B1B🪨\u2B1B     \u2B1B\u2B1B\u2B1B\n   🪨\U0001F635🪨     🪨\U0001F635\U0001F60F     🪨\U0001F603\U0001F60F\n   \u2B1B🪨\u2B1B     \u2B1B\u263A\u2B1B     \u2B1B🪨🪨\n- You can't go of the field by yourself")#("You and your friends are on a black field. But it is full of dangers! Your task is to survive a meteor shower\u2604 , lightning storm\U0001F329  and make sure that you aren't stuck between meteor fragments\U0001F5FB ! Last survived player is the winner\U0001F3C6!\n\n\u2B1B - simple cell, everyone can step on it\n🪨 - meteor fragment, no one can step on it, if it falls on you, ⠀⠀⠀you lose\n\u26A1 - lightning is too fast, you can't step on it, but it can strike ⠀⠀⠀and you will have 80% chance of lose and 20% of ⠀⠀⠀paralyzation\n\U0001F32A - hurricane, might kill or might save, 50% chance of flew of ⠀⠀⠀the field and 50% chance to get in a random position\n\U0001F40A - you better avoid it! Run if you don't want to become it's ⠀⠀⠀lunch!\n\U0001F381 - /mysterious_box ... something happens when you open ⠀⠀⠀it...\n\nNotes:\n- You can't step on other players\n- If you are surrounded by fragments or other players you lose\n   \u2B1B🪨🪨     \u2B1B🪨\u2B1B     \u2B1B\u2B1B\u2B1B\n   🪨\U0001F635🪨     🪨\U0001F635\U0001F60F     🪨\U0001F603\U0001F60F\n   \u2B1B🪨\u2B1B     \u2B1B\u263A\u2B1B     \u2B1B🪨🪨\n- You can't go of the field by yourself")


async def end(update, context):
    await update.message.reply_text("Quited...")
    global amount_players, character, game_started, GameOver, chat_id, message_id, column, row, field, died_reason, ignoreL, ignoreU, ignoreD, ignoreR, paralyzed, what, lightnings, hurricane

    amount_players = 0
    character = None
    game_started = False
    field = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]
    what = "start"  # input("\n")
    ignoreL = False
    ignoreR = False
    ignoreU = False
    ignoreD = False
    paralyzed = False
    lightnings = 0
    died_reason = None
    hurricane = False
    GameOver = False

async def gameover(update, context):
     await update.message.reply_text("G͓̽a͓̽m͓̽e͓̽ ͓̽o͓̽v͓̽e͓̽r͓̽")
     global  amount_players, character, game_started,GameOver, chat_id, message_id, column, row, field, died_reason, ignoreL, ignoreU, ignoreD, ignoreR, paralyzed, what, lightnings, hurricane

     amount_players = 0
     character = None
     game_started = False
     field = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]
     what = "start"  # input("\n")
     ignoreL = False
     ignoreR = False
     ignoreU = False
     ignoreD = False
     paralyzed = False
     lightnings = 0
     died_reason = None
     hurricane = False
     GameOver = False
async def mysterious_box(update, context):
     await update.message.reply_text("\U0001F381 What a surprise! Wonder what is inside? Watch out, not always you can find something safe in random boxes📦...\n\n\U0001F6E1 - you can be absolutly safe for once!\n🩴 - be carefull, you holding the most powerfull thing in the ⠀⠀⠀world...use it to push differnt things as far as possible. It ⠀⠀⠀becomes even more crazy when you throw it at hurricane, ⠀⠀⠀it can crash fragments , knockout players or creat deep ⠀⠀⠀hole on the ground\n⚗ - drink it and you will get 3 turns to crush anything you ⠀⠀⠀want!\n🔘 - click it and start firework show. But it can hurt someone, ⠀⠀⠀inluding you...\n🐊 - it is very hungry so it will chase everything eatable! RUN!\n❄ - soooo cold, you will be freezed for 1 - 3 turns")

async def pre_move_skript(update, context):
    global column, row, field, died_reason, ignoreL, ignoreU, ignoreD, ignoreR, paralyzed, what, GameOver, allow_move
    if ignoreL == True and ignoreU == True and ignoreR == True and ignoreD == True:
        died_reason = "Uh, I can't move!"
        await update.message.reply_text(f"{died_reason}")
        GameOver = True

    #moves = ['u', 'r', 'd', 'l']
    if paralyzed == True:
        allow_move = random.choice([True, False])
        print(allow_move)
        if allow_move == True:
            what = None
        else:
            if ignoreL == True and what.title() == "L" or ignoreU == True and what.title() == "U" or ignoreR == True and what.title() == "R" or ignoreD == True and what.title() == "D":
                await pre_move_skript(update, context)
            else:
                what = "You can't move!"
    else:
        allow_move = True
async def left(update, context):
     global column, row, field, died_reason, ignoreL, what, GameOver, allow_move
     if allow_move == True:
         what = "l"
         if column != 0 and field[row][column - 1] == 4:
             hurr = random.randint(0, 4)
             cane = random.randint(0, 4)
             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                 died_reason = "Uhhh, is that dot in the sky you?"
                 field[row][column] = 0
                 GameOver = True
             elif field[hurr][cane] == 0:
                 field[hurr][cane] = 1
                 field[row][column] = 0
                 row = int(hurr)
                 column = int(cane)
                 await post_move_skript(update, context)
         elif column != 0 and field[row][column - 1] != 2:
             field[row][column] = 0
             field[row][column - 1] = 1
             row = row
             column = column - 1
             ignoreL = False
             await post_move_skript(update, context)
         else:
             ignoreL = True
             await update.message.reply_text("No, you can't go there")
             await pre_move_skript(update, context)
     else:
         await update.message.reply_text(what)
         await post_move_skript(update, context)

async def right(update, context):
    global column, row, field, died_reason, ignoreR, what, GameOver
    if allow_move == True:
        what = "r"
        if column != 4 and field[row][column + 1] == 4:
            hurr = random.randint(0, 4)
            cane = random.randint(0, 4)
            if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                died_reason = "Uhhh, is that dot in the sky you?"
                field[row][column] = 0
                GameOver = True
            elif field[hurr][cane] == 0:
                field[hurr][cane] = 1
                field[row][column] = 0
                row = int(hurr)
                column = int(cane)
                await post_move_skript(update, context)
        elif column != 4 and field[row][column + 1] != 2:
            field[row][column] = 0
            field[row][column + 1] = 1
            row = row
            column = column + 1
            ignoreR = False
            await post_move_skript(update, context)
        else:
            ignoreR = True
            await update.message.reply_text("No, you can't go there")
            await pre_move_skript(update, context)
    else:
        await update.message.reply_text(what)
        await post_move_skript(update, context)

async def up(update, context):
    global column, row, field, died_reason, ignoreU, what, GameOver
    if allow_move == True:
        what = "u"
        if row != 0 and field[row - 1][column] == 4:
            hurr = random.randint(0, 4)
            cane = random.randint(0, 4)
            if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                died_reason = "Uhhh, is that dot in the sky you?"
                field[row][column] = 0
                GameOver = True
            elif field[hurr][cane] == 0:
                field[hurr][cane] = 1
                field[row][column] = 0
                row = int(hurr)
                column = int(cane)
                await post_move_skript(update, context)
        elif row != 0 and field[row - 1][column] != 2:
            field[row][column] = 0
            field[row - 1][column] = 1
            row = row - 1
            column = column
            ignoreU = False
            await post_move_skript(update, context)
        else:
            ignoreU = True
            await update.message.reply_text("No, you can't go there")
            await pre_move_skript(update, context)
    else:
        await update.message.reply_text(what)
        await post_move_skript(update, context)

async def down(update, context):
    global column, row, field, died_reason, ignoreD, what, GameOver
    if allow_move == True:
        what = "d"
        if row != 4  and field[row + 1][column] == 4:
            hurr = random.randint(0, 4)
            cane = random.randint(0, 4)
            if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                died_reason = "Uhhh, is that dot in the sky you?"
                field[row][column] = 0
                GameOver = True
            elif field[hurr][cane] == 0:
                field[hurr][cane] = 1
                field[row][column] = 0
                row = int(hurr)
                column = int(cane)
                await post_move_skript(update, context)
        elif row != 4  and field[row + 1][column] != 2:
            field[row][column] = 0
            field[row + 1][column] = 1
            row = row + 1
            column = column
            ignoreD = False
            await post_move_skript(update, context)
        else:
            ignoreD = True
            await update.message.reply_text("No, you can't go there")
            await pre_move_skript(update, context)
    else:
        await update.message.reply_text(what)
        await post_move_skript(update, context)
async def post_move_skript(update, context):
        global column, row, field, died_reason, ignoreL, ignoreU, ignoreD, ignoreR, paralyzed, what, lightnings, hurricane, character, GameOver
        frag = random.randint(0,4)
        ment = random.randint(0,4)
        chance = random.randint(1,100)
        if chance < 8:
            if hurricane == False:
                await update.message.reply_text("I wonder why it is so cloudy...\n")
                await update.message.reply_text("Oh no!It is 🌀ԋυɾɾιƈαɳҽ🌀!")
                while True:
                     if field[frag][ment] != 4:
                         if field[frag][ment] == 1:
                             hurr = random.randint(0, 4)
                             cane = random.randint(0, 4)
                             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                                 died_reason = "Uhhh, is that dot in the sky you?"
                                 GameOver = True
                             elif field[hurr][cane] == 0:
                                 field[hurr][cane] = 1
                                 row = int(hurr)
                                 column = int(cane)
                             field[frag][ment] = 4
                             hurricane = True
                             break
                         else:
                             field[frag][ment] = 4
                             hurricane = True
                             break
                     else:
                         frag = random.randint(0, 4)
                         ment = random.randint(0, 4)
            elif hurricane == True:
                Hlines = 4
                Hcells = 4
                while True:
                    if field[Hlines][Hcells] == 4:
                        field[Hlines][Hcells] = 0
                    Hcells = Hcells - 1
                    if Hcells < 0:
                        Hcells = 4
                        Hlines = Hlines - 1
                    if Hlines < 0:
                        hurricane = False
                        break

        elif chance < 28:
            await update.message.reply_text("I wonder why it is so cloudy...\n")
            await update.message.reply_text("Oh no!It is 🌩️𝘵𝘩𝘶𝘯𝘥𝘦𝘳𝘴𝘵𝘰𝘳𝘮🌩️!")
            ligh = random.randint(0, 4)
            ning = random.randint(0, 4)
            strike = False
            strike_field = copy.deepcopy(field)
            lightnings = random.randint(0,4)
            while strike == False:
                if strike_field[ligh][ning] != 3 and strike_field[ligh][ning] != 4:
                    if strike_field[ligh][ning] == 1:
                        para_dea_chance = random.randint(1,5)
                        if para_dea_chance == 1:
                            paralyzed = True
                            just_paralyzed = True
                        else:
                            died_reason = "So ʂԋσƙ⚡ɳɠ expiriance!"
                            field[ligh][ning] = 0
                            GameOver = True
                    elif strike_field[ligh][ning] == 2:
                        field[ligh][ning] = 0
                    strike_field[ligh][ning] = 3
                    if lightnings == 0:
                        strike = True
                    else:
                        lightnings = lightnings - 1
                else:
                    strike = False
                    ligh = random.randint(0, 4)
                    ning = random.randint(0, 4)
            strike_field_show = ""
            for lineS in strike_field:
                for cellS in lineS:
                    strike_field_show += str(cellS)
                strike_field_show += '\n'
            strike_field_show = strike_field_show.replace('0', '⬛').replace('1', character).replace('2', '🪨').replace('3', '⚡').replace('4', '🌪️')
            await update.message.reply_text(strike_field_show)



        elif chance < 101:
            fall = False
            while fall == False:
                 if field[frag][ment] != 2 and field[frag][ment] != 4:
                     if field[frag][ment] == 1:
                         died_reason = "Oh...You've got smashed..."
                         GameOver = True
                     field[frag][ment] = 2
                     fall = True
                 else:
                     fall = False
                     frag = random.randint(0, 4)
                     ment = random.randint(0, 4)
        frame_field = ""
        for line in field:
             for cell in line:
                 frame_field += str(cell)
             frame_field += '\n'
             frame_field = frame_field.replace('0', '⬛').replace('1', character).replace('2', '🪨').replace('4', '🌪️')
        await update.message.reply_text(frame_field)
        if paralyzed == True and just_paralyzed == True:
            await update.message.reply_text("You've been paralyzed...")
            just_paralyzed = False

        lineAKAfield = field[0] + field[1] + field[2] + field[3] + field[4]
        if died_reason != None:
             await update.message.reply_text(died_reason)
             GameOver = True
        if not 0 in lineAKAfield:
             await update.message.reply_text("ყơų ῳıŋ!")
             await end(update, context)
        if 1 in lineAKAfield:
             if column != 0 and field[row][column - 1] != 2:
                 ignoreL = False
             else:
                 ignoreL = True
             if column != 4 and field[row][column + 1] != 2:
                 ignoreR = False
             else:
                 ignoreR = True
             if row != 0 and field[row - 1][column] != 2:
                 ignoreU = False
             else:
                 ignoreU = True
             if row != 4 and field[row + 1][column] != 2:
                 ignoreD = False
             else:
                 ignoreD = True
             await pre_move_skript(update, context)
        else:
             GameOver = True
        if GameOver == True:
            await gameover(update, context)



def main() -> None:
    global amount_players
    updater = Updater(token, update_queue=True)
    dispatcher = updater
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start_game", start_game))
    application.add_handler(CommandHandler("pick_char", pick_char))
    application.add_handler(CallbackQueryHandler(dispetcher))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("st", special_thanks))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("game_help", game_help))
    application.add_handler(CommandHandler("rules", rules))
    application.add_handler(CommandHandler("end", end))
    application.add_handler(CommandHandler("mysterious_box", mysterious_box))
    application.add_handler(CommandHandler("l", left))
    application.add_handler(CommandHandler("u", up))
    application.add_handler(CommandHandler("r", right))
    application.add_handler(CommandHandler("d", down))
    application.run_polling()


if __name__ == "__main__":
    main()



