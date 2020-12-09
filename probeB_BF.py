import probeA_BF
import resources

res = resources.Resources()


class ProblemB(probeA_BF.ProblemA):
    def __init__(self):
        super().__init__()
        self.MapB = res.map2
        self.weather = res.weather1
        self.start = '1'
        self.end = '64'
        self.villageA = '39'
        self.villageB = '62'
        self.mineA = '30'
        self.mineB = '55'
        self.itemTaken = [0, 0]
        self.currentMoney = 10000
        self.date = 0
        self.currentPosition = None

    def solve(self):
        # Full load
        self.buyer(240, 240, home=True)
        pathToMineA = self.routeFinder(self.MapB, self.start, self.mineA).__iter__()
        mineAToVillageA = self.routeFinder(self.MapB, self.mineA, self.villageA).__iter__()
        self.walker(pathToMineA, self.mineA)
        # print('-' * 50)
        while True:
            self.date += 1
            currentWeather = self.weather[self.date - 1]

            if currentWeather is 2:
                self.currentMoney += 1000
                self.itemTaken[0] -= 30
                self.itemTaken[1] -= 30
            elif currentWeather is 1:
                self.currentMoney += 1000
                self.itemTaken[0] -= 24
                self.itemTaken[1] -= 18
            else:
                self.currentMoney += 1000
                self.itemTaken[0] -= 15
                self.itemTaken[1] -= 21
            if self.itemTaken[0] <= 33 or self.itemTaken[1] <= 43:  # TODO Check This
                break
            print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        print('Stop Mining!', self.itemTaken, 'Day:', self.date)
        self.walker(mineAToVillageA, self.villageA)
        self.buyer(240 - self.itemTaken[0], 240 - self.itemTaken[1])
        # print('-' * 50)
        villageAToMineB = self.routeFinder(self.MapB, self.villageA, self.mineB).__iter__()
        self.walker(villageAToMineB, self.mineB)
        # # print('-' * 50)
        while self.date <= 29:
            self.date += 1
            currentWeather = self.weather[self.date - 1]

            if currentWeather is 2:
                self.currentMoney += 1000
                self.itemTaken[0] -= 30
                self.itemTaken[1] -= 30
            elif currentWeather is 1:
                self.currentMoney += 1000
                self.itemTaken[0] -= 24
                self.itemTaken[1] -= 18
            else:
                self.currentMoney += 1000
                self.itemTaken[0] -= 15
                self.itemTaken[1] -= 21
            if self.itemTaken[0] <= 32 or self.itemTaken[1] <= 24:  # TODO Check This
                break
            print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        print('Stop Mining!', self.itemTaken, 'Day:', self.date)
        mineBToVillageB = self.routeFinder(self.MapB, self.mineB, self.villageB).__iter__()
        # print('-' * 50)
        self.walker(mineBToVillageB, self.villageB)
        self.buyer(52, 42)
        villageBTOMineB = self.routeFinder(self.MapB, self.villageB, self.mineB).__iter__()
        self.walker(villageBTOMineB, self.mineB)
        while self.date <= 27:
            self.date += 1
            currentWeather = self.weather[self.date - 1]

            if currentWeather is 2:
                self.currentMoney += 1000
                self.itemTaken[0] -= 30
                self.itemTaken[1] -= 30
            elif currentWeather is 1:
                self.currentMoney += 1000
                self.itemTaken[0] -= 24
                self.itemTaken[1] -= 18
            else:
                self.currentMoney += 1000
                self.itemTaken[0] -= 15
                self.itemTaken[1] -= 21
            # if self.itemTaken[0] <= 32 or self.itemTaken[1] <= 24:  # TODO Check This
            #     break
            print('Mining', self.itemTaken, 'Day:', self.date, ' Money:', self.currentMoney)
        print('Stop Mining!', self.itemTaken, 'Day:', self.date)
        mineBTOEnd = self.routeFinder(self.MapB, self.mineB, self.end).__iter__()
        self.walker(mineBTOEnd, self.end)
        print('Money:', self.currentMoney, 'item', self.itemTaken, 'date', self.date)

    def routeFinder(self, graph, start, end, path=None):
        if start is self.start and end is self.villageA:
            return ['1', '9', '18', '26', '27', '28', '29', '30', '39']
        elif start is self.start and end is self.mineA:
            return ['1', '9', '18', '26', '27', '28', '29', '30']
        elif start is self.mineA and end is self.villageA:
            return ['30', '39']
        elif start is self.villageA and end is self.mineB:
            return ['39', '46', '55']
        elif start is self.mineB and end is self.end:
            return ['55', '63', '64']
        elif start is self.villageA and end is self.end:
            return ['39', '47', '56', '64']
        elif start is self.mineB and end is self.villageB:
            return ['55', '62']
        elif start is self.villageB and end is self.mineB:
            return ['62', '55']
        else:
            raise ValueError('Route not defined')


if __name__ == '__main__':
    prob = ProblemB()

    prob.solve()
