import random as rand
import numpy as np


class Team:
    '''Teams are just an id and and elo'''
    def __init__(self, n, elo=1000):
        self.id = n
        self.elo = elo

    def __repr__(self):
        return f'Team {self.id} (elo: {self.elo})'


class Round(Team):
    def __init__(self, teams):
        self.teams = teams
        self.matches = []
        self.winners = []

    def make_matches(self):
        ''' just pairs the teams as given'''
        matches = []
        for i in range(0, len(self.teams), 2):
            matches.append((self.teams[i], self.teams[i + 1]))
        self.matches = matches

    def seed(self):
        '''sorts the teams so that they are paired such that
        teams 1-4 should make it to the semi-finals
        teams 1-8 to the quarter finals etc.
        '''
        sorted_teams = sorted(self.teams, key=lambda team: team.elo,
                              reverse=True)
        # start with the expect finals then work backwards every round adding
        # as many teams as we had before
        # When adding the new teams they the best new team should be paired
        # with the worst existing team
        # example: for 4 teams we should have [1, 4, 2, 3]
        # for an 8 team then we are adding teams 5, 6 ,7 8
        # team 5 is paired with 4, 6 with 3, etc.
        matches = [sorted_teams[0], sorted_teams[1]]
        while len(matches) < len(sorted_teams):
            temp_team_list = sorted(matches, key=lambda team: team.elo)
            temp_list = []
            num_teams = len(matches)
            team_list = sorted_teams[num_teams: int(num_teams * 2)]
            for match in matches:
                temp_list.append(match)
                temp_list.append(team_list[temp_team_list.index(match)])
            matches = temp_list
        self.teams = matches

    def prob_of_winning(self, match):
        '''prob of team 1 beating team 2 based on elo'''
        elo1 = match[0].elo
        elo2 = match[1].elo
        prob = 1 / (1 + 10**((elo2 - elo1) / 400))
        return prob

    def find_winner(self, match):
        if rand.random() > self.prob_of_winning(match):
            self.winners.append(match[1])
        else:
            self.winners.append(match[0])


class Tournament(Round):
    def __init__(self, n=3, min_elo=500, max_elo=1500, teams=[]):
        self.teams = teams
        self.teams_per_round = []
        self.min_elo = min_elo
        self.team_count = 2**n
        self.max_elo = max_elo

    def make_teams_flat_dist(self):
        rand_elos = [rand.randrange(self.min_elo, self.max_elo)
                     for i in range(self.team_count)]
        rand_elos.sort(reverse=True)
        self.teams = [Team(i, rand_elos[i]) for i in range(self.team_count)]
        self.teams_per_round = [(0, self.teams)]

    def do_round(self, round_num, teams, seed=False):
        the_round = Round(teams)
        if seed:
            the_round.seed()
        the_round.make_matches()
        for match in the_round.matches:
            the_round.find_winner(match)
        self.teams_per_round.append((round_num, the_round.winners))

    def do_tourney(self):
        i = 1
        while len(self.teams_per_round[-1][-1]) > 1:
            if i == 1:
                self.do_round(i, self.teams_per_round[-1][-1], seed=True)
            else:
                self.do_round(i, self.teams_per_round[-1][-1])
            i += 1


# how often does the highest elo team win?
def proportion_of_highest(testN=10000, teamN=3, min_elo=500, max_elo=1500):
    winners = np.zeros(testN, dtype='int8')
    highest_count = 0
    for i in range(testN):
        tourney = Tournament(teamN, min_elo, max_elo)
        tourney.make_teams_flat_dist()
        tourney.do_tourney()
        winner = tourney.teams_per_round[-1][-1][-1].id
        winners[i] = winner
        if winner == 0:
            highest_count += 1
    return highest_count / testN

if __name__ == '__main__':
    print(proportion_of_highest())