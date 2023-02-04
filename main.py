import random
import time
import numpy
import matplotlib.pyplot as plt
import numpy as np

random.seed(40)


class RandomAgent:
    def __init__(self):
        self.numbers = []

    def act(self, vector: list):
        if random.random() > 0.5:
            self.numbers.append(vector[0])
            return vector[1:]
        self.numbers.append(vector[-1])
        return vector[:-1]


class GreedyAgent:
    def __init__(self):
        self.numbers = []

    def act(self, vector: list):
        if vector[0] > vector[-1]:
            self.numbers.append(vector[0])
            return vector[1:]
        self.numbers.append(vector[-1])
        return vector[:-1]


class NinjaAgent:
    """   ⠀⠀⠀⠀⠀⣀⣀⣠⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠴⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠠⠶⠶⠶⠶⢶⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⠀⠀⠀⢀⣴⣶⣶⣶⣶⣶⣶⣦⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⠀⣸⣿⡿⠟⠛⠛⠋⠉⠉⠉⠁⠀⠀⠀⠈⠉⠉⠉⠙⠛⠛⠿⣿⣿⡄⠀
⠀⠀⠀⠀⣿⠋⠀⠀⠀⠐⢶⣶⣶⠆⠀⠀⠀⠀⠀⢶⣶⣶⠖⠂⠀⠀⠈⢻⡇⠀
⠀⠀⠀⠀⢹⣦⡀⠀⠀⠀⠀⠉⢁⣠⣤⣶⣶⣶⣤⣄⣀⠀⠀⠀⠀⠀⣀⣾⠃⠀
⠀⠀⠀⠀⠘⣿⣿⣿⣶⣶⣶⣾⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣷⣶⣾⣿⣿⡿⠀⠀
⠀⠀⢀⣴⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⣾⡿⢃⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
⠀⢸⠏⠀⣿⡇⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀
⠀⠀⠀⢰⣿⠃⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⠛⠛⣉⣁⣤⡶⠁⠀⠀⠀⠀⠀
⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀
                かかって来い! """
    def __init__(self):
        self.numbers = []

    def act(self, vector: list):
        if len(vector) % 2 == 0:
            left = sum(vector[::2])
            right = sum(vector) - left
            if left >= right:
                self.numbers.append(vector[0])
                return vector[1:]
            self.numbers.append(vector[-1])
            return vector[:-1]
        else:
            left = max(sum(vector[1::2]), sum(vector[2::2]))
            right = max(sum(vector[:-1:2]), sum(vector[:-2:2]))
            if left >= right:
                self.numbers.append(vector[-1])
                return vector[:-1]
            self.numbers.append(vector[0])
            return vector[1:]


def check_power_of_diagram(diagram_index, sum_of_powers=0):
    for power in range(50):
        sum_of_powers += 2 ** power
        if sum_of_powers >= diagram_index:
            return power


class MinMaxAgent:
    def __init__(self, max_depth=50):
        self.numbers = []
        self.max_depth = max_depth

    def minmax(self, vector, actual_depth=1, which_way=1):
        if len(vector) == 1:
            return [vector[0] * which_way, False]
        elif actual_depth == self.max_depth:
            if which_way == 1:
                if vector[0] > vector[-1]:
                    return [vector[0], True]
                else:
                    return [vector[-1], False]
            elif which_way == -1:
                if vector[0] > vector[-1]:
                    return [-vector[-1], False]
                else:
                    return [-vector[0], True]

        value_of_left_branch = self.minmax(vector[1:], actual_depth + 1, which_way * -1)[0]
        value_of_right_branch = self.minmax(vector[:-1], actual_depth + 1, which_way * -1)[0]

        value_of_left_branch += which_way * vector[0]
        value_of_right_branch += which_way * vector[-1]
        if which_way == 1:
            if value_of_right_branch > value_of_left_branch:
                return [value_of_right_branch, False]
            else:
                return [value_of_left_branch, True]
        else:
            if value_of_right_branch > value_of_left_branch:
                return [value_of_left_branch, True]
            else:
                return [value_of_right_branch, False]

    def act(self, vector: list):
        turn = self.minmax(vector)
        if turn[1]:
            self.numbers.append(vector[0])
            return vector[1:]
        self.numbers.append(vector[-1])
        return vector[:-1]


def run_game(vector, first_agent, second_agent):
    while len(vector) > 0:
        vector = first_agent.act(vector)
        if len(vector) > 0:
            vector = second_agent.act(vector)


def main():
    sum_time = 0
    list_of_points_p1 = np.array([])
    list_of_points_p2 = np.array([])
    glebokosc_drzewa = 1

    for _ in range(500):
        vector = [random.randint(-10, 10) for _ in range(15)]
        first_agent, second_agent = MinMaxAgent(glebokosc_drzewa), NinjaAgent()
        start_time = time.time()
        run_game(vector, first_agent, second_agent)
        sum_time += time.time() - start_time
        list_of_points_p1 = np.insert(list_of_points_p1, len(list_of_points_p1), sum(first_agent.numbers))
        list_of_points_p2 = np.insert(list_of_points_p2, len(list_of_points_p2), sum(second_agent.numbers))

        vector = [random.randint(-10, 10) for _ in range(15)]
        first_agent, second_agent = MinMaxAgent(glebokosc_drzewa), NinjaAgent()
        start_time = time.time()
        run_game(vector, second_agent, first_agent)
        sum_time += time.time() - start_time
        list_of_points_p1 = np.insert(list_of_points_p1, len(list_of_points_p1), sum(first_agent.numbers))
        list_of_points_p2 = np.insert(list_of_points_p2, len(list_of_points_p2), sum(second_agent.numbers))

    avg_time = sum_time/1000
    avg_score_p1 = sum(list_of_points_p1)/1000
    avg_score_p2 = sum(list_of_points_p2)/1000

    print(f"średni czas gry: {avg_time}\n"
          f"średnia suma punktów gracza1: {round(avg_score_p1, 2)} \n"
          f"średnie odchylenie standardowe gracza1: {round(list_of_points_p1.std(), 2)}\n"
          f"średnia suma punktów gracza2: {round(avg_score_p2, 2)} \n"
          f"średnie odchylenie standardowe gracza2: {round(list_of_points_p2.std(), 2)}\n")

    # histogram_player1(list_of_points_p1)
    # histogram_player2(list_of_points_p2)

    # print(f"First agent: {sum(first_agent.numbers)} Second agent: {sum(second_agent.numbers)}\n"
    #       f"First agent: {first_agent.numbers}\n"
    #       f"Second agent: {second_agent.numbers}")


def histogram_player1(list_of_points):
    plt.hist(list_of_points, bins=100, range=(-50, 50), color="gray")
    plt.title("Player's 1 score distribution")
    plt.ylabel('Number of results')
    plt.xlabel('Sum of points')
    plt.show()


def histogram_player2(list_of_points):
    plt.hist(list_of_points, bins=100, range=(-50, 50), color="red")
    plt.title("Player's 2 score distribution")
    plt.ylabel('Number of results')
    plt.xlabel('Sum of points')
    plt.show()


if __name__ == "__main__":
    main()
