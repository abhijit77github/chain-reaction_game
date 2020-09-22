<template>
  <div class="hello" >
    <div class="row" v-if="!game_on">
       <div class="input-field col s6 m4" v-if="!paired">
          <i class="material-icons prefix">create</i>
          <input id="icon_prefix" type="text" class="validate">
          <label for="icon_prefix">Enter room no.</label>
        </div>
        <div class="col  " v-if="!paired">
          <button @click="join_room" class="waves-effect waves-light btn">Create/Join a Room</button>
        </div>
        <div class="col  " v-if="paired && !game_on && creator">
          <button @click="start_game" class="waves-effect waves-light btn">Start</button>
        </div>
    </div>
    <h5 id="demo">{{ msg }}</h5>
    

    <div class="row">

      <div class="col s12 m3">
        <!-- Grey navigation panel -->
        <div class="row" @click="show=!show" >
           <i class="small material-icons">touch_app</i><a>How to play</a>
        </div>
        <transition name="fade" > 
            <div class="row" v-if="show">
                <div class="col s12 m12">
                  <div class="card blue-grey darken-1">
                    <div class="card-content white-text">
                      <span class="card-title">Strategy</span>
                      <p>Your goal is to dominate over opponents area, by extinguishing others area(color). To win eleminate others.Making  a move 
                        in unstable position will cause a spread. </p>
                    </div>
                  
                  </div>
                </div>
              </div>
        </transition>
              
      </div>

      <div class="col s12 m6 ">
       <!-- Teal page content 
                <div class="row">
               <div class="col">
                  <a class=" btn-floating pulse" v-bind:class="crnt_cls"><i class="material-icons">menu</i></a>
                  <span>Now its your turn.</span>
               </div>
          </div>

                -->
           <div class="row ">
                 <div class="blue-grey lighten-2 box" >
                    <div class="row cst" v-for="(item,i) in arr_bx" :key="i" >
                      <Button v-on:btnpos="get_pos" v-for="(element,j) in item" :key="j" v-bind:cnt=element.cnt v-bind:nbr="element.nbr.length" v-bind:user="user_clr[element.col]" v-bind:posx="i" v-bind:posy="j" 
                      />
                    </div>  
                
                 </div>   

            </div>

            <div class="row">
                     <div class="col" v-if="turn">
                          <a class=" btn-floating pulse" v-bind:class="get_color()"><i class="material-icons">check_circle</i></a>
                          <span style="margin-left:10px">Now its your turn.</span>
                     </div>

            </div>
          


          </div>   
          

          
          
     
        
      
          <div class="col s12 m3">
          
          </div>

    </div>
     <footer class="page-footer teal darken-3">
          <div class="container">
            <div class="row">
              <div class="col l6 s12">
                <img src="/static/me.jpeg" height="70" style=" border-radius: 50%">
                <h5 class="white-text" style="font-family:Jazz LET, fantasy">About Developer</h5>
                <p class="grey-text text-lighten-4" style = "font-family:cursive">This fun game is devloped by Abhijit, to enjoy the fun of playing Populer offline 
                  game "ChainReaction" online with remote friends.</p>
              </div>
              <div class="col l5  s12">
                 <div>
                   <img src="/static/git_hub.png" height="60" width="60">
                    <a class="grey-text text-lighten-3" href="https://github.com/abhijit77github"><h5 class="white-text">Github Profile</h5></a>
                
                 </div>
                
                <div>
                  <a class="grey-text text-lighten-3 img_box" href="https://www.linkedin.com/in/abhijit-halder-410151b5"><img src="/static/linked_in.svg" height="60" width="60"></a>
                  <a class="grey-text text-lighten-3 img_box" href="#!"><img src="/static/insta_logo.svg" height="60" width="60"></a>
                  <a class="grey-text text-lighten-3 img_box" href="#!"><img src="/static/fb_logo.svg" height="60" width="60"></a>
                </div>

              
              </div>
            </div>
          </div>
          <div class="footer-copyright">
            <div class="container">
            © 2020 Copyright ,All Rights Rserved.
            </div>
          </div>
        </footer>
            
  </div>
</template>

