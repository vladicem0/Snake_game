import parameters
import functions
from game import game_loop


def level_1(menu) -> None:
    class Snake1(functions.Snake):
        print('level 1')

        @staticmethod
        def get_current_score(score: int) -> None:
            pass

        def win_condition(self) -> bool:
            if self.length == 2:
                return True

        def tick(self, food: list[tuple[int, int]]) -> None:
            self.head = (self.head[0] + self.speed[0], self.head[1] + self.speed[1])
            self.body.append((self.head, self.condition))

            if self.head in food:
                self.eat()
            else:
                del self.body[0]

    class Food1(functions.Food):
        def __init__(self, _):
            super().__init__(_)
            self.current_food = [(30*x, 30*x) for x in range(10, 20)]

        def get_food(self, obstacle: list[tuple[int, int]]) -> list[tuple[int, int]]:
            for block in obstacle:
                if block in self.current_food:
                    del self.current_food[self.current_food.index(block)]
            return self.current_food
    game_loop(menu, 'level_1.map', Snake1, Food1)


def level_2(menu) -> None:
    class Snake2(functions.Snake):
        print('level 2')

        def win_condition(self) -> bool:
            if self.length == 2:
                return True

    #class Food2(functions.Food):
    #    pass

    game_loop(menu, 'level_2.map', Snake2)


levels = {
    'level_1': level_1,
    'level_2': level_2,
}
