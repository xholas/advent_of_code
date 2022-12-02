from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


OpponentShape = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS,
}

ExpectedResult = {
    'X': Result.LOSS,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}


def get_response(shape_opponent, expected_result):
    # For draw choose the same shape
    if expected_result == Result.DRAW:
        return shape_opponent
    # For win choose the shape one above opponents (modulo 3)
    if expected_result == Result.WIN:
        s = (shape_opponent.value + 1) % 3
        s = 3 if s == 0 else s
        return Shape(s)
    # For loss select the shape one below opponents (modulo 3)
    else:
        s = (shape_opponent.value - 1) % 3
        s = 3 if s == 0 else s
        return Shape(s)


def play_round(shape_opponent, shape_response):
    if shape_opponent == shape_response:
        return Result.DRAW

    # Rock 1, Paper 2, Scissors 3, (Rock 4, ...)
    # You win if you play the shape one above the other
    # If you play the shape two points above then the other is one above you
    # this is "modulo-like" design of the game

    # You are one above, if you - opponent = 1
    diff = shape_response.value - shape_opponent.value
    if diff % 3 == 1:
        return Result.WIN
    else:
        return Result.LOSS


def main():
    with open('input_day_02.txt') as file_in:
        points_total = 0
        for line in file_in:
            # Get the shape and expected result from line
            a, b = line.split()
            shape_opponent = Shape(OpponentShape[a])
            expected_result = Result(ExpectedResult[b])
            # print("Opponent plays: " + shape_opponent.name + " and result should be: " + expected_result.name)
            # Find correct response
            shape_response = get_response(shape_opponent, expected_result)
            # print("Response should be: " + shape_response.name)
            # Points for my shape
            points_shape = int(shape_response.value)
            # print("\tPoints for shape (" + shape_response.name + "): " + str(points_shape))
            # Points for the round result
            r = play_round(shape_opponent, shape_response)
            points_result = int(Result(r).value)
            # print("\tPoints for round result (" + Result(r).name + "): " + str(points_result))
            # Sum of points for round:
            points_sum = points_shape + points_result
            # print("\tPoints for round: " + str(points_sum))
            # Total points
            points_total += points_sum
        print("Total points: " + str(points_total))


if __name__ == '__main__':
    main()
