from application.dto import RatingInfoResponse

menu_text = '''
*Добро пожаловать в главное меню!*

/game — *просто жми и не думай*  
/rating — *общий рейтинг*  
/set\\_profile — *добавить инфу о себе, чтобы все знали кто самый сильный игрок тут.*
'''

help_text = '*Бот для соревнования по тыканью по кнопке. Тыкай в кнопку и побеждай!*'



def create_rating_table(rating_info: RatingInfoResponse) -> str:

    template = (
        f'<b>Всего нажатий твоих:</b> {rating_info.user_count_tap}\n'
        f'<b>Всего нажатий:</b> {rating_info.all_count_tap}\n\n'
        f'<b>Лучший жмакер:</b>\n'
        f'   {rating_info.leader_name} '
        f'<a href=\"https://t.me/{rating_info.leader_username}\">@{rating_info.leader_username}</a>\n'
        f'   {rating_info.leader_about}')

    return template


def create_result_game(result: int = 0) -> str:
    return f'*Количество нажатий в сессии: {result}*'
