from telegram_notifier import TelegramNotifier

notifier = TelegramNotifier()

notifier.notify('''
Completed: Thursday

6:00 - 2.3, 101.1 to 3.5, 101.3
6:30 - 2.3, 101.1 to 3.5, 101.3
''')
