
import string
import json
import random
from enum import Enum, auto
from collections import defaultdict

from typing import (
    List,
    Dict,
    Tuple
)

from jill_box.game import GameGateway, Room, StartReturnCodes, InteractReturnCodes


def _load_prompts() -> List[Tuple[str, str]]:
    prompts :List[Tuple[str, str]] = []
    with open('jill_box/data/questions.txt') as fd:
        for line in fd.readlines():
            prompts.append(tuple(line.split('\t')))
    return prompts


class TestRoom(Room):

    class State(Enum):
        WAITING_TO_START = 'WAITING_TO_START'
        COLLECTING_ANSWERS = 'COLLECTING_ANSWERS'
        VOTING = 'VOTING'
        SHOWING_RESULTS = 'SHOWING_RESULTS'

    ROUNDS = 3 

    CORRECT_KEY = "~!~ø~!~"

    PROMPTS = _load_prompts()
  
    def __init__(self):
        super().__init__()
        
        self.prompts = random.sample(TestRoom.PROMPTS, TestRoom.ROUNDS)
        self.state = TestRoom.State.WAITING_TO_START
        self.round = 0
        self.answers: Dict[str, str] = {}
        self.votes: Dict[str, str] = {}
        self.vote_orders: Dict[str, List[str]] = {}
        self.scores: Dict[str, int] = defaultdict(int)
        self.confirmed: Dict[str, bool] = {}

    def start(self) -> StartReturnCodes:
        if self.state != TestRoom.State.WAITING_TO_START:
            return StartReturnCodes.ALREADY_STARTED
        if len(self.players) < 3:
            return StartReturnCodes.TOO_FEW_PLAYERS
        self.state = TestRoom.State.COLLECTING_ANSWERS
        return StartReturnCodes.SUCCESS


    def get_prompt(self) -> str:
        return self.prompts[self.round][0]

    def get_anwers(self, user) -> List[str]:
        if user is None:
            return random.sample(list(self.answers.values()), len(self.answers))
        else:
            return [ self.answers[p] for p in self.vote_orders[user] ]
    
    def __start_voting(self):
        self.state = TestRoom.State.VOTING
        self.answers[TestRoom.CORRECT_KEY] = self.prompts[self.round][1]
        for player in self.players:
            other_players = [ k for k in self.answers.keys() if k != player ]
            self.vote_orders[player] = random.sample(other_players, len(other_players))

    def __show_results(self):
        self.state = TestRoom.State.SHOWING_RESULTS
        new_scores = self.__votes_to_score()
        for name, score in new_scores.items():
            self.scores[name] += score

    def __votes_to_score(self):
        scores = { u:0 for u in self.players }
        for player, vote in self.votes.items():
            if vote in scores:
                scores[vote] += 1
            else:
                scores[player] += 1
        return scores

    def __next_round(self):
        self.round += 1
        if self.round < TestRoom.ROUNDS:
            self.state = TestRoom.State.COLLECTING_ANSWERS
            self.answers: Dict[str, str] = {}
            self.votes: Dict[str, str] = {}
            self.vote_orders: Dict[str, List[str]] = {}
            self.confirmed: Dict[str, bool] = {}
        else:
            pass


    def submit_data(self, player, data) -> InteractReturnCodes:
        try:
            if self.state == TestRoom.State.COLLECTING_ANSWERS:
                self.answers[player] = data['answer'].upper()
                if len(self.answers) == len(self.players):
                    self.__start_voting()
            elif self.state == TestRoom.State.VOTING:
                vote = int(data['vote'])
                self.votes[player] = self.vote_orders[player][vote]
                if len(self.votes) == len(self.players):
                    self.__show_results()
            elif self.state == TestRoom.State.SHOWING_RESULTS:
                self.confirmed[player] = True
                if len(self.confirmed) == len(self.players):
                    self.__next_round()
            else:
                return InteractReturnCodes.WRONG_STATE
            return InteractReturnCodes.SUCCESS
        except:
            return InteractReturnCodes.INVALID_DATA

    def get_room_state(self, player) -> Tuple[InteractReturnCodes, str, str]:
        if self.state == TestRoom.State.COLLECTING_ANSWERS:
            return (InteractReturnCodes.SUCCESS, self.state, self.get_prompt())
        elif self.state == TestRoom.State.VOTING:
            answers = json.dumps(self.get_anwers(player))
            return (InteractReturnCodes.SUCCESS, self.state, answers)
        elif self.state == TestRoom.State.SHOWING_RESULTS:
            ret = json.dumps({'answer': self.prompts[self.round][1],'earned': self.__votes_to_score(), 'total': self.scores})
            return (InteractReturnCodes.SUCCESS, self.state, ret)
        return (InteractReturnCodes.WRONG_STATE, self.state, '')

def main():
    gateway = GameGateway()

    room = gateway.new_game(TestRoom)

    name1 = "tester1"
    name2 = "tester2"
    name3 = "tester3"

    print(gateway.join_room(room, name1))
    print(gateway.join_room(room, name2))
    print(gateway.join_room(room, name3))

    print(gateway.room_start(room))

    print(gateway.get_room_state(room))

    print(gateway.submit_data(room, name1, {'answer': 'A'}))
    print(gateway.submit_data(room, name2, {'answer': 'B'}))
    print(gateway.submit_data(room, name3, {'answer': 'C'}))

    print(gateway.get_room_state(room))
    print(gateway.get_room_state(room, name2))

    print(gateway.submit_data(room, name1, {'vote': '1'}))
    print(gateway.submit_data(room, name2, {'vote': '0'}))
    print(gateway.submit_data(room, name3, {'vote': '1'}))

    print(gateway.get_room_state(room))

    print(gateway.submit_data(room, name1, {}))
    print(gateway.submit_data(room, name2, {}))
    print(gateway.submit_data(room, name3, {}))


    print(gateway.get_room_state(room))

    print(gateway.submit_data(room, name1, {'answer': 'A2'}))
    print(gateway.submit_data(room, name2, {'answer': 'B2'}))
    print(gateway.submit_data(room, name3, {'answer': 'C2'}))

    print(gateway.get_room_state(room))
    print(gateway.get_room_state(room, name2))

    print(gateway.submit_data(room, name1, {'vote': '0'}))
    print(gateway.submit_data(room, name2, {'vote': '0'}))
    print(gateway.submit_data(room, name3, {'vote': '1'}))

    print(gateway.get_room_state(room))

if __name__ == "__main__":
    main()
