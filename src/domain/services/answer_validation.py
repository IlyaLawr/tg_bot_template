from typing import Callable
from re import fullmatch

from domain.dataclasses import ValidationResult


class AnswerValidationService:
    def __init__(self) -> None:
        self._validators: dict[int, Callable[[str | bytes], ValidationResult]] = {
            1: self._validate_name,
            2: self._validate_about,
            3: self._validate_photo,
        }

        self.questions = {1: 'Напишите ваше имя', 
                          2: 'Напишите о себе',
                          3: 'Добавьте фото'}


    def check(self, answer: str | bytes, question_number: int) -> ValidationResult:
        validator = self._validators.get(question_number)
        if not validator:
            return ValidationResult(False, f'Неизвестный номер вопроса: {question_number}')
        return validator(answer)


    def _validate_name(self, answer: str) -> ValidationResult:
        answer = (answer or '').strip()

        if not answer:
            return ValidationResult(False, 'Имя не может быть пустым')
        if len(answer) < 2 or len(answer) > 50:
            return ValidationResult(False, 'Имя должно содержать от 2 до 50 символов')
        if not fullmatch(r'[A-Za-zА-Яа-яЁё\s\-]+', answer):
            return ValidationResult(False, 'Имя содержит недопустимые символы')

        return ValidationResult(True)


    def _validate_about(self, answer: str) -> ValidationResult:
        answer = (answer or '').strip()

        if not answer:
            return ValidationResult(False, 'Поле «О себе» не может быть пустым')
        if len(answer) < 10:
            return ValidationResult(False, 'Расскажите о себе чуть подробнее (не менее 10 символов)')
        if len(answer) > 500:
            return ValidationResult(False, 'Поле «О себе» слишком длинное (макс. 500 символов)')

        return ValidationResult(True)


    def _validate_photo(self, answer: bytes) -> ValidationResult:
        if answer is None:
            return ValidationResult(False, 'Фото обязательно')
        if isinstance(answer, bytes):
            return ValidationResult(True)

        return ValidationResult(False, 'Некорректный формат фото')
