import config
import requests


class WhatsappIntegrationBase:
    BASE_URL = 'https://graph.facebook.com'
    VERSION = 'v21.0'
    SENDER_ID = config.SENDER_ID
    SEND_URL = f'{BASE_URL}/{VERSION}/{SENDER_ID}/messages'
    TOKEN = config.TOKEN

    def get_template_name(self):
        return "confirm_account"

    def get_template_params(self, params: dict) -> list:
        return [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": params.get("text"),
                    }
                ]
            }
        ]

    def send(self, to: str, params: dict):
        body = {
            "messaging_product": "whatsapp",
            "to": to.removeprefix('+'),
            "type": "template",
            "template": {
                "name": self.get_template_name(),
                "language": {
                    "code": "en_US"
                },
                "components": self.get_template_params(params)
            }
        }
        headers = {
            'Authorization': f'Bearer {self.TOKEN}'
        }
        return requests.post(self.SEND_URL,
                             json=body,
                             headers=headers)


class WhatsappIntegrationConfirmation(WhatsappIntegrationBase):
    pass


class HelloWorldIntegrationConfirmation(WhatsappIntegrationBase):

    def get_template_name(self):
        return "hello_world"

    def get_template_params(self, params: dict) -> list:
        return []