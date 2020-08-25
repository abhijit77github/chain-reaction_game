import json
import time

import tornado.ioloop
import tornado.web
import tornado.websocket

import os
from game_manager import GameManager

'''from .game_manager import GameManager '''

APP_DIR = os.path.dirname(os.path.realpath(__file__))
settings = {
    "template_path": os.path.join(APP_DIR, "templates"),
    "static_path": os.path.join(APP_DIR, "static")
   
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


        
        
class SocketHandler(tornado.websocket.WebSocketHandler):
    
    def initialize(self, game_manager, *args, **kwargs):
        """Initialize game parameters.  Use Game Manager to register game
        """
        self.game_manager = game_manager
        self.game_id = None
        super().initialize(*args, **kwargs)

    def open(self):
        """Opens a Socket Connection to client
        """
        print(" client connected")
        self.send_message("message", message="Connected to Game Server")

    def on_message(self,message):
        """Respond to messages from connected client.
        Messages are of form -
        {
            action: <action>,
            <data>
        }
        Valid Actions: new, join, start, abort, move.
        new - Request for new game
        join - Join an existing game (but that's not been paired)
        abort - Abort the game currently on
        move - Record a move
        """


    
        
        
    
        data = json.loads(message)
        action = data.get("action", "")
        print(action,data.get("data"))
        if action == "move":
            # Game is going on
            # Set turn to False and send message to opponent
            player_selection = data.get("player_move")
            print(player_selection)
            player_move = (int(player_selection[0]), int(player_selection[1]))
            if player_move:
                self.game_manager.record_move(self.game_id, player_move, self)
          
            # Check if the game is still ON
            if self.game_manager.has_game_ended(self.game_id):
                #game_result = self.game_manager.get_game_result(self.game_id, self)
                self.game_manager.result(self.game_id)
                print("game ended")

               

        elif action == "join":
            # Get the game id
            try:
                game_id = int(data.get("game_id"))
                self.game_manager.join_game(game_id, self)
            except (ValueError, TypeError):
                self.send_message(action="error", data="Invalid Game Id: {}".format(data.get("game_id")))
            else:
                # Joined the game.
                self.game_id = game_id
                # Tell both players that they have been paired, so reset the pieces
                self.send_message("paired", game_id=game_id)
                self.send_message("color", user=self.game_manager.get_index(self.game_id,self))
                self.game_manager.msg_all(game_id,"paired")
                #self.send_pair_message(action="paired", game_id=game_id)
                # One to wait, other to move
                #self.send_message(action="opp-move")
                #self.send_pair_message(action="move")

        elif action == "new":
            # Create a new game id and respond the game id
            self.game_id = self.game_manager.new_game(self)
            self.send_message("created", game_id=self.game_id)
            self.send_message("color", user=self.game_manager.get_index(self.game_id, self))
        elif action == "start":
            self.game_manager.start(self.game_id)
            self.send_message(action="started", data="started")
            self.send_message(action="turn")
        elif action == "ping":
            pass

        elif action == "abort":
            self.game_manager.abort_game(self.game_id)
            self.game_manager.end_game(self.game_id)
        else:
            self.send_message(action="error", data="Unknown Action: {}".format(action))



      
    def on_close(self): 
        print("client disconnected")    

 
    def check_origin(self, origin):
        return True

    def send_message(self, action, **data):
        message = {
            "action": action,
            "data": data
        }
        try:
            self.write_message(json.dumps(message))
            
        except tornado.WebSocketClosedError:
            #logger.warning("WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            #self.send_pair_message(action="pair-closed")
            self.close()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

 
 
 
 
 
gameManager= GameManager()
 
        
urls=[
    (r"/", MainHandler),
    (r"/demo/ws", SocketHandler , dict(game_manager=gameManager)),



]

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app= tornado.web.Application(urls, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()