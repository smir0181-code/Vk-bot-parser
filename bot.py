import time
from datetime import datetime
from state_manager import StateManager

from google_sheets import get_sheet
from logger import log
from vk_client import VKClient
from config import VK_TOKEN,VK_GROUP_ID
from parsers import parse_post_text
from db_manager import DatabaseManager

data_manager=DatabaseManager() 
state_manager=StateManager()

data_manager.init_db()


class Bot:
    def __init__(self, vk_client, state_manager, data_manager):
        self.vk_client = vk_client
        self.state_manager = state_manager
        self.data_manager = data_manager
        self.last_post_id, self.last_comment_ids = state_manager.load_state()
        log.info(f"Загружено состояние: last_post_id={self.last_post_id}, last_comment_ids={self.last_comment_ids}")
    
    def run(self):
        while True:
            try:
                log.info("Проверка новых постов...")
                new_posts = self.vk_client.get_new_posts(self.last_post_id)
                log.info(f"Найдено {len(new_posts)} новых постов")
                for post in new_posts:
                    title, article, price = parse_post_text(post['text'])
                    if title and article and price:
                        post_date = datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')
                        data_manager.save_post(post['id'], title, article, price, post_date)
                        # row=
                        # append_row(row)
                        log.info(f"Новый пост {post['id']}: {title} | {article} | {price}")
                        if post['id'] not in self.last_comment_ids:
                            self.last_comment_ids[post['id']] = 0
                    else:
                        log.info(f"Пост {post['id']} не соответствует формату")
                if new_posts:
                    max_id = max(p['id'] for p in new_posts)
                    if max_id > self.last_post_id:
                        self.last_post_id = max_id
                        log.info(f"last_post_id обновлён до {self.last_post_id}")

                log.info("Проверка комментариев...")
                updated_comment_ids = {}
                for post_id in list(self.last_comment_ids.keys()):
                    last_cid = self.last_comment_ids[post_id]
                    comments = self.vk_client.get_comments_for_post(post_id, last_cid)
                    if comments:
                        log.info(f"Пост {post_id}: {len(comments)} новых комментариев")
                        post_data = data_manager.get_post(post_id)
                        if post_data:
                            title, article, price, post_date = post_data
                            for comment in comments:
                                comment_date = datetime.fromtimestamp(comment['date']).strftime('%Y-%m-%d %H:%M:%S')
                                data_manager.save_comment_to_queue(post_id, comment['id'], comment['from_id'], comment['text'], comment_date)
                                log.info(f"Добавлен комментарий {comment['id']} от {comment['from_id']}")
                        else:
                            log.info(f"Нет данных для поста {post_id}")
                        updated_comment_ids[post_id] = max(c['id'] for c in comments)
                        
                for post_id, new_last in updated_comment_ids.items():
                    self.last_comment_ids[post_id] = new_last
                data_manager.sync_comments_to_sheets()
                state_manager.save(self.last_post_id, self.last_comment_ids)
                
                
                log.info("Пауза 60 секунд...")
                time.sleep(60)

            except KeyboardInterrupt:
                log.info("Остановка по запросу пользователя, сохраняю состояние...")
                state_manager.save(self.last_post_id, self.last_comment_ids)
                break
            
            
            
            except Exception as e:
                log.error(f"Критическая ошибка: {e}")
                
                
            
                                

if __name__=="__main__":
    vk_client = VKClient(VK_TOKEN, VK_GROUP_ID)
    state_manager = StateManager()
    data_manager = DatabaseManager()
    data_manager.init_db()
    bot = Bot(vk_client, state_manager, data_manager)
    bot.run()
