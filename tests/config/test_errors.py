import pytest
from config.initializers.errors import NotFoundException, \
    ParametersException, UnprocessibleEntryException


class TestErrors():
    def test_not_found_exception_error(self):
        with pytest.raises(SyntaxError):
            not_found_exception = NotFoundException()


    def test_not_found_exception(self):
        not_found_exception = NotFoundException(model='Person', attribute='id',
                                                value=0)
        assert not_found_exception.message.json == {
            'status': ["Person with id='0' not found"]}


    def test_parameters_exception(self):
        parameters_exception = ParametersException('is missing',
                                                   'id', 'created_at')
        assert parameters_exception.message.json == {
            'status': ["'id' key is missing", "'created_at' key is missing"]}


    def test_unprocessible_entry_exception(self):
        unprocessible_entry_exception = UnprocessibleEntryException(
            ["'id' cannot be 0", "'created_at' cannot be NULL"])
        assert unprocessible_entry_exception.message.json == {
            'status': ["'id' cannot be 0", "'created_at' cannot be NULL"]}