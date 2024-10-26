from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

TRUE = Symbol("true statement")


baseKnowledge = And(
    # saying that every person must either be a knight or a knave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
)

# Puzzle 0
# A says "I am both a knight and a knave."
sentenceA = And(AKnight,AKnave)
knowledge0 = And(
    Implication(sentenceA, AKnight),
    Implication(Not(sentenceA), AKnave)
)
knowledge0.add(baseKnowledge)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentenceA = And(AKnave, BKnave)
knowledge1 = And(
    Biconditional(sentenceA, AKnight),

)
knowledge1.add(baseKnowledge)
# Puzzle 2
# A says "We are the same kind."
sentenceA = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
sentenceB = Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave)))
knowledge2 = And(
Biconditional(sentenceA, AKnight),
    Biconditional(sentenceB, BKnight),
)
knowledge2.add(baseKnowledge)
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentenceA = Or(AKnight, AKnave)
# B says "A said 'I am a knave'."
# B says "C is a knave."
sentenceB = And(CKnave, AKnave)
# C says "A is a knight."
sentenceC = AKnight

knowledge3 = And(
Biconditional(sentenceA, AKnight),
    Biconditional(Not(sentenceA), AKnave),
    Biconditional(sentenceB, BKnight),
    Biconditional(Not(sentenceB), BKnave),
    Biconditional(sentenceC, CKnight),
    Biconditional(Not(sentenceC), CKnave),
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
