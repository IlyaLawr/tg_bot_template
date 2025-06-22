from domain.interfaces.unit_of_work import IUnitOfWork
from domain.entities.profile import Profile
from domain.entities.user import User

from application.dto import RatingInfoResponse


class ShowRatingUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow


    async def execute(self, client_id: int) -> RatingInfoResponse | None:
        all_count_tap = 0
        leader_count_tap = 0
        leader_id = None

        async with self._uow as uow:
            async for profile in uow.profile_repository.get_all():
                all_count_tap += profile.taps_statistics
                if profile.taps_statistics >= leader_count_tap:
                    leader_id = profile.client_id
                    leader_count_tap = profile.taps_statistics

            if leader_id is None:
                return

            leader_user: User = await uow.user_repository.get(leader_id)
            leader_profile: Profile = await uow.profile_repository.get(leader_id)

            user_profile: Profile = await uow.profile_repository.get(client_id)

            if not all((leader_user, leader_profile, user_profile)):
                return

            return RatingInfoResponse(all_count_tap=all_count_tap,
                                      user_count_tap=user_profile.taps_statistics,
                                      leader_count_tap=leader_profile.taps_statistics,
                                      leader_username=leader_user.username,
                                      leader_name=leader_profile.name,
                                      leader_about=leader_profile.about,
                                      leader_photo=leader_profile.photo)
