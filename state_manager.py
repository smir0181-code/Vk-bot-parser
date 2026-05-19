
import json
from logger import log



STATE_FILE = 'bot_state.json'

class StateManager:
    def __init__(self,state_file=STATE_FILE):
        self.state_file = state_file

    def save(self, last_post_id, last_comment_ids):
        with open(self.state_file, 'w') as f:
            json.dump({
                'last_post_id': last_post_id,
                'last_comment_ids': last_comment_ids
            }, f)
        log.info(f"Состояние сохранено в {self.state_file}")
    
    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data.get('last_post_id', 0), data.get('last_comment_ids', {})
        except FileNotFoundError:
            log.info("Файл состояния не найден, начинаем с нуля")
            return 0, {}

