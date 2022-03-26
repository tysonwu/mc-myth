from collections import Counter

import numpy as np
from numpy.random import default_rng

from exam import Exam

class Student:

    def __init__(self, seed: int, knowledge_level: float, attempt_level: float, attempt_correct_level: float):
        '''
        Model a student by setting two param:
        knowledge_level [0,1]: the probability of the student exactly knowing the answer
        attempt_level: the probability of the student attempting a question with doubt
        attempt_correct_level: the probability of the student attempting a question with doubt and yet answering correctly
        '''
        self.seed = seed
        self.rng = default_rng(seed)
        self.kl = knowledge_level
        self.al = attempt_level
        self.acl = attempt_correct_level


    def attempt(self, exam: Exam):
        # init answer sheet with nan
        answer_sheet = np.empty(exam.N_QUESTIONS)
        answer_sheet[:] = np.nan
        self.answer_sheet = answer_sheet

        # fill in the answer sheet
        self._answer_questions(exam)

        # answering un-attempted question
        # in informed way
        informed_answers, without_informed_answers = self._answer_unattempted_questions(exam)
        return informed_answers, without_informed_answers


    def _answer_questions(self, exam: Exam):
        
        # first, attempt the questions
        for i in range(len(self.answer_sheet)):
            
            kp = self.rng.uniform(0, 1)
            ap = self.rng.uniform(0, 1)
            acp = self.rng.uniform(0, 1)

            if self.kl > kp:
                # student knows the answer for sure
                self.answer_sheet[i] = exam.answer[i]
            else:
                # student is in doubt
                if self.al > ap:
                    # student attempts the question
                    if self.acl > acp:
                        # student attempts the question and is correct
                        self.answer_sheet[i] = exam.answer[i]
                    else:
                        # student attempts the question but is wrong
                        true_ans = exam.answer[i]
                        self.answer_sheet[i] = self.rng.choice([i for i in [0,1,2,3] if i != true_ans], size=1)
                else:
                    # student does not attempt the question
                    # leave the answer as nan
                    pass


    def _answer_unattempted_questions(self, exam: Exam):

        # attempt the question in "smart" way means that
        # the student incorporates the count of mc choices in current answer sheet
        # making up the choice of filling unattempted answer with 0/1/2/3
        # action separated in part A and B
        # in case of a tie, randomly chooses one

        answered_counter_part_a = Counter([i for i in self.answer_sheet[:exam.N_QUESTIONS_A] if not np.isnan(i)])
        answered_counter_total = Counter([i for i in self.answer_sheet if not np.isnan(i)])

        if answered_counter_part_a:
            # in case counter is empty ie. no questions attempted at all
            minimum_part_a = min(answered_counter_part_a, key=answered_counter_part_a.get)
        else:
            minimum_part_a = self.rng.choice([0,1,2,3], size=1)[0]

        if answered_counter_total:
            minimum_total = min(answered_counter_total, key=answered_counter_total.get)
        else:
            minimum_total = self.rng.choice([0,1,2,3], size=1)[0]
        
        informed_answer_sheet = np.copy(self.answer_sheet)
        without_informed_answer_sheet = np.copy(self.answer_sheet)

        # what if informed
        for i, ans in enumerate(informed_answer_sheet):
            if np.isnan(ans):
                # filling in unattempted question
                informed_answer_sheet[i] = minimum_part_a if i < exam.N_QUESTIONS_A else minimum_total

        # what if not informed - randomly chooses answer
        for i, ans in enumerate(without_informed_answer_sheet):
            if np.isnan(ans):
                # filling in unattempted question by random fill
                without_informed_answer_sheet[i] = self.rng.choice([0,1,2,3], size=1)[0]
        
        return informed_answer_sheet, without_informed_answer_sheet