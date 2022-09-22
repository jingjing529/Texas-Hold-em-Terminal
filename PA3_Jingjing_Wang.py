import random
import itertools
import argparse
import csv
from pathlib import Path


class GameClass:

    def __init__(self):
        self.threshold = 8
        self.money_pool = 0
        self.bet = 1
        self.count = 0
        self.monster_money = 3 * self.bet
        self.good_money = 2 * self.bet
        self.decent_money = self.bet



    def create_player_class(self):
        """Create input number of players' classes."""
        self.all_player_class = []
        for x in range(5):
            self.all_player_class.append(PlayerClass(name="Player" + str(x + 1)))
        self.user_class = PlayerClass(name="*Human*") #add an additional class for user
        self.all_player_class.append(self.user_class)


    def initialize(self):
        """Initialize a game."""
        self.count += 1
        print(f"\n——————Initialize Game {self.count}————————")
        self.reset_whole_game()
        self.display_user_cards()
        self.smart_bot_init()
        self.display_community_cards()
        self.Round_1()


    def reset_whole_game(self):
        """Reset and initialize everything."""
        self.reset_deck_cards()
        self.reset_community_card()
        self.reset_in_hand_cards()
        self.each_round_player_class()
        self.money_pool = 0
        self.player_still_play = True
        self.has_monster = False


    def reset_deck_cards(self):
        """Create a deck of cards."""
        self.deck_cards = []
        for x in range(1, 14):
            self.deck_cards.append("S" + str(x))
            self.deck_cards.append("H" + str(x))
            self.deck_cards.append("D" + str(x))
            self.deck_cards.append("C" + str(x))


    def reset_community_card(self):
        """Initialize community cards."""
        self.community_card = [self.random_card(), self.random_card(), self.random_card()]
        self.update_player_communityCards()


    def update_player_communityCards(self):
        """Update community card to player end."""
        for player in self.all_player_class:
            player.community_card = self.community_card


    def reset_in_hand_cards(self):
        """Initialize the two in-hand cards for each player."""
        for player in self.all_player_class:
            player.own_card = [self.random_card(), self.random_card()]


    def random_card(self):
        """Randomly generate cards."""
        self.chosen_card = random.choice(self.deck_cards)
        self.deck_cards.remove(self.chosen_card)
        return self.chosen_card


    def each_round_player_class(self):
        """Get the player class for each round, convenient for removing the plyaers who fold."""
        self.round_player_class = self.all_player_class[:]


    def display_user_cards(self):
        """Display only user's in-hand cards."""
        print(f"Your card is: {','.join(self.user_class.own_card)}.")


    def user_decision(self):
        """Ask for user's decision about fold, check or bet."""
        while True:
            try:
                self.decision = input("please take your action.\nChoose between f(fold)/b(bet)/c(check)\n")
                if self.decision == "f" or self.decision == "F":
                    self.round_player_class.pop()
                    self.player_still_play = False
                    break
                elif self.decision == "b" or self.decision == "c" or self.decision == "B" or self.decision == "C":
                    if self.decision == "b" or self.decision == "B":
                        self.user_bet = int(input("How much do you want to bet?\n"))
                        if self.user_bet <= 0 or self.user_bet > (self.user_class.money):
                            raise ValueError
                        else:
                            self.user_class.money -= self.user_bet
                            self.money_pool += self.user_bet
                            print(f"{self.user_class.name}: bet ${self.user_bet}")
                    else:
                        print(f"{self.user_class.name}: check")
                    break
                else:
                    raise ValueError
            except ValueError:
                print("You input in invalid, please try again.")


    def display_community_cards(self):
        """Display community cards."""
        print(f"Community Cards: {','.join(self.community_card)}")


    def Round_1(self):
        """Start Round 1."""
        print("——————Round 1————————")
        self.players_init_rank()
        self.smart_bot()
        if self.player_still_play == True:
            self.user_decision()
        self.check_player_number()


    def players_init_rank(self):
        """Get players' ranks for the first round."""
        for player in self.all_player_class:
            player.get_init_rank()


    def smart_bot_init(self):
        self.bad_card_player = 0
        for player in self.round_player_class[:-1]:
            self.hand_number = set([int(num[1:]) for num in player.own_card])
            self.judge = self.judge_init()
            if self.judge is None:
                self.bad_card_player += 1
                if self.bad_card_player < 3 or self.has_monster == True:
                    print(f"{player.name}: fold")
                    self.round_player_class.remove(player)
                elif self.bad_card_player == 3:
                    print(f"{player.name}: bad bet ${self.bet}")
                    player.money -= self.bet
                    self.money_pool += self.bet
                else:
                    print(f"{player.name}: zha bet ${self.monster_money}")
                    player.money -= self.monster_money
                    self.money_pool += self.monster_money #诈唬

            else:
                print(f"{player.name}: bet ${self.judge}")
                player.money -= self.judge
                self.money_pool += self.judge


    def judge_init(self):
        if self.hand_number in [{1}, {1, 13}, {13}, {12}]:
            self.has_monster = True
            return self.monster_money
        elif self.hand_number in [{11}, {10}, {9}, {1, 12}, {1, 11}, {1, 10}, {13, 12}]:
            return self.good_money
        elif len(self.hand_number) == 1 or ({1} in self.hand_number) or (
                (sorted(list(self.hand_number))[1] - sorted(list(self.hand_number))[0]) == 1):
            return self.decent_money
        else:
            return None


    def smart_bot(self):
        """Display bot user's action about fold, check or bet."""
        self.bad_rank_player = 0
        if self.user_class in self.round_player_class:
            bots = self.round_player_class[:-1]
        else:
            bots = self.round_player_class
        for player in bots: # except user, which is the last index
            if player.rank > self.threshold:
                self.bad_rank_player += 1
                if self.bad_rank_player < len(self.round_player_class) - 1:
                    print(f"{player.name}: fold")
                    self.round_player_class.remove(player)
                else:
                    if player.money >= 2 * self.bet:
                        print(f"{player.name}: zha bet ${2 * self.bet}")
                        player.money -= 2 * self.bet
                        self.money_pool += 2 * self.bet
                    else:
                        print(f"{player.name}: bet ${player.money}")
                        self.money_pool += player.money
                        player.money = 0
            elif player.rank == self.threshold or player.money == 0:
                print(f"{player.name}: check")
                self.bad_rank_player += 1
            else:
                if player.rank > 5:
                    self.should_bet = self.bet
                elif player.rank > 3:
                    self.should_bet = 2 * self.bet
                elif player.rank > 1:
                    self.should_bet = 3 * self.bet
                if player.money >= self.should_bet:
                    print(f"{player.name}: bet ${self.should_bet}")
                    player.money -= self.should_bet
                    self.money_pool += self.should_bet
                else:
                    print(f"{player.name}: bet ${player.money}")
                    self.money_pool += player.money
                    player.money = 0


    def check_player_number(self):
        """Check how many player left."""
        if len(self.round_player_class) == 1:
            self.win_name = self.round_player_class[0].name
            self.game_over()
        else:
            self.Round_2()


    def game_over(self):
        """Ask the user whether keep on playing."""
        print(f"——————End of Game {self.count}————————")
        if len(self.all_player_class) == 1:
            print("There's no player left, game ends.")
        elif self.user_class.money <= 0:
            print("You don't have any money left for the next round, game ends.")
        else:
            while True:
                try:
                    self.response = input("Do you want to play again?\nPlease input Y or y for yes, N or n for no.\n")
                    if self.response == "Y" or self.response == "y":
                        print("You decide to start a new game.")
                        self.initialize()
                        break
                    elif self.response == "N" or self.response == "n":
                        print("You decide to quit the game.")
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please only enter Y, y or N, n")


    def Round_2(self):
        """Start Round 2."""
        print("——————Round 2————————")
        self.update_community_card()
        self.display_community_cards()
        self.smart_bot()
        if self.player_still_play == True:
            self.user_decision()
        self.player_get_best_comb()
        self.Result()


    def update_community_card(self):
        """Add two additional community cards during round 2."""
        self.community_card.append(self.random_card())
        self.community_card.append(self.random_card())
        self.update_player_communityCards()


    def player_get_best_comb(self):
        """Get the best combination card for each player."""
        for player in self.round_player_class:
            player.get_update_data()


    def Result(self):
        """Display results."""
        self.all_player_data_round2()
        self.final_summary()
        self.display_final_result()
        self.check_if_broke()
        self.game_over()


    def check_if_broke(self):
        """Check if any of the players don't have any more money to bet for the next round."""
        print("——————Quitting Info————————")
        self.length_class = len(self.all_player_class)
        for player in self.all_player_class[:-1]:
            if player.money <= 0:
                print(f"{player.name} broke.")
                self.all_player_class.remove(player)
        if len(self.all_player_class) == self.length_class:
            print("Nobody quits.")


    def all_player_data_round2(self):
        """Get all players' data after second round for the final comparison."""
        self.all_cards = []
        self.numbers = []
        self.ranks = []
        for player in self.round_player_class:
            self.all_cards.append(player.organized_card)
            self.numbers.append(player.number)
            self.ranks.append(player.rank)
        self.final_rankclass = RankClass(self.all_cards, self.all_cards, self.numbers, self.ranks)
        self.final_win_index = self.final_rankclass.get_win_index()


    def final_summary(self):
        """Get winner name and get every player's current money."""
        print("——————Results————————")
        self.winner_class = [self.round_player_class[index] for index in self.final_win_index]
        if self.user_class in self.winner_class :
            print("Congrats, you win!")
        elif self.user_class in self.round_player_class:
            print("Sorry but you lost.")
        self.winner = ",".join([win.name for win in self.winner_class])
        print("Winner:", self.winner)
        print("——————Game Statics————————")
        for player in self.round_player_class:
            if player in self.winner_class:
                self.split_money = self.money_pool / len(self.winner_class)
                if self.split_money.is_integer():
                    player.money += int(self.split_money)
                else:
                    player.money += float(self.split_money)


    def display_final_result(self):
        """Display final result."""
        for player in self.all_player_class:
            print(f"{player.name} {','.join(player.own_card)} ${player.money} {player.organized_card}")


