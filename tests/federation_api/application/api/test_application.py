import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestApplication():
    def test_index(self):
            assert self.client.get(url_for('index')).status_code == 200


    def test_status(self):
        response = self.client.get(url_for('application.status'))
        assert response.status_code == 200
        assert response.json == {'status': {'Database': 'Up'}}
