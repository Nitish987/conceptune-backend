from .models import Chatbot
from ..apis.models import Api
from ..apis.services import ApiService
from common.platform.products import Product
from common.debug.log import Log



class ChatbotService:
    @staticmethod
    def configure(data):
        api = Api.objects.get(id=data.get('api_id'))
        chatbot = Chatbot.objects.create(
            api=api,
            type=api.type,
            config=data.get('config'),
            data=data.get('data')
        )
        return ChatbotService.to_json(chatbot)
    
    @staticmethod
    def get_configuration(api_id, chatbot_id):
        api = Api.objects.get(id=api_id)
        chatbot = Chatbot.objects.get(id=chatbot_id, api=api)
        return ChatbotService.to_json(chatbot)
    
    @staticmethod
    def to_json(chatbot: Chatbot):
        return {
            'id': chatbot.pk,
            'api': ApiService.to_json(chatbot.api),
            'config': chatbot.config,
            'data': chatbot.data
        }
