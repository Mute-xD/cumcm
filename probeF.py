import random
import resources
import numpy as np

res = resources.Resources()


class Player:
    def __init__(self, label):
        self.label = label
        self.position = [0, 0]
        self.target = None
        self.item = [0, 0]
        self.check = 0


playerA = Player('A')
playerB = Player('B')
playerC = Player('C')


class ProblemF:
    def __init__(self):

        self.date = 0
        self.space = np.zeros([5, 5])
        self.spaceShape = self.space.shape
        self.playerA = playerA
        self.playerB = playerB
        self.playerC = playerC
        self.start = [0, 0]
        self.end = [4, 4]
        self.village = [3, 2]
        self.mine = [2, 3]
        self.playerA.position = self.start
        self.playerB.position = self.start
        self.playerC.position = self.start
        self.weather = None

    @staticmethod
    def distance(target, current):
        currentX = current[0]
        currentY = current[1]
        targetX = target[0]
        targetY = target[1]
        # print([targetX - currentX, targetY - currentY])
        return [targetX - currentX, targetY - currentY]

    def createWeather(self, p1, p2):
        if p1 > p2:
            raise ValueError('p1 > p2')
        weather = []
        for i in range(30):
            rand = random.random()
            if rand < p1:
                weather.append(0)
            elif rand > p2:
                weather.append(2)
            else:
                weather.append(1)
        self.weather = weather
        print('Weather:', self.weather)

    def findNearby(self, x, y):
        nearby_list = [self.getCells(x + delta_x, y + delta_y)
                       for delta_x in [-1, 0, 1] for delta_y in [-1, 0, 1]
                       if not (delta_x is 0 and delta_y is 0) and (delta_x != delta_y)]
        return [i for i in nearby_list if i is not None]

    def getCells(self, x, y):
        if x < 0 or x > self.spaceShape[0] - 1 or y < 0 or y > self.spaceShape[1] - 1:
            return None
        else:
            return [x, y]

    def itemCounter(self, player):
        weather = self.weather[self.date - 1]
        if weather is 2:
            print('Storm!')
            player.item[0] -= 10
            player.item[1] -= 10
        elif weather is 1:
            player.item[0] -= 18
            player.item[1] -= 18
        else:
            player.item[0] -= 6
            player.item[1] -= 8
        print('player', player.label, 'pos:', player.position, 'item', player.item)

    def update(self):
        for i in range(2):
            self.date += 1
            self.step(self.playerB, self.mine)
            self.step(self.playerC, self.mine)
            self.step(self.playerA, self.mine)
            self.move(self.playerB)
            self.move(self.playerC)

    def step(self, player, dest):
        if player.position == dest:
            return
        player.target = player.position
        isMoved = False
        if self.weather[self.date - 1] is 2:
            self.itemCounter(player)
            return
        dist = self.distance(dest, player.position)
        if dist[0] != 0:
            player.target[0] += (dist[0] / abs(dist[0]))
            isMoved = True
        if not isMoved:
            if dist[1] != 0:
                player.target[1] += (dist[1] / abs(dist[1]))
            else:
                print('arrived')
        print('label:', player.label, player.target)

    def move(self, player):
        otherPlayer = [i for i in [self.playerA, self.playerB, self.playerC] if i is not player]
        # print(otherPlayer[0].label, otherPlayer[1].label)
        nearBy = self.findNearby(player.position[0], player.position[1])
        targets = [i.target for i in otherPlayer]
        # print(targets)
        if player.target not in targets:
            player.position = player.target
            # print('move to', player.position)
            self.itemCounter(player)
        else:
            for near in nearBy:
                if near not in targets:
                    player.position = near
                    # print('move to', player.position)
                    self.itemCounter(player)
                    break
                else:
                    print('wait')


if __name__ == '__main__':
    probeF = ProblemF()
    probeF.createWeather(0.4, 0.9)
    probeF.update()
    # playerA.check += 1
    # print(playerB.check)
