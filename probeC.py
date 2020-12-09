import probeA
import resources
import random
res = resources.Resources()


class ProblemC(probeA.ProblemA):
    def __init__(self):
        super().__init__()
        self.mapC = res.map3
        self.weather = None
        self.start = '1'
        self.mine = '9'
        self.end = '13'
        self.currentMoney = 10000
        self.cost = None

    def createWeather(self, point):
        weather = []
        for i in range(10):
            rand = random.random()
            if rand < point:
                weather.append(0)
            if rand > point:
                weather.append(1)
        self.weather = weather
        # print('Weather:', self.weather)

    @staticmethod
    def heavyWeatherCost(days):
        # print('Item Backup', 18 * days)
        return 18 * days

    def plan(self, a, b):
        self.buyer(a, b, home=True)
        self.cost = self.heavyWeatherCost(3)
        pathToMine = self.routeFinder(self.mapC, self.start, self.mine).__iter__()
        pathToEnd = self.routeFinder(self.mapC, self.start, self.end).__iter__()
        mineToEnd = self.routeFinder(self.mapC, self.mine, self.end).__iter__()

        # Full load TODO Why?
        # self.buyer(240, 240, home=True)
        self.walker(pathToMine, self.mine)
        while True:
            self.date += 1
            currentWeather = self.weather[self.date - 1]

            if currentWeather is 1:
                self.currentMoney += 200
                self.itemTaken[0] -= 27
                self.itemTaken[1] -= 27
            else:
                self.currentMoney += 200
                self.itemTaken[0] -= 9
                self.itemTaken[1] -= 12
            if self.itemTaken[0] <= self.cost or self.itemTaken[1] <= self.cost or self.date >= 8:  # TODO ???
                break

            # print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        # print('Stop Mining!', self.itemTaken, 'Day:', self.date)
        self.walker(mineToEnd, self.end)
        print('END', self.currentMoney, self.itemTaken)
        return self.itemTaken, self.currentMoney


if __name__ == '__main__':
    water = 0
    food = 0
    maxMoney = 0
    moneySum = 0
    for _ in range(1000):
        probC = ProblemC()
        probC.createWeather(0.6)

        if _ is 0:
            ret, maxMoney = probC.plan(0, 0)
        else:
            ret, money = probC.plan(water, food)
            moneySum += money
            water += - ret[0]
            food += - ret[1]
            if money > maxMoney:

                maxMoney = money

    print('-------', water, food, maxMoney, moneySum/1000)
