from fastapi.testclient import TestClient

import main


client = TestClient(
    main.app
)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["application"] == "EduGenie"


def test_qa_endpoint(
    monkeypatch
):

    def fake_answer(
        question
    ):

        return "Test answer"


    monkeypatch.setattr(
        main,
        "answer_question",
        fake_answer
    )


    response = client.post(
        "/qa",
        json={
            "text": "What is Python?"
        }
    )


    assert response.status_code == 200

    assert response.json()[
        "result"
    ] == "Test answer"