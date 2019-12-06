import random as rand
import numpy as np

class Team:
    def __init__(self, id, elo=1000):
        self.id = id
        self.elo = elo
    def __repr__(self):
        return f'Team {self.id} (elo: {self.elo})'

class Round(Team):
    def __init__(self, *teams):
        self.teams = teams[0]
        self.matches = []
        self.winners = []

    def make_matches(self):
        '''after seeding we make matches where teams are paired with 
        the team half of the distribution away
        for example: the highest rated team is paired with the middle one
        '''
        num = int(len(self.teams)/2)
        for i in range(num):
            self.matches.append([self.teams[i], self.teams[i + num]])

    def seed(self):
        '''sorts the teams from highest elo to lowest'''
        self.teams.sort(key=lambda team: team.elo, reverse = True)

    def Prob_of_winning(self, match):
        '''prob of team 1 beating team 2 based on elo'''
        elo1 = match[0].elo
        elo2 = match[1].elo
        prob = 1 / (1 + 10**((elo2 - elo1)/400))
        return prob

    def find_winner(self, match):
        if rand.random() > self.Prob_of_winning(match):
            self.winners.append(match[1])
        else:
            self.winners.append(match[0]) 


class Tournament(Round):
    def __init__(self, n, min_elo, max_elo):
        self.teams=[]
        self.teams_per_round = []
        self.min_elo = min_elo
        self.team_count = 2**n
        self.max_elo = max_elo
    # creates 2^n teams with elo from flat distribution (min_elo, max_elo)
    def make_teams_flat_dist(self):
        rand_elos = [rand.randrange(self.min_elo, self.max_elo) for i in range(self.team_count)]
        rand_elos.sort(reverse=True)
        self.teams = [Team(i, rand_elos[i]) for i in range(self.team_count)]
        self.teams_per_round = [(0, self.teams)]

    def do_round(self, round_num, teams):
        the_round = Round(teams)   
        the_round.seed()
        the_round.make_matches()
        for match in the_round.matches:
            the_round.find_winner(match)
        return self.teams_per_round.append((round_num, the_round.winners))

    def get_champ(self):
        teams = self.teams_per_round[-1][-1]
        while len(teams) > 1:
            i = 1 # round number
            self.do_round(i, teams)
            i += 1
            teams = self.teams_per_round[-1][-1]
        return teams

# how often does the highest elo team win?
def proportion_of_highest(testN=10000, teamN=3, min_elo=500, max_elo=1500):
    winners = np.zeros(testN, dtype='int8')
    highest_count = 0
    for i in range(testN):
        tourney = Tournament(teamN, min_elo, max_elo)
        tourney.make_teams_flat_dist()
        winner = tourney.get_champ()[0].id
        winners[i] = winner
        if winner == 0:
            highest_count += 1
    return highest_count / testN

print(proportion_of_highest())
