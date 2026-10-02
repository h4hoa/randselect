import random

from randselect.data import name_list, questions
from randselect.selector import random_selection


def main():
    rng = random.Random()
    while True:
  
        resp = input("Press 'Y' to continue, any other key to exit:")

        if resp.upper() != 'Y':
           break
        else:
            chosen_name, chosen_question = random_selection(name_list, questions, rng=rng)

        print(f"\n{chosen_name}, please answer: {chosen_question}\n") 