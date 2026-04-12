import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser

#проверка создания правильных пользователей по номеру
def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


# количество АКТИВНЫХ звонков
def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


#проверка количества BORDER_CALLS
def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_cross_border_detection_both_directions() -> None:
    switchboard = Switchboard()

    call1 = switchboard.register_call("1,Ivan D,+7123,2,Zhen D,+1123")
    call2 = switchboard.register_call("3,Zhen D,+1123,4,Ivan D,+7123")
    call3 = switchboard.register_call("5,Ivan D,+7123,6,Zhen D,+7123")
    call4 = switchboard.register_call("7,Zhen D,+1123,8,Jane D,+4123")

    assert call1.is_cross_border is True
    assert call2.is_cross_border is True
    assert call3.is_cross_border is False
    assert call4.is_cross_border is False


def test_userid_is_not_int_should_return_exception() -> None:
    with pytest.raises(TypeError, match="User id must be int"):
        LocalUser(id="1", fullname="John", phone="+7123456789")


def test_user_fullname_is_not_str_should_return_exception() -> None:
    with pytest.raises(TypeError, match="User fullname must be str"):
        LocalUser(id=1, fullname=123, phone="+7123456789")


def test_user_fullname_is_empty_should_return_exception() -> None:
    with pytest.raises(ValueError, match="User fullname cannot be empty"):
        LocalUser(id=1, fullname="", phone="+7123456789")


def test_user_phone_is_not_str_should_return_exception() -> None:
    with pytest.raises(TypeError, match="User phone must be str"):
        LocalUser(id=1, fullname="John Doe", phone=123456789)


def test_user_phone_is_empty_should_return_exception() -> None:
    with pytest.raises(ValueError, match="User phone cannot be empty"):
        LocalUser(id=1, fullname="John Doe", phone="")


def test_raw_call_is_not_string() -> None:
    switchboard = Switchboard()
    with pytest.raises(TypeError, match="Входные данные должны быть типом str"):
        switchboard.register_call(123)


def test_raw_call_is_empty_string() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match="Введенные данные не соответствуют, требуется 6 элементов"):
        switchboard.register_call("")


def test_raw_call_too_few_elements() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match="Введенные данные не соответствуют, требуется 6 элементов"):
        switchboard.register_call("1,Ivan D,+7123,2,Petr D")


def test_caller_id_is_not_integer() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match="id должен быть числом"):
        switchboard.register_call("abc,Ivan D,+71234567,2,John D,+11234567")


def test_receiver_id_is_not_integer() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match="id должен быть числом"):
        switchboard.register_call("1,Ivan D,+71234567,xyz,John D,+11234567")

def test_user_fullname_is_empty_register_call() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match='Поле "Имя Фамилия" не должно быть пустым'):
        switchboard.register_call("1,,+71234567,2,John D,+11234567")


def test_user_fullname_with_digits_register_call() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match='Поле "Имя Фамилия" должно состоять только из букв'):
        switchboard.register_call("1,Ivan123 D,+71234567,2,John D,+11234567")


def test_phone_is_empty_register_call() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match='Номер телефона не должен быть пустым'):
        switchboard.register_call("1,Ivan D,,2,John D,+11234567")


def test_phone_without_plus_register_call() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match='Номер телефона должен начинаться с'):
        switchboard.register_call("1,Ivan D,71234567,2,John D,+11234567")


def test_phone_with_letters_register_call() -> None:
    switchboard = Switchboard()
    with pytest.raises(ValueError, match='Номер телефона должен содержать только цифры после'):
        switchboard.register_call("1,Ivan D,+7A1234567,2,John D,+11234567")
