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

    call1 = switchboard.register_call("1,Ivan,+7123,2,Zhen,+1123")
    call2 = switchboard.register_call("3,Zhen,+1123,4,Ivan,+7123")
    call3 = switchboard.register_call("5,Ivan,+7123,6,Zhen,+7123")
    call4 = switchboard.register_call("7,Zhen,+1123,8,Jane,+4123")

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

