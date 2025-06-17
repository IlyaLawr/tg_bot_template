from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserRequest:
    client_id: int
    username: str
    pass_phrase: str


@dataclass(frozen=True)
class RegisterUserResponse:
    success: bool
    message: str


@dataclass
class FormUserRequest:
    client_id: int
    content: str | bytes


@dataclass
class FormUserResponse:
    success: bool
    message: str
    error: str | None = None
    complete: bool = False


@dataclass
class CheckUserResponse:
    success: bool
    message: str


@dataclass
class RatingInfoResponse:
    all_count_tap: int
    user_count_tap: int
    leader_count_tap: 0
    leader_username: str
    leader_name: str
    leader_about: str
    leader_photo: str
