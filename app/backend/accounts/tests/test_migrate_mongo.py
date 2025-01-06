import pytest

from backend.accounts.management.commands.migrate_mongo import Command

@pytest.fixture
def mock_stdout(mocker):
    return mocker.MagicMock()

@pytest.fixture
def mock_importlib(mocker):
    return mocker.patch("importlib.import_module")

@pytest.fixture
def migrations():
    return [
        'backend.accounts.migrations.001_create_indexes_user',
        'backend.books.migrations.001_create_indexes_book',
    ]

def test_execute_migrations_success(mock_stdout, mock_importlib, mocker, migrations):
    mock_module = mocker.MagicMock()
    mock_module.run = mocker.MagicMock()
    mock_importlib.return_value = mock_module

    command = Command()
    command.stdout = mock_stdout
    command.execute_migrations()

    for migration in migrations:
        mock_importlib.assert_any_call(migration)
        mock_stdout.write.assert_any_call(command.style.SUCCESS(f"Running migration: {migration}"))
        mock_stdout.write.assert_any_call(command.style.SUCCESS(f"Migration {migration} successfully executed"))

    assert mock_importlib.call_count == len(migrations)
    assert mock_module.run.call_count == len(migrations)

def test_execute_migrations_no_run_function(mock_stdout, mock_importlib, mocker, migrations):
    mock_module = mocker.MagicMock()
    del mock_module.run  # Eliminar la función `run`
    mock_importlib.return_value = mock_module

    command = Command()
    command.stdout = mock_stdout
    command.execute_migrations()

    for migration in migrations:
        mock_importlib.assert_any_call(migration)
        mock_stdout.write.assert_any_call(command.style.ERROR(f"The {migration} module does not have a 'run' function"))

    assert mock_importlib.call_count == len(migrations)


def test_execute_migrations_module_not_found(mock_stdout, mock_importlib, migrations):
    mock_importlib.side_effect = ModuleNotFoundError

    command = Command()
    command.stdout = mock_stdout
    command.execute_migrations()

    for migration in migrations:
        mock_importlib.assert_any_call(migration)
        mock_stdout.write.assert_any_call(command.style.ERROR(f"Module not found: {migration}"))

    assert mock_importlib.call_count == len(migrations)


def test_execute_migrations_general_exception(mock_stdout, mock_importlib, migrations):
    mock_importlib.side_effect = Exception("Test exception")

    command = Command()
    command.stdout = mock_stdout
    command.execute_migrations()

    for migration in migrations:
        mock_importlib.assert_any_call(migration)
        mock_stdout.write.assert_any_call(
            command.style.ERROR(f"Error while executing migration {migration}: Test exception")
        )

    assert mock_importlib.call_count == len(migrations)


def test_handle_method(mock_stdout, mocker):
    mock_execute_migrations = mocker.patch.object(Command, "execute_migrations")

    command = Command()
    command.stdout = mock_stdout
    command.handle()

    mock_execute_migrations.assert_called_once()
    mock_stdout.write.assert_any_call(command.style.SUCCESS("MongoDB migrations applied"))
