import vk_api
from config import VK_TOKEN, VK_GROUP_ID



class VKClient:
    def __init__(self,token,group_id):
        self.token=token
        self.group_id=group_id
        vk_session = vk_api.VkApi(token=self.token, api_version='5.131')
         
        self.vk=vk_session.get_api()
        
    def get_new_posts(self,last_post_id=0):
        """Возвращает список новых постов (с ID > last_post_id)."""
        # Для группы
        response = self.vk.wall.get(owner_id=self.group_id, count=100, filter='owner')
        posts = []
        for item in response['items']:
            if item['id'] > last_post_id:
                posts.append({
                    'id': item['id'],
                    'text': item['text'],
                    'date': item['date']
                })
        return posts    


    def get_comments_for_post(self,post_id, last_comment_id=0):
        response = self.vk.wall.getComments(owner_id=self.group_id, post_id=post_id, need_likes=0, count=10)
        comments = []
        for item in response['items']:
            if item['id'] > last_comment_id:
                comments.append({
                    'id': item['id'],
                    'from_id': item['from_id'],
                    'text': item['text'],
                    'date': item['date']          # добавляем дату комментария
                })
        return comments

