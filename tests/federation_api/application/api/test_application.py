class TestApplication():
    class TestIndex():
        def test_ok(self, client):
            assert client.get('/').status_code == 200


    class TestStatus():
        def test_ok(self, client):
            response = client.get('/status')
            assert response.status_code == 200
            assert response.json == {'status': {'Database': 'Up'}}
