from django.core.management import BaseCommand

from site_app.bot_telegram import bot


class Command(BaseCommand):
    help = 'Listen bot'

    def handle(self, *args, **options):
        bot.polling()
        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
