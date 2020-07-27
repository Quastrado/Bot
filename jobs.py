def send_hello(context):
    context.bot.send_message(chat_id=555825427, text=f'hello {context.job.interval}')
    context.job.interval += 5
    if context.job.interval > 15:
        context.bot.send_message(chat_id=555825427, text="bye")
        context.job.schedule_removal()
