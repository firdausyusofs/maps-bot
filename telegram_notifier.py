import requests
import json

api_key = "5878407640:AAFXg94u4hiwTeiXm7jvPVz29MIUQ9huul4"

class TelegramNotifier():
    chat_ids = []

    def get_users(self):
        response = requests.get(f'https://api.telegram.org/bot{api_key}/getUpdates')
        json = response.json()
        for i, v in enumerate(json['result']):
            if "message" in v:
                self.chat_ids.append(v["message"]["chat"]["id"])

    def __init__(self):
        self.get_users()

    def notify(self, message):
        for i, v in enumerate(set(self.chat_ids)):
            self.send_telegram_message(message, v)

    def send_telegram_message(self,
                              message: str,
                              chat_id: str):
        headers = {
            'Content-Type': 'application/json',
            'Proxy-Authorization': 'Basic base64'
        }
        data_dict = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_notification': False
        }

        data = json.dumps(data_dict)
        url = f'https://api.telegram.org/bot{api_key}/sendMessage'
        response = requests.post(url,
                                 data=data,
                                 headers=headers,
                                 verify=False)

        return response
