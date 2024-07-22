from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from please_ignore_this import token, open_ai_key
from openai import OpenAI

#telegram info 
TOKEN: Final = token
BOT_USERNAME: Final = "@Test_2024_MNIC_bot"

#openai info
client = OpenAI(api_key=open_ai_key)


#commands telegram
async def start_command(update: Update, cotext: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    await update.message.reply_text(f"""
\U0001F1EC\U0001F1E7    \U0001F375
Hey {username}, I'm a bot created by @justinmnic
This bot uses the credits from OpenAI API, so most likely it will be disscontinued soon...

\U0001F1F7\U0001F1FA    \U0001F1F7\U0001F1FA 
Привет {username}.я бот, созданный @justinmnic
Этот бот использует кредит от OpenAI API, так что, скорее всего, он будет прекращен в ближайшее время.""")
    

#handle responses
def handle_responses(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=100,
        temperature=0.4,
        n=1,
        presence_penalty=0,
        frequency_penalty=0,
        messages=[
            {"role": "system", "content": "You are a developer that gives a short and precise explanation. Also, every answer you give is first in English, then in a new row the same answer but in Russian."},
            {"role": "user", "content": f"{user_message}"}
        ]
    )
    return response.choices[0].message.content

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = handle_responses(user_message)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    
if __name__ == "__main__":
    print("Bot started")
    app = Application.builder().token(TOKEN).build()
    
    #commands
    app.add_handler(CommandHandler("start", start_command))
    
    #messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    #errors
    app.add_error_handler(error)
    
    #polling
    print("Bot started polling")
    app.run_polling(poll_interval=3)
    
    app.run()