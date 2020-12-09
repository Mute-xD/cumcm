import resources
res = resources.Resources()


class ProblemA:
    def __init__(self):
        self.MapA = res.map1
        self.costingList = res.costingList
        self.weather = res.weather1
        self.start = '1'
        self.end = '27'
        self.village = '15'
        self.mine = '12'
        self.itemNeeded = [0, 0]  # food, water
        self.weightList = [3, 2]
        self.priceList = [5, 10]
        self.itemTaken = [0, 0]
        self.currentMoney = 10000
        self.date = 0
        self.currentPosition = None

    def routeFinder(self, graph, start, end, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start is end:
            return path
        shortestPath = []
        for node in graph[start]:
            if node not in path:
                newPath = self.routeFinder(graph, node, end, path)
                if newPath:
                    if not shortestPath or len(newPath) < len(shortestPath):
                        shortestPath = newPath
        return shortestPath

    def buyer(self, water, food, free=False, home=False):
        self.itemTaken[0] += water
        self.itemTaken[1] += food
        if not free:
            if home:
                self.currentMoney -= water * 5
                self.currentMoney -= food * 10
            else:
                self.currentMoney -= water * 10
                self.currentMoney -= food * 20

    def walker(self, path, dest):
        self.currentPosition = path.__next__()
        while self.currentPosition is not dest:
            self.date += 1
            currentWeather = self.weather[self.date - 1]
            if currentWeather is 2:
                print('Storm !')
                self.itemTaken[0] -= 10
                self.itemTaken[1] -= 10
            elif currentWeather is 1:
                self.currentPosition = next(path)
                self.itemTaken[0] -= 16
                self.itemTaken[1] -= 12
            else:
                self.currentPosition = next(path)
                self.itemTaken[0] -= 10
                self.itemTaken[1] -= 14
            # print('Current Position:', self.currentPosition, ' item', self.itemTaken, ' Day:', self.date)

    def directCost(self):
        directPath = self.routeFinder(self.MapA, self.start, self.end)
        print(directPath)
        directDistance = len(directPath) - 1
        weatherList = self.weather[:directDistance]
        self.itemNeeded = [0, 0]
        for day in range(directDistance):
            weather = weatherList[day]
            if weather is not 2:
                self.itemNeeded[0] += self.costingList[weather][0] * 2
                self.itemNeeded[1] += self.costingList[weather][1] * 2
            else:
                directDistance += 1
                self.itemNeeded[0] += self.costingList[weather][0]
                self.itemNeeded[1] += self.costingList[weather][1]
        moneyNeeded = self.itemNeeded[0] * self.priceList[0] + self.itemNeeded[1] * self.priceList[1]
        weightNeeded = self.itemNeeded[0] * self.weightList[0] + self.itemNeeded[1] * self.weightList[1]
        print('MoneyNeeded:', moneyNeeded, '\nWeightNeeded', weightNeeded)
        print(self.itemNeeded)

    def MineAndBack(self):
        # 证明满载是必要的
        self.buyer(240, 240, home=True)
        print('Money:', self.currentMoney)
        pathToVillage = self.routeFinder(self.MapA, self.start, self.village).__iter__()
        self.walker(pathToVillage, self.village)
        self.buyer()
        villageToMine = self.routeFinder(self.MapA, self.village, self.mine).__iter__()
        self.walker(villageToMine, self.mine)
        while self.date <= 25:
            self.date += 1
            currentWeather = self.weather[self.date - 1]
            if currentWeather is 2:
                self.itemTaken[0] -= 10
                self.itemTaken[1] -= 10
                # self.currentMoney += 1000
            elif currentWeather is 1:
                self.currentMoney += 1000
                self.itemTaken[0] -= 24
                self.itemTaken[1] -= 18
            else:
                self.currentMoney += 1000
                self.itemTaken[0] -= 15
                self.itemTaken[1] -= 21
            if self.itemTaken[0] <= 40 or self.itemTaken[1] <= 40:  # TODO Check This
                print('leave', self.itemTaken)
                break
            print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        print('Stop Mining!', self.itemTaken, 'Day:', self.date)
        print('-'*50)
        mineToVillage = self.routeFinder(self.MapA, self.mine, self.village).__iter__()
        self.walker(mineToVillage, self.village)
        self.buyer(0, 0)
        villageToEnd = self.routeFinder(self.MapA, self.village, self.end).__iter__()
        self.walker(villageToEnd, self.end)
        print('END', self.currentMoney, self.itemTaken)


if __name__ == '__main__':

    problemA = ProblemA()
    # problemA.directCost()
    print('---------------------------------------------------------------------------')
    problemA.MineAndBack()