class PlayerClass:


    def __init__(self, name: str = '', own_card: list = [], community_card: list = [], money: int = 10):
        self.name = name
        self.own_card = own_card
        self.community_card = community_card
        self.money = money
        self.rank = None
        self.organized_card = None


    def get_init_rank(self):
        """Get the rank for the first round"""
        self.init_card = self.own_card + self.community_card
        self.init_rankclass = RankClass(cards=self.init_card)
        self.init_rankclass.OrganizeData()
        self.init_rankclass.only_numbers()
        self.rank = self.init_rankclass.card_rank()


    def get_update_data(self):
        """Get the rank for the second round and the best combination card to pass on to the comparison."""
        self.all_cards = self.own_card + self.community_card
        self.all_combinations = list(itertools.combinations(self.all_cards, 5))
        self.combination_rankclass = RankClass(cards=self.all_combinations)
        self.combination_rankclass.separate_cards_combinations()
        self.combination_rankclass.get_best_combination()
        self.organized_card = self.combination_rankclass.best_card
        self.number = self.combination_rankclass.best_number
        self.rank = self.combination_rankclass.best_rank


class RankClass:


    def __init__(self, cards: list = [], organized: list = [], numbers: list = [], ranks: list = []):
        self.cards = cards
        self.card = cards
        self.organized = organized
        self.numbers = numbers
        self.ranks = ranks


    def OrganizeData(self):
        """Organize the cards by the order of the number on the cards for each player."""
        if len(self.card[0]) == 1:
            self.card = self.card[1:] #for file mode, when the first index in the list is the player's number
        for i in range(len(self.card)):
            if self.card[i][1:] == '1':
                self.card[i] = self.card[i][0] + '14'  # change 1 to 14 to make sort easier
        self.card.sort(key=lambda x: int(x[1:]))# sort by the number in the cards


    def only_numbers(self):
        """Get only the number of each player's card."""
        self.OnlyNum = []
        for each_card in self.card:
            self.OnlyNum.append(int(each_card[1:]))


    def separate_cards_combinations(self):
        """Separate each combination and put them in list to get the best combination."""
        self.organized = []
        self.numbers = []
        self.ranks = []
        for card in self.cards:
            self.card = list(card)
            self.OrganizeData()
            self.only_numbers()
            self.organized.append(self.card)
            self.numbers.append(self.OnlyNum)
            self.ranks.append(self.card_rank())


    def get_best_combination(self):
        """Get the best combination."""
        self.best_index = self.get_win_index()
        self.best_card = self.organized[self.best_index[0]]
        self.best_number = self.numbers[self.best_index[0]]
        self.best_rank = self.ranks[self.best_index[0]]  # though it's very unlikely to have two sets of cards share the same rank, but use list just to be safe


    def card_rank(self):
        """Get the rank of the current card."""
        self.max_frequency = self.OnlyNum.count(
            max(self.OnlyNum, key=self.OnlyNum.count))  # check the highest frequency of a card appeared
        self.min_frequency = self.OnlyNum.count(
            min(self.OnlyNum, key=self.OnlyNum.count))  # check the lowest frequency of a card appeared
        if self.check_if_flush():
            if set(self.OnlyNum) == {10, 11, 12, 13, 14}:
                # Royal flush
                return 0
            elif self.OnlyNum[-1] - self.OnlyNum[0] == 4:
                # Since the number is in order and there will not be two same numbers share the same suit so if the last - the first = 4 then it's a straight flush
                return 1
            else:
                # Flush
                return 4
        else:
            if self.max_frequency == 4:
                # if there are four cards that share the same number, then it's four of a kind
                return 2
            elif self.max_frequency == 3:
                # if there are three cards that share the same number
                if self.min_frequency == 2:
                    # and if the other two also has the same number, then it's full house
                    return 3
                else:
                    # if the other two has different numbers, it's three of a kind
                    return 6
            elif self.max_frequency == 1 and self.OnlyNum[-1] - self.OnlyNum[0] == 4:
                # if every number is different and the difference between the first and last card is 4, then it's straight
                return 5
            elif self.OnlyNum.count(self.OnlyNum[1]) == 2 and self.OnlyNum.count(self.OnlyNum[3]) == 2:
                # no matter how to format the card, the second and the forth card is always double. Such as [2,2,3,4,4], [2,2,3,3,4],[2,3,3,4,4]
                # so if the second and forth card is double, then it's two pairs
                return 7
            elif self.max_frequency == 2:
                # Pairs
                return 8
            else:
                # Highcard
                return 9


    def check_if_flush(self):
        """Check if all the cards have the same suit."""
        if self.card[0][0] == self.card[1][0] == self.card[2][0] == self.card[3][0] == self.card[4][0]:
            return True


    def get_win_index(self):
        """Determine who has the smallest rank and highest number to be the winner."""
        self.winRank = min(self.ranks)  # find the lowest rank (highest score)
        self.PW_nums = []
        if self.ranks.count(self.winRank) == 1:  # if there is only one winner rank, there is only 1 winner
            return [self.ranks.index(self.winRank)]
        else:  # [0,1,2]
            self.P_Winners = [i for i, x in enumerate(self.ranks) if
                              x == self.winRank]  # the potential winner indexes, since index + 1 is the player id, so this is a list to store ids
            for P_Winner in self.P_Winners:  # P_Winner is the index (which is also id -1) of each potential winner
                self.ReorderNum = self.numbers[P_Winner]
                self.ReorderNum.reverse()
                # if the card is [2,2,3,4,4], it will become [4,4,3,2,2]
                self.ReorderNum = sorted(self.ReorderNum, key=self.ReorderNum.count, reverse=True)
                # sort the number by their count, the example above will become [4,4,2,2,3]
                self.PW_nums.append(self.ReorderNum)
            for i in range(5):  # each player has 5 cards, so the index is 0-4
                self.each_card = [x[i] for x in self.PW_nums]
                # compare each set of card from the biggest to the smallest, based on the sorted order of ReorderNum (compare the largest count's number first and then single number)
                if self.each_card.count(
                        max(self.each_card)) == 1:  # if one person have the largest number, then that player id is the winner
                    self.winners = self.P_Winners[self.each_card.index(max(self.each_card))]
                    return [self.P_Winners[self.each_card.index(max(self.each_card))]]
                else:  # if there are multiple sets of cards share the same largest number, we need to compare their second largest number, etc.
                    self.remove_index = []
                    for i in range(len(self.each_card)):
                        if self.each_card[i] != max(self.each_card):
                            self.remove_index.append(i)
                    self.PW_nums = [self.PW_nums[i] for i in range(len(self.PW_nums)) if i not in self.remove_index]
                    self.P_Winners = [self.P_Winners[i] for i in range(len(self.P_Winners)) if
                                      i not in self.remove_index]
        # if there are multiple player/cards that has the same cards' numbers, then they are tied
        return [index for index in self.P_Winners]


