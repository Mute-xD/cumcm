import probeA
import resources
import random
import numpy as np
import matplotlib.pyplot as plt

res = resources.Resources()


class ProblemD(probeA.ProblemA):
    def __init__(self):
        super().__init__()
        self.mapD = res.map4
        self.start = [0, 0]
        self.end = [4, 4]
        self.village = [3, 2]
        self.mine = [2, 3]
        self.itemTaken = [0, 0]
        self.currentMoney = 10000
        self.date = 0
        self.currentPosition = [0, 0]
        self.space = np.zeros([5, 5])
        self.decisionCond = None
        self.killed = False

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

    def distance(self, target, current):
        if current is None:
            current = self.currentPosition
        currentX = current[0]
        currentY = current[1]
        targetX = target[0]
        targetY = target[1]
        # print([targetX - currentX, targetY - currentY])
        return [targetX - currentX, targetY - currentY]

    def cell(self):
        self.decisionCond = self.heavyWeatherCost(5)
        self.currentPosition = self.start
        self.itemTaken = [240, 240]
        self.currentMoney = 6400
        # start to mine
        self.runner(self.mine)
        self.miner()
        self.runner(self.village)
        self.itemTaken = [240, 240]
        if not self.killed:
            self.currentMoney -= 240 - self.itemTaken[0] * 10
            self.currentMoney -= 240 - self.itemTaken[1] * 20
        # TODO buy here
        print('-' * 50)
        self.currentMoney -= 0
        self.runner(self.mine)
        self.miner()
        self.runner(self.end)
        if self.killed is True:
            return None
        else:
            return self.currentMoney

    def runner(self, dest):
        while self.currentPosition is not dest:
            if self.killed:
                print('Killed In Action In Day:', self.date)
                break

            self.space[int(self.currentPosition[0])][int(self.currentPosition[1])] = 1
            self.date += 1
            isMoved = False
            if self.weather[self.date - 1] is 2:
                self.itemUpdate()
                return
            dist = self.distance(dest)
            if dist[0] != 0:
                self.currentPosition[0] += (dist[0] / abs(dist[0]))
                isMoved = True
            if not isMoved:
                if dist[1] != 0:
                    self.currentPosition[1] += (dist[1] / abs(dist[1]))
                else:
                    break
            self.itemUpdate()
            if self.date is 30 and self.currentPosition is not self.end:
                self.killed = True
                break
            self.space[int(self.currentPosition[0])][int(self.currentPosition[1])] = 2
            print('Current Pos:', self.currentPosition, 'Item:', self.itemTaken, 'Day:', self.date)
            self.UI()

    def miner(self):
        while True:
            if self.date is 30:
                self.killed = True
                break
            self.date += 1
            weather = self.weather[self.date - 1]
            if weather is 2:
                self.currentMoney += 1000
                self.itemTaken[0] -= 30
                self.itemTaken[1] -= 30
            elif weather is 1:
                self.currentMoney += 1000
                self.itemTaken[0] -= 27
                self.itemTaken[1] -= 27
            else:
                self.currentMoney += 1000
                self.itemTaken[0] -= 9
                self.itemTaken[1] -= 12
            if self.itemTaken[0] <= self.decisionCond or\
                    self.itemTaken[1] <= self.decisionCond or\
                    self.date >= 27:  # TODO check
                break
            print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        print('Stop Mining!', self.itemTaken, 'Day:', self.date)

    def itemUpdate(self):
        weather = self.weather[self.date - 1]
        if weather is 2:
            print('Storm!')
            self.itemTaken[0] -= 10
            self.itemTaken[1] -= 10
        elif weather is 1:
            self.itemTaken[0] -= 18
            self.itemTaken[1] -= 18
        else:
            self.itemTaken[0] -= 6
            self.itemTaken[1] -= 8
        if self.itemTaken[0] < 0:
            self.killed = True
        if self.itemTaken[1] < 0:
            self.killed = True

    @staticmethod
    def heavyWeatherCost(days):
        print('Item Backup', 18 * days)
        return 18 * days

    def UI(self):
        plt.title('Day:' + str(self.date))
        plt.imshow(self.space, cmap='Set3')
        plt.show()


if __name__ == '__main__':
    # surviveList = []
    # for _ in range(10000):
    #     probeD = ProblemD()
    #     probeD.createWeather(0.2, 0.7)
    #     surviveList.append(probeD.cell())
    #     print('***********************************************************************************\n\n')
    # surviveRate = 0
    # money = 0
    # for sample in surviveList:
    #     if sample is not None:
    #         money += sample
    #         surviveRate += 1
    # print('SurviveRate', surviveRate/len(surviveList))
    # print('AvgMoney', int(money/surviveRate))
    probeD = ProblemD()
    probeD.createWeather(0.4, 0.9)
    probeD.cell()
