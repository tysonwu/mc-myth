import pandas as pd
import numpy as np
from numpy.random import default_rng

from tqdm import tqdm

from exam import Exam
from student import Student


def get_student_ability(seed, simulation_seed):
    rng = default_rng(seed+simulation_seed)
    knowledge_level = rng.uniform(0.5, 1)
    attempt_level = rng.uniform(0.25, 1)
    attempt_succeed_level = rng.uniform(0.1, 0.6)
    return knowledge_level, attempt_level, attempt_succeed_level

def main():
    # test the functionalities
    simulation_seed = 2022

    exam_seed = 2021
    exam = Exam(exam_seed)

    n_students = 10_000_000

    informed_scores = np.empty(n_students)
    informed_scores[:] = np.nan

    random_scores = np.empty(n_students)
    random_scores[:] = np.nan

    kls = np.empty(n_students)
    kls[:] = np.nan

    als = np.empty(n_students)
    als[:] = np.nan

    asls = np.empty(n_students)
    asls[:] = np.nan

    for n in tqdm(range(n_students)):
        knowledge_level, attempt_level, attempt_succeed_level = get_student_ability(seed=n, simulation_seed=simulation_seed)
        student = Student(n, knowledge_level, attempt_level, attempt_succeed_level)
        informed_ans, random_ans = student.attempt(exam)

        # calculate score
        informed_scores[n] = exam.get_score(informed_ans)
        random_scores[n] = exam.get_score(random_ans)

        # mark their metadata
        kls[n] = knowledge_level
        als[n] = attempt_level
        asls[n] = attempt_succeed_level

    # print(f'{informed_ans=}')
    # print(f'{random_ans=}')
    # print(f'{exam.answer=}')

    # print(f'{informed_score=}')
    # print(f'{random_score=}')
    mean_informed_scores = np.mean(informed_scores)
    mean_random_scores = np.mean(random_scores)

    print(f'{mean_informed_scores=}')
    print(f'{mean_random_scores=}')

    df = pd.DataFrame({'kl': kls, 'al': als, 'asl': asls, 'informed_score': informed_scores, 'random_score': random_scores})
    df.to_csv('df.csv', index=False)

if __name__ == '__main__':
    main()