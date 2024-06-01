

<script setup>
import Navbar from "../src/components/Navbar.vue";
import A_Nav from "../src/components/admin_navbar.vue";

</script>

<template>
  <div id="app">
    
    <Navbar />
    <A_Nav/>
    
    <router-view />
  </div>
</template>
