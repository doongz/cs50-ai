from http.client import IM_USED
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Puzzle0_Asays = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),  # (A is a Knight) ∨  (A is a Knave)
    Implication(AKnight, Not(AKnave)),  # (A is a Knight) => (¬(A is a Knave))
    Implication(AKnave, Not(AKnight)),  # (A is a Knave) => (¬(A is a Knight))
    # (A is a Knight) => ((A is a Knight) ∧ (A is a Knave))
    Implication(AKnight, Puzzle0_Asays),
    # (A is a Knave) => (¬((A is a Knight) ∧ (A is a Knave)))
    Implication(AKnave, Not(Puzzle0_Asays))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Puzzle1_Asays = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave),  # A is only one of them
    Implication(AKnight, Not(AKnave)),  # if A is a Knight, then A is not Knave
    Implication(AKnave, Not(AKnight)),  # if A is a Knave, then A is not Knight

    Or(BKnight, BKnave),  # same above
    Implication(BKnight, Not(BKnave)),
    Implication(BKnight, Not(BKnave)),

    # if A is a Knight, then A says is true
    Implication(AKnight, Puzzle1_Asays),
    # if A is a Knave, then A says is not true
    Implication(AKnave, Not(Puzzle1_Asays))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Puzzle2_Asays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Puzzle2_Bsays = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),  # A is only one of them
    Implication(AKnight, Not(AKnave)),  # if A is a Knight, then A is not Knave
    Implication(AKnave, Not(AKnight)),  # if A is a Knave, then A is not Knight

    Or(BKnight, BKnave),  # same above
    Implication(BKnight, Not(BKnave)),
    Implication(BKnight, Not(BKnave)),

    # if A is a Knight, then A says is true
    Implication(AKnight, Puzzle2_Asays),
    # if A is a Knave, then A says is not true
    Implication(AKnave, Not(Puzzle2_Asays)),
    Implication(BKnight, Puzzle2_Bsays),  # same above
    Implication(BKnave, Not(Puzzle2_Bsays))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Puzzle3_Asays = Or(AKnight, AKnave)
Puzzle3_Bsays_0 = AKnave
Puzzle3_Bsays_1 = CKnave
Puzzle3_Csays = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),  # A is only one of them
    Implication(AKnight, Not(AKnave)),  # if A is a Knight, then A is not Knave
    Implication(AKnave, Not(AKnight)),  # if A is a Knave, then A is not Knight

    Or(BKnight, BKnave),  # same above
    Implication(BKnight, Not(BKnave)),
    Implication(BKnight, Not(BKnave)),

    Or(CKnight, CKnave),  # same above
    Implication(CKnight, Not(CKnave)),
    Implication(CKnight, Not(CKnave)),

    Implication(AKnight, Puzzle3_Asays),
    Implication(AKnave, Not(Puzzle3_Asays)),

    Implication(BKnight, Puzzle3_Bsays_0),
    Implication(BKnave, Not(Puzzle3_Bsays_0)),

    Implication(BKnight, Puzzle3_Bsays_1),
    Implication(BKnave, Not(Puzzle3_Bsays_1)),

    Implication(CKnight, Puzzle3_Csays),
    Implication(CKnave, Not(Puzzle3_Csays)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
