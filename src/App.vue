<template>
  <div id="app">

  <nav>
    <div class="nav-wrapper teal darken-2">
      <a href="#" class="brand-logo left">ChainReaction</a>         
      <ul id="nav-mobile" class="right ">
        <li><a href="#">Home</a></li>
        </ul>
    </div>
  </nav>
   
    <HelloWorld  msg="Game made by abhijit"/>
    
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';



export default {
  name: 'App',
  components: {
    HelloWorld,
    
  },
 
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  
}
body{
  background-color: #cfd8dc ;
}

</style>