class FileClass:


    def __init__(self, case_dire: str = ""):
        self.case_dic = {}
        self.result_dic = {}
        self.run_dic = {}
        self.case_dire = case_dire
        self.path_dire = Path(self.case_dire)
        self.count = 0
        self.read_path()
        self.result_func()
        self.compare_files()


    def compare_files(self):
        """Compare the output of program with the result in file."""
        for file_name in self.case_dic:
            self.player_card = RankClass(cards=self.case_dic[file_name])
            self.player_card.separate_cards_combinations()
            self.player_card.get_best_combination()
            self.run_dic[file_name] = ",".join([str(i) for i in self.player_card.best_index])
            if self.run_dic[file_name] == self.result_dic[file_name]:
                self.count += 1
            else:
                print(file_name)
        print(self.count)


    def read_path(self):
        """Read the file path."""
        for x in self.path_dire.iterdir():
            if x.is_dir():
                self.path_list = Path(x).glob('*.txt')
                for path in self.path_list:
                    self.Path = path
                    self.path_name = str(path)
                    self.OnlyTxt = self.path_name[self.path_name.rindex("/") + 1:]
                    self.case_dic[self.OnlyTxt] = self.read_file()


    def result_func(self):
        """Create a result dictionary with the program output result as value."""
        self.result_list = Path(self.path_dire).glob('*.txt')
        for result in self.result_list:
            with open(result) as file:
                self.reader = csv.reader(file)
                self.content = list(self.reader)
                for every in self.content:
                    self.result_dic[every[0]] = ",".join(every[1:]) #if there are multiple tie


    def read_file(self):
        """Read the cvs file and return the content in the file."""
        with open(self.Path) as f:
            self.single_reader = csv.reader(f)
            self.single_content = list(self.single_reader)
            while [] in self.single_content:
                self.single_content.remove([])
        return self.single_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true')
    parser.add_argument('-p', type=int)
    parser.add_argument('-f', action='store_true')
    parser.add_argument('-i', type=str)
    args = parser.parse_args()
    if args.u:
        Game = GameClass(args.p)
        Game.create_player_class()
        Game.initialize()
    elif args.f:
        FileClass(args.i)