<script>
import Button from './Button.vue'
export default {
  name: 'HelloWorld',
  components: {
    
    Button
  },
  props: {
    _msg: String
  },
 
  data(){
    return {
      connected : false,
      turn: false,
      game_finished:  false,
      server_msg: null,
      msg: "welcome",
      indx: null,
      user_clr:["grey","teal darken-3","pink darken-3","purple darken-4","deep-orange accent-4"],
      h:6,
      w:5,
      game_id: null,
      crnt_usr:1,
      game_on:false,
      creator: false,
      paired: false,
      show: false,
      socket:null,
      arr_bx : 
          [ 
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:1,x:0,y:1},{cnt: 0,col:0,id:3,x:0,y:2},{cnt: 0,col:0,id:4,x:0,y:3}],
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:10,x:1,y:0},{cnt: 0,col:0,id:11,x:1,y:1},{cnt: 0,col:0,id:12,x:1,y:2},{cnt: 0,col:0,id:13,x:1,y:3}],
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:1,x:0,y:1},{cnt: 0,col:0,id:3,x:0,y:2},{cnt: 0,col:0,id:4,x:0,y:3}],
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:10,x:1,y:0},{cnt: 0,col:0,id:11,x:1,y:1},{cnt: 0,col:0,id:12,x:1,y:2},{cnt: 0,col:0,id:13,x:1,y:3}],
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:1,x:0,y:1},{cnt: 0,col:0,id:3,x:0,y:2},{cnt: 0,col:0,id:4,x:0,y:3}],
            [{cnt: 0,col:0,id:0,x:0,y:0},{cnt: 0,col:0,id:10,x:1,y:0},{cnt: 0,col:0,id:11,x:1,y:1},{cnt: 0,col:0,id:12,x:1,y:2},{cnt: 0,col:0,id:13,x:1,y:3}],

            ],
      sound : null,

    }
  },
  methods: {
    /*
    btn_id : function(x,y){
      var arr=this.get_nbh(x,y);
    
    },   */
    get_nbh : function(x,y){
       var nbh=[];
       if(x-1>=0)
          nbh.push([x-1,y])
       if(x+1<this.h)
          nbh.push([x+1,y])
       if(y-1>=0)
          nbh.push([x,y-1])
       if(y+1<this.w)
          nbh.push([x,y+1])
       return nbh;

    },
    next_usr: function() {
      if(this.crnt_usr+1>2)
         this.crnt_usr=1;
      else
         this.crnt_usr+=1;
      
    },
    add_nbr: function(){
      var i,j;
      for( i=0;i<this.h; i++){
        for(j=0; j<this.w; j++){
          this.arr_bx[i][j].nbr= this.get_nbh(i,j)
        }
      }
     },
     move : function(user,x,y){
         this.move_sound.currentTime=0;
         this.move_sound.play();         
        function check_end(this_ref){
          var i,j;
          var lst=[];
          for(i=0;i<this_ref.h;i++){
            for(j=0;j<this_ref.w;j++){
              if(this_ref.arr_bx[i][j].col>0){
                if (!lst.includes(this_ref.arr_bx[i][j].col)){
                  lst.push(this_ref.arr_bx[i][j].col);
                }
              }

              }

            } 
            if(lst.length>1)
               return false;
            else if( lst.length ==1 )
               return true;
               
                
          }
        
        function over_flo(this_ref){
                     //sleep(200);
           flag=true;
           var new_arr=[];
           nbr.forEach(el => {                
                this_ref.arr_bx[el[0]][el[1]].cnt ++;
                this_ref.arr_bx[el[0]][el[1]].col = user +1;                
                if (this_ref.arr_bx[el[0]][el[1]].cnt >= this_ref.arr_bx[el[0]][el[1]].nbr.length){
                        flag= false;
                        this_ref.arr_bx[el[0]][el[1]].cnt=0;
                        this_ref.arr_bx[el[0]][el[1]].col=0;
                        this_ref.arr_bx[el[0]][el[1]].nbr.forEach( element =>{
                          new_arr.push(element)
                        })
                          }

             
             });
             //this.sound.play();
             nbr=new_arr;
             if(check_end(this_ref)){
               flag=true;
             }
             if(!flag){
                   this_ref.sound.currentTime=0;
                   this_ref.sound.play();      
                   setTimeout( over_flo,300,this_ref);

                 }
               

        } 

       this.arr_bx[x][y].cnt++;
       this.arr_bx[x][y].col=user+1;       
       if (this.arr_bx[x][y].cnt >=this.arr_bx[x][y].nbr.length){
         this.arr_bx[x][y].col=0;
         this.arr_bx[x][y].cnt=0;
         var nbr= this.arr_bx[x][y].nbr;
         var flag= false;
         if(!flag){
            this.sound.currentTime=0;
            this.sound.play();        
            setTimeout( over_flo,200,this);
         }
          

        

       }

    },
    pos_col: function(x,y){
      return this.arr_bx[x][y].col;
    },
    start_game: function(){
      
      var data = {
                           action: "start",
                           
                           };
              this.socket.send(JSON.stringify(data));


    },
    get_pos:function(val) {

      //this.move(this.crnt_usr,val.x,val.y);
      //this.next_usr();
      //this.sendMessage();
      if(this.turn){
         var data = {
                           action: "move",
                           player_move: val,
                           };
              if(this.connected){
                this.socket.send(JSON.stringify(data));
                this.turn=false;
              }

      }
      else 
        this.msg="This is not your turn..";
      

    },
    get_color:function () {
      return this.user_clr[this.crnt_usr];
      
    },
    demo:function(){
      console.log("function called from hooks");
    },

  initialize: function() {
     
    

  },
  join_room: function(){
    if(this.connected){
      var data={};  
        if(document.getElementById("icon_prefix").value)
        {      
               data = {
                           action: "join",
                           game_id: document.getElementById("icon_prefix").value,
                           };
              this.socket.send(JSON.stringify(data));

              
        }
      
      else
       {  data = { action: "new",
                            };
              this.socket.send(JSON.stringify(data));
              this.creator=true;
         }

    }
    else
       this.msg="Not connected";
     // this.game_on=true;
  },
   serverMessage: function(action, data) {     
    switch (action) {
      case "open":
        this.msg="Connected to Game Server";
        break;
      case "created":
       // APP.gameStarted(data.game_id);
       
        this.game_id= data.game_id;
        //this.crnt_usr=data.user;
        this.msg="ID: "+this.game_id+".  Waiting for Pair to Join..";        
        break;
      case "color":
        this.crnt_usr=data.user+1;
        break;
      case "started":
        //APP.gameStarted(data.game_id);
        this.game_on=true;
        //this.game_id= data.id;
        //this.crnt_usr=data.user;
        this.msg="Game Started...";
        break;
      case "paired":
        this.paired=true;
        this.msg="One player joined";
        this.game_id=data;
        break;
      case "move":
        //code to handle opponent move
        this.move(data.data.user,data.data.x,data.data.y);
        this.msg="friend's Move...";
        break;
      case "turn":
        this.turn = true;
        this.msg="make a move...";
        break;
      case "message":
        this.msg=data.message;
        break;
      case "pong":
        break;
        
      case "end":
       // APP.gameEnded();
       this.turn=false;
        if (data.result == "W") {
          this.msg="You Won. Congrats!";
        } else if (data.result == "L") {
          this.msg="You Lost.  Better luck next time.";
        } else if (data.result == "A") {
          this.msg="Game Aborted.";
        } else {
          this.msg="Game Ended.";
        }
        break;
      case "error":
        if (data.message) {
        (data.message)
        } else {
        this.msg="Error Occured";
        }
        break;
       default:
        this.msg="Unknown Action: " + action;
    }
  },
  sendMessage: function() {
    this.socket.send("hello");
   
  },
  on_open:  function() {
      this.connected = true;
      if(this.socket.readyState==1)
        this.msg='Connected to Game Server';
        setInterval(this.ping , 1000*30);
     
    },
    on_close: function() {
      this.connected = "galo";
     
      this.msg='Disconnected from Game Server';
      // Game Ended - Disconnected from Server

    },
    on_message: function(event) {
      var jsonObject = JSON.parse(event.data);
      var action = jsonObject.action;
      var data = jsonObject.data;
	
    // console.log("on_message called",action ,data);
     this.serverMessage(action,data)
    
     
    },
    load: function(){
      this.add_nbr();
      this.sound= new Audio();
      this.sound.src="/static/sound.mp3";
      this.move_sound= new Audio();
      this.move_sound.src="/static/move.wav";
      this.connect_socket();
         
    },
    connect_socket: function(){
        //var wsURL= "wss://"+window.location.hostname+"/demo/ws";
        var wsURL= "wss://chain-reaction-2020.herokuapp.com/demo/ws";
      //var wsURL= 'ws://192.168.43.228:8880/demo/ws';
     this.socket = new WebSocket(wsURL);
     this.socket.pass_this=this;


    // Show a connected message when the WebSocket is opened.
      this.socket.onopen =this.on_open();

    // Show a disconnected message when the WebSocket is closed.
          //this.socket.onclose = this.reconnect();
    // Handle any errors that occur.
    this.socket.onerror = function() {
      this.connected = false;
      this.gameOn = false;
      this.msg='Connection Error';
    };

    // Handle messages sent by the server.
    
    this.socket.onmessage = function(event){
      //this.pass_this.msg="successful";
      this.pass_this.on_message(event);
      
      
    };

    },
    ping: function(){
      var readyState = this.socket.readyState;
      if(readyState != 1)
       { this.msg="connection closed.";
         this.connected=false;
        }
      if( readyState == 1){
         var data = {
                           action: "ping",
                            };
              this.socket.send(JSON.stringify(data));
      }
       
    

    },
   

  },
    mounted(){
      console.log("component mounted");
      
    }
   ,
   updated(){
     // console.log("component updated");
      
    },
    created(){
     this.load();     
     setInterval(this.check_status, 1000);
    
    }
   
   
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
.cst{
  margin: 0px;
  

}
a{
  height: 45px;
  width: 45px;
  font-size: 25px;
}
.box{
  padding: 5px;
}
.hello{
  margin-top: 15px;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .8s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.img_box{
  margin: 10px;
}

</style>
