import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import replicate as repl

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("https").setLevel(logging.WARNING)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):


    await update.message.reply_text("Welcome to Text to Image Bot. Just send a text then I send you the image")
    # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("1.png", "rb"), caption="The image you requested is sended to you")
    # await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open('voice1.ogg', 'rb'), caption="Voice is sended to you")


async def make_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        prompt = text

        replicate = repl.Client(api_token='r8_EewS7AZ9RVsV1EMEwtqRHAOWImGhnpg3NZANq')
        output = replicate.run(
            "bingbangboom-lab/flux-dreamscape:b761fa16918356ee07f31fad9b0d41d8919b9ff08f999e2d298a5a35b672f47e",
            input = {
                "width": 512,
                "height": 512,
                "prompt": prompt,
                "refine": "expert_ensemble_refiner",
                "scheduler": "K_EULER",
                "lora_scale": 0.6,
                "num_outputs": 1,
                "guidiance_scale": 7.5,
                "apply_watermark": False,
                "high_noise_frac": 0.8,
                "negative_prompt": "",
                "prompt_strength": 0.8,
                "num_inference_steps": 25
            }
        )

        image_url = output[0]

        # img = Image.open(req.get(output[0], stream=True).raw)
        await update.message.reply_photo(photo=image_url, caption="Image you requested has been generated successfully")
    except Exception as e:
        await update.message.reply_text(f"Generation failed because of error: {e}")

application = ApplicationBuilder().token("7261405517:AAGWx5a4XyLrL_za6Ed02NVf_aS-A2c78B0").build()
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

new_h = MessageHandler(filters.TEXT, make_image)
application.add_handler(new_h)

application.run_polling()
