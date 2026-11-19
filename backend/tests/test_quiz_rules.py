from app.api.routes import QUIZZES


def test_every_seeded_course_has_quiz():
    assert set(QUIZZES) == {"climate-basics", "clean-energy", "biodiversity", "circular-economy"}


def test_quiz_answer_keys_match_question_and_option_counts():
    for quiz in QUIZZES.values():
        assert len(quiz["questions"]) == len(quiz["answers"]) == len(quiz["options"])
        assert all(0 <= answer < len(options) for answer, options in zip(quiz["answers"], quiz["options"]))
