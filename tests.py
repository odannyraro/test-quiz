import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_inappropriate_points():
    with pytest.raises(Exception):
        Question(title='q1', points=-13)
    with pytest.raises(Exception):
        Question(title='q1', points=122)

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points='')
    with pytest.raises(Exception):
        Question(title='q1', points=[])
    with pytest.raises(Exception):
        Question(title='q1', points='13')
    with pytest.raises(Exception):
        Question(title='q1', points=[13, 22])

def test_add_choice_returns_choice_with_sequential_id():
    question = Question(title='q1')

    first = question.add_choice('a')
    second = question.add_choice('b')

    assert first.id == 1
    assert second.id == 2
    assert first is question.choices[0]

def test_add_choice_rejects_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')

def test_add_choice_rejects_text_over_100_characters():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_set_correct_choices():
    question = Question(title='q1')  
    question.add_choice('a') # 'a' id = 1, index = 0
    question.add_choice('b') # 'b' id = 2, index = 1
    question.add_choice('c') # 'c' id = 3, index = 2
    question.add_choice('d') # 'd' id = 4, index = 3
    question.set_correct_choices([2, 3])
    choice = question.choices[0]
    assert not choice.is_correct
    choice = question.choices[1]
    assert choice.is_correct
    choice = question.choices[2]
    assert choice.is_correct
    choice = question.choices[3]
    assert not choice.is_correct   
    
def test_set_correct_choice_to_inexistent():
    question = Question(title='q1')  
    question.add_choice('a') # 'a' id = 1, index = 0
    with pytest.raises(Exception):
        question.set_correct_choices([0])
    with pytest.raises(Exception):
        question.set_correct_choices([2, 1])

def test_set_correct_choice_to_invalid():
    question = Question(title='q1')  
    question.add_choice('a') # 'a' id = 1, index = 0
    with pytest.raises(Exception):
        question.set_correct_choices(['', '1'])


def test_correct_selected_choices():
    question = Question(title='q1', points=10, max_selections=2)  
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', True)
    assert not question.correct_selected_choices([])
    assert not question.correct_selected_choices([1])
    assert question.correct_selected_choices([1, 2]) == [2]
    assert question.correct_selected_choices([2, 3]) == [2, 3]

def test_exceeded_quantity_of_selected_choices():
    question = Question(title='q1', points=10, max_selections=1)  
    question.add_choice('a', False)
    question.add_choice('b', True)
    with pytest.raises(Exception):
        question.correct_selected_choices([1,2])

