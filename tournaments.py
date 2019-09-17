import random as rand

class Team:
    def __init__(self, id, elo=1000, kval = 32):
        self.id = id
        self.elo = elo
        self.kval = kval
    def __repr__(self):
        return f'Team {self.id} (elo: {self.elo})'

class Round(Team):
    def __init__(self, *teams):
        self.teams = teams[0]
        self.matches = []
        self.winners = []
    
    def make_matches(self):
        num = int(len(self.teams)/2)
        for i in range(num):
            self.matches.append([self.teams[i], self.teams[i + num]])

    def seed(self):
        self.teams.sort(key=lambda team: team.elo, reverse = True)

    def Prob_of_winning(self, match):
        elo1 = match[0].elo
        elo2 = match[1].elo
        prob = 1 / (1 + 10**((elo2 - elo1)/400))
        return prob

    def find_winner(self, match):
        if rand.random() > self.Prob_of_winning(match):
            self.winners.append(match[1])
        else:
            self.winners.append(match[0]) 

# creates 2^n teams each with random elo between min_elo and max_elo 
def get_teams(n, min_elo, max_elo):
    teams = [Team(i, rand.randrange(min_elo, max_elo)) for i in range(2**n)]
    return teams

teams = get_teams(3, 500, 1500)

while len(teams) > 1:
    round = Round(teams)
    round.seed()
    round.make_matches()
    for match in round.matches:
        round.find_winner(match)
    teams = round.winners
print(teams)
