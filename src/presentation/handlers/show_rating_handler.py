from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.logic import or_f as Or
from aiogram.types import Message, FSInputFile

from application.use_case.show_rating import ShowRatingUseCase
from application.dto import RatingInfoResponse

from presentation.utils.templates import create_rating_table


def setup_rating_handlers(router: Router,
                          use_case_show_rating: ShowRatingUseCase) -> None:

    @router.message(Or(Command('rating'), F.text == 'Рейтинг'))
    async def command_handler(message: Message) -> None:
        client_id = message.from_user.id

        result: RatingInfoResponse | None = await use_case_show_rating.execute(client_id)
        if result:
            rating_table = create_rating_table(result)
            await message.answer(rating_table, parse_mode='HTML', disable_web_page_preview=True)
            if result.leader_photo:
                await message.answer_photo(FSInputFile(result.leader_photo))
