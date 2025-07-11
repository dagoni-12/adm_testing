import pytest
@pytest.mark.parametrize("port, expected_error", [("80", "Значение порта не должно быть меньше 1024."), ("50000", "Значение порта не должно быть больше 49151."), ("", "Поле должно быть заполнено."), ("1024", None), ("49151", None),], 
                         ids=["small port", "big port", "empty port", "min. port", "max. port"])
def test_invalid_port_validation(setupmanager, port, expected_error):
    setupmanager.force_clear_port_field()
    setupmanager.set_port(port)
    setupmanager.set_username("valid_user")
    setupmanager.set_password("valid_password")
    setupmanager.click_install()
    actual_error = setupmanager.get_error_message()
    assert actual_error == expected_error, \
        f"Ожидалась ошибка: '{expected_error}', но получено: '{actual_error}'"

@pytest.mark.parametrize("username, password, expected_error", [("", "valid_password", "Поле должно быть заполнено."), ("valid_user", "", "Поле должно быть заполнено."), ("", "", "Поле должно быть заполнено."), ("invalid_user", "wrong_pass", "Incorrect login/password to connect to the SSH-server"), ("root", "pwdroot", "Менеджер успешно установлен")], 
                         ids=["empty usrname", "empty pwd", "both empty", "invalid creds.", "valid creds."])
def test_ssh_credentials_validation(setupmanager, username, password, expected_error):
    if username:
        setupmanager.set_username(username)
    if password:
        setupmanager.set_password(password)
    setupmanager.click_install()
    
    if "Incorrect login/password" in str(expected_error):
        actual_error = setupmanager.get_error_message_incorrect()
        assert "Incorrect login/password" in str(actual_error), \
            f"Ожидалась ошибка авторизации, но получено: '{actual_error}'"
    elif "Менеджер успешно установлен" in str(expected_error):
        actual_error = setupmanager.get_error_message_incorrect()
        assert "Менеджер успешно установлен" in str(actual_error), \
            f"Ожидалась авторизация, но получено: '{actual_error}'"
    else:
        actual_error = setupmanager.get_error_message()
        assert actual_error == expected_error, \
            f"Ожидалась ошибка: '{expected_error}', но получено: '{actual_error}'"
