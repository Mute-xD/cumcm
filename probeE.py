import resources
import probeA

res = resources.Resources()


class Player:
    def __init__(self, label):
        self.label = label
        self.position = None
        self.item = [0, 0]
        self.money = 10000
        self.date = 0
        self.target = None


class ProblemE(probeA.ProblemA):
    def __init__(self):
        super().__init__()
        self.Map5 = res.map3
        self.start = '1'
        self.end = '13'
        self.mine = '9'
        self.weather = res.weather2
        self.playerA = Player('AAA')
        self.playerB = Player('BBB')

    def playerWalker(self, player, path, dest, heatStop=False):
        player.position = path.__next__()
        while player.position is not dest:
            player.date += 1
            currentWeather = self.weather[player.date - 1]
            if currentWeather is 2:
                print('Storm !')
                player.item[0] -= 10
                player.item[0] -= 10
            elif currentWeather is 1 and not heatStop:
                player.position = next(path)
                player.item[0] -= 18
                player.item[1] -= 18
            elif currentWeather is 1 and heatStop:
                player.item[0] -= 9
                player.item[1] -= 9
            else:
                player.position = next(path)
                player.item[0] -= 6
                player.item[1] -= 8
            print(player.label, 'Current Position:', player.position, ' item', player.item, ' Day:', player.date)

    def routeFinderB(self, graph, start, end, path=None, avoid=None):
        if path is None:
            path = []
        path = path + [start]
        if start is end:
            return path
        shortestPath = []
        for node in graph[start]:
            if node not in avoid:
                if node not in path:
                    newPath = self.routeFinder(graph, node, end, path)
                    if newPath:
                        if not shortestPath or len(newPath) < len(shortestPath):
                            shortestPath = newPath
            else:
                pass
        return shortestPath

    @staticmethod
    def playerBuyer(player, water, food, free=False, home=False):
        player.item[0] += water
        player.item[1] += food
        if not free:
            if home:
                player.money -= water * 5
                player.money -= food * 10
            else:
                player.money -= water * 10
                player.money -= food * 20

    def miner(self, player, leaveDate=float('inf')):
        while True:
            player.date += 1
            weather = self.weather[player.date - 1]
            if weather is 2:
                player.money += 200
                player.item[0] -= 30
                player.item[1] -= 30
            elif weather is 1:
                player.money += 200
                player.item[0] -= 27
                player.item[1] -= 27
            else:
                player.money += 200
                player.item[0] -= 9
                player.item[1] -= 12
            if player.date >= leaveDate:  # TODO check
                break
            print(player.label, 'Mining', player.item, 'Day:', player.date, ' Money:', player.money)
        print(player.label, 'Stop Mining!', player.item, 'Day:', player.date)

    def planA(self):
        bPathToEnd = self.routeFinder(self.Map5, self.start, self.end).__iter__()
        self.playerWalker(self.playerB, bPathToEnd, self.end, heatStop=False)
        aPathToMine = self.routeFinder(self.Map5, self.start, self.mine).__iter__()
        aMineToEnd = self.routeFinder(self.Map5, self.mine, self.end).__iter__()
        self.playerBuyer(self.playerA, 0, 0, home=True)
        self.playerWalker(self.playerA, aPathToMine, self.mine, heatStop=False)
        self.miner(self.playerA, 4)
        self.playerWalker(self.playerA, aMineToEnd, self.end, heatStop=False)
        self.playerBuyer(self.playerA, -self.playerA.item[0], -self.playerA.item[1], home=True)
        self.playerBuyer(self.playerB, -self.playerB.item[0], -self.playerB.item[1], home=True)
        print('PlayerA END', self.playerA.item, 'Money:', self.playerA.money)
        print('PlayerB END', self.playerB.item, 'Money:', self.playerB.money)

    def planB(self):
        aPathToEnd = self.routeFinder(self.Map5, self.start, self.end)
        bPathToEnd = self.routeFinder(self.Map5, self.start, self.end)
        # daily update
        update = len(aPathToEnd)
        self.playerA.position = self.start
        self.playerB.position = self.start
        for i in range(1, update):
            self.playerA.date += 1
            self.playerB.date += 1
            self.playerA.target = aPathToEnd[i]
            self.playerB.target = bPathToEnd[i]
            if self.playerB.position == self.playerA.position and self.playerB.target == self.playerA.target:
                if self.weather[self.playerA.date] is 1:
                    self.playerA.item[0] -= 36
                    self.playerA.item[1] -= 36
                    self.playerB.item[0] -= 36
                    self.playerB.item[1] -= 36
                else:
                    self.playerA.item[0] -= 12
                    self.playerA.item[1] -= 16
                    self.playerB.item[0] -= 12
                    self.playerB.item[1] -= 16
            else:
                if self.weather[self.playerA.date] is 1:
                    self.playerA.item[0] -= 18
                    self.playerA.item[1] -= 18
                    self.playerB.item[0] -= 18
                    self.playerB.item[1] -= 18
                else:
                    self.playerA.item[0] -= 6
                    self.playerA.item[1] -= 8
                    self.playerB.item[0] -= 6
                    self.playerB.item[1] -= 8
            self.playerA.position = self.playerA.target
            self.playerB.position = self.playerB.target
            print('AAA', self.playerA.position, 'BBB', self.playerB.position)
            self.playerBuyer(self.playerA, -self.playerA.item[0], -self.playerA.item[1], home=True)
            self.playerBuyer(self.playerB, -self.playerB.item[0], -self.playerB.item[1], home=True)
            print('Money', self.playerA.money, self.playerB.money)
    def planC(self):
        pass


if __name__ == '__main__':
    probeE = ProblemE()
    probeE.planA()
    probeE_ = ProblemE()
    print('-------------------------------------------------------------------------------------------------')
    probeE_.planB()
