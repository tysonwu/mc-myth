from collections import Counter

import numpy as np
from numpy.random import default_rng

class Exam:

    '''
    Generates random answers with A/B/C/D notated in 0/1/2/3
    '''

    N_QUESTIONS = 45
    N_QUESTIONS_A = 30
    N_QUESTIONS_B = 25
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = default_rng(seed)

        self._answer = self._make_answers()
    
    def _make_answers(self):
        '''
        A generation of model answers based on the observed pattern in real world
        Generation is restricted so that part A consists of either 8 or 9 questions with answer 0/1/2/3
        The only possible combinations are, exhaustively, 7/7/8/8, 7/8/7/8, 7/8/8/7, 8/7/7/8, 8/7/8/7, 8/8/7/7
        '''
        part_a = np.array([0] * 7 + [1] * 7 + [2] * 7 + [3] * 7)
        # randomly choose two elements in 0/1/2/3 
        extra_part_a = self.rng.choice([0, 1, 2, 3], size=2, replace=False)
        not_in_extra_part_a = np.array([i for i in [0, 1, 2, 3] if i not in extra_part_a]) # is just complement of extra_part_a
        part_a = np.append(part_a, extra_part_a)
        
        # the two chosen in extra_part_a must have 4 questions with such answer in part B

        # all the fuzz because
        # if we have 7 As in Part A then there must be 4 As in Part B
        part_b = np.array([0] * 3 + [1] * 3 + [2] * 3 + [3] * 3)
        part_b = np.append(part_b, not_in_extra_part_a)
        part_b = np.append(part_b, self.rng.choice(extra_part_a, size=1, replace=False))
        
        # append them together
        answers = np.append(part_a, part_b)
        self.rng.shuffle(answers)
        return answers

    @property
    def answer(self):
        return self._answer

    def get_answer_distribution(self):
        return Counter(self._answer)

    def get_score(self, attempted: np.array) -> int:
        return sum([attempted_ans == model_ans for attempted_ans, model_ans in zip(attempted, self._answer)])


if __name__ == '__main__':
    # test the functionalities
    seed = 2021

    m = Exam(seed=seed)
    m.get_answer_distribution()
    answer = m.answer
    print(answer)

    # simulate a student random filling of answers
    rng = default_rng(seed)
    student_ans = rng.choice([0,1,2,3], size=45)
    print(student_ans)
    
    score = m.get_score(student_ans)
    print(score)