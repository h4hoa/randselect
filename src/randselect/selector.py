import random

def remaining(items, used=()):
  # Items not yet in `used`, keeping their original order.
  return [item for item in items if item not in used]


def random_selection(n_list, q_list, rng=random, used_names=(), used_questions=()):
  # Pick one name and one question, skipping anything in used_names/used_questions.
  names = remaining(n_list, used_names)
  qs = remaining(q_list, used_questions)
  if not names or not qs:
    raise ValueError("No names or questions left to choose from.")

  chosen_name = rng.choice(names)
  chosen_question = rng.choice(qs)

  return (chosen_name, chosen_question)
