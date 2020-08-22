import tornado
from tornado.websocket import WebSocketClosedError

from chain import Chain
import json


class InvalidGameError(Exception):
    """Raised when Game is not in registry
    """
    pass


class GameManager(object):

    def __init__(self):
        """Records All Games in a Dictionary and create a sequence of game ids
        """
        self.games = {}
        self.max_game_id = 100

    def _get_next_game_id(self):
        """Returns next game id
        """
        if self.max_game_id > 100000:
            self.max_game_id = 100
        self.max_game_id += 1
        return self.max_game_id

    def new_game(self, handler):
        """Creates a new Game and returns the game id
        """
        game_id = self._get_next_game_id()
        self.games[game_id] = {
            "handlers": [handler]
        }
        game = self.get_game(game_id)
        game["chain"] = Chain()
        # code to send message to the client
        return game_id

    def join_game(self, game_id, handler):
        """Returns game_id if join is successful.
        Raises InvalidGame when it could not join the game
        """
        game = self.get_game(game_id)
        if handler not in game.get("handlers"):
            game["handlers"].append(handler)
            # code to send message to the client
            return game_id
        # Game ID not found.
        raise InvalidGameError

    def start(self, game_id):
        game = self.get_game(game_id)
        game["chain"].start(len(game["handlers"]))
        self.msg_all(game_id, "msg", data="Game started")

    def end_game(self, game_id):
        """Removes the Game from the games registry
        """
        if game_id in self.games:
            del self.games[game_id]

    def get_index(self, game_id, handler):
        """Returns the paired Handler
        """
        game = self.get_game(game_id)
        for i in range(len(game["handlers"])):
            if game["handlers"][i] == handler:
                return i

    def get_game(self, game_id):
        """Returns the game instance.  Raises Error when game not found
        """
        game = self.games.get(game_id)
        if game:
            return game
        raise InvalidGameError

    def msg_all(self, game_id, action, **data):
        message = {
            "action": action,
            "data": data
        }
        try:
            game = self.get_game(game_id)
            for handler in game["handlers"]:
                handler.write_message(json.dumps(message))

        except WebSocketClosedError:
            # logger.warning("WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            # self.send_pair_message(action="pair-closed")
            # self.close()
            pass

    def record_move(self, game_id, player_move, handler):
        game = self.get_game(game_id)
        for i in range(len(game["handlers"])):
            if game["handlers"][i] == handler:
                if game["chain"].pos_is_vallid(i,player_move):
                    next = game["chain"].play(i, player_move)
                    self.msg_all(game_id, "move", data={"user": i, "x": player_move[0], "y": player_move[1]})
                    if next != None:
                        next_plr = self.get_handler(game_id, next)
                        message = {
                            "action": "turn",
                        }
                        try:
                            next_plr.write_message(json.dumps(message))
                        except WebSocketClosedError:
                            # logger.warning("WS_CLOSED", "Could Not send Message: " + json.dumps(message))
                            # Send Websocket Closed Error to Paired Opponent
                            # self.send_pair_message(action="pair-closed")
                            # self.close()
                            pass
                else:
                    message = {
                        "action": "turn",
                    }
                    try:
                        handler.write_message(json.dumps(message))
                    except WebSocketClosedError:
                        pass


    def get_handler(self, game_id, index):
        game = self.get_game(game_id)
        return game["handlers"][index]

    def has_game_ended(self, game_id):
        game = self.get_game(game_id)
        result = game["chain"].is_game_ended()
        return result

    def result(self, game_id):
        game = self.get_game(game_id)
        result = game["chain"].result
        for i in range(len(game["handlers"])):
            if i == result:
                self.send_message(game["handlers"][i],"end", result="W")
            else:
                self.send_message(game["handlers"][i], "end", result="L")

        del(game)

    def send_message(self,handler, action, **data):
        message = {
            "action": action,
            "data": data
        }
        try:
            handler.write_message(json.dumps(message))

        except tornado.WebSocketClosedError:
            # logger.warning("WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            # self.send_pair_message(action="pair-closed")
            handler.close()


