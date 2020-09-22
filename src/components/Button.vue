<template>
   <div class="element " >
    <!-- <a v-on:click="btn_id" class="col waves-effect waves-light btn "  v-bind:class="[user,rotation]" v-bind:id="posx.toString()+posy" >{{count}}</a>
        -->
     
        <span id="unit">
          <div v-on:click="btn_id" class="col waves-effect waves-light btn own"  v-bind:class="[user]" v-bind:id="posx.toString()+posy" >
            <div v-bind:class="rotation">
                <img v-if="cnt" v-bind:id="'img'+posx.toString()+posy"  height="30" width="30">

            </div>
            
          </div>    
        </span>
      
   </div>    
          
          
    
        
      
</template>

<script>
export default {
  name: 'Button',
 
  props: {
    msg: String,
    cnt: Number,
    nbr: Number,
    user: String,
    posx: Number,
    posy: Number,
   
  },
  data(){
    return {
     rot:false,
     
    }
  },
  methods: {
     btn_id: function() {
         this.$emit('btnpos', [this.posx,this.posy]);
          
      },
      ball: function(){

      }
  },
  computed:{
    rotation: function(){
             //console.log(this.user);
                 var rotate=null;
                 if(this.rot)
                    rotate= "rotate";
                  else
                     rotate= null;
                 return rotate;
                  
    },
    count: function(){
     
               return this.cnt;

    }
   
  },
   updated(){
      //console.log(" button component updated");
      var ele= document.getElementById("img"+this.posx.toString()+this.posy.toString());
          // var host= "/static/";
       if(this.cnt>=3)
              {
              
                ele.src="/static/3ball.png";
                 
              } 
              else if(this.cnt==2)
                 {
                    //console.log("count"+this.cnt);
                    ele.src="/static/2ball.png";
                 }
                 else if(this.cnt==1){
                   ele.src="/static/1ball.png";
                                      }
              
              if(this.cnt==this.nbr-1){
                 this.rot=true;
              }
              else if(this.cnt < this.nbr-1){
                 this.rot=false;
              }
                 
                
                
    },
  
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.own{
  height: 45px;
  width: 45px;
  font-size: 25px;
}
.box{
  padding: 5px;
}
.rotate {
  animation: rotation 10s infinite linear;
}
@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}


</style>
