from aiogram import Bot, Dispatcher, Router
from asyncio import run
import redis.asyncio as redis

from domain.services.answer_validation import AnswerValidationService
from domain.factories.game_factory import GameFactory

from infrastructure.state_cache import (
    RedisProfileFillingStateCache as ProfileCache, RedisGameStateCache as GameCache)

from infrastructure.repositories import (
    SQLProfileRepository as ProfileRepo, SQLUserRepository as UserRepo)

from infrastructure.sql_alchemy_uow import SqlAlchemyUnitOfWork as UoW
from infrastructure.disk_photo_stogare_service import DiskPhotoStorageService as PhotoStorage

from application.use_case import (
    RegisterUserUseCase as RegisterUC, FillingProfileUseCase as FillProfileUC,
    UpdateProfileUseCase as UpdateProfileUC, AccessCheckUseCase as AccessUC)
 
from application.use_case import (
    GameActionUseCase as GameUC, SavingGameResultUseCase as SaveGameUC,
    ShowRatingUseCase as RatingUC)

from application.use_case import CanselInteractionUseCase as CancelUC

from presentation.handlers import (
    setup_filling_profile_handlers as setup_profile, setup_game_handlers as setup_game,
    setup_start_handlers as setup_start, setup_info_handlers as setup_info,
    setup_menu_handlers as setup_menu, setup_rating_handlers as setup_rating)

from presentation.services.ui_state_service import RedisUIStateService
from presentation.services.interaction_state_manager import InteractionStateManager
from presentation.services.content_parse_service import TelegramMessageParser
from presentation.utils.keyboards import set_command

from settings import settings

photo_storage_service = PhotoStorage(settings.photo_storage)

redis_client = redis.from_url(url=settings.redis_url, encoding='utf-8', decode_responses=False)

unit_of_work = UoW(db_url=settings.db_url,user_repo_cls=UserRepo, profile_repo_cls=ProfileRepo)

game_state_cache = GameCache(redis_client=redis_client,game_factory=GameFactory())

filling_profile_state_cache = ProfileCache(redis_client=redis_client)

update_profile_use_case = UpdateProfileUC(state_cache=filling_profile_state_cache, uow=unit_of_work,
                                          photo_storage_service=photo_storage_service)

saving_game_result_use_case = SaveGameUC(game_state=game_state_cache, uow=unit_of_work)

cancel_interaction_use_case = CancelUC(profile_update_use_case=update_profile_use_case, 
                                       saving_game_result_use_case=saving_game_result_use_case)

filling_profile_use_case = FillProfileUC(state_cache=filling_profile_state_cache,
                                         profile_update_use_case=update_profile_use_case,
                                         validator=AnswerValidationService())

register_user_use_case = RegisterUC(settings.pass_phrase, uow=unit_of_work)
game_acation_use_case = GameUC(game_state=game_state_cache)
access_check_use_case = AccessUC(uow=unit_of_work)
show_rating_use_case = RatingUC(uow=unit_of_work)

ui_state_service = RedisUIStateService(redis_client=redis_client)

interaction_state_manager = InteractionStateManager(ui_state_service=ui_state_service,
                                                    cancel_interaction_use_case=cancel_interaction_use_case)


async def main():
    bot = Bot(token=settings.bot_token)

    dispatcher = Dispatcher()

    command_router = Router()
    game_action_router = Router()
    filling_profile_router = Router()

    setup_start(router=command_router, use_case_register_user=register_user_use_case,
                use_case_access_check=access_check_use_case, interaction_state_manager=interaction_state_manager)

    setup_profile(router=filling_profile_router, interaction_state_manager=interaction_state_manager,
                  use_case_filling_profile=filling_profile_use_case, content_parser=TelegramMessageParser(bot=bot))
    
    setup_game(router=game_action_router, use_case_game_action=game_acation_use_case,
               interaction_state_manager=interaction_state_manager)
    
    setup_rating(router=command_router, use_case_show_rating=show_rating_use_case)
    setup_menu(router=command_router, interaction_state_manager=interaction_state_manager)
    setup_info(router=command_router)

    dispatcher.workflow_data['ui_state_service'] = ui_state_service

    dispatcher.include_router(command_router)
    dispatcher.include_router(filling_profile_router)
    dispatcher.include_router(game_action_router)

    await set_command(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, polling_timeout=60, handle_signals=False)

if __name__ == "__main__":
    run(main())
