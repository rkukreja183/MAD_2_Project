<template>
    <div v-show="roles=='admin'">
        <nav class="navbar navbar-expand-lg fixed-top bg-dark navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Meloverse</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
                <li class="nav-item">
                <router-link class="nav-link active" aria-current="page" :to="{name:'admin_dashboard'}">Home</router-link>
                </li>
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Library
                </a>
                <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" :to="{name:'a_all_songs'}">All Songs</router-link></li>
                    <li ><router-link class="dropdown-item" :to="{name:'a_all_artists'}">All Artists</router-link></li>
                    <li><router-link class="dropdown-item" :to="{name:'a_all_albums'}">All Albums</router-link></li>
                </ul>
                </li>
            </ul>
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <button @click="logout()" class="nav-link">Logout <i class="fa-solid fa-right-from-bracket ms-1"></i></button>
                </li>
            </ul>
            </div>
        </div>
        </nav>
    </div>
</template>

<script>
export default{
    data(){
        return{
            roles:null,
      }
    },
    created(){
        this.roles=localStorage.getItem('roles')
    },
    methods:{
        async logout(){
            const res= await fetch('http://127.0.0.1:5000/logout',{
                headers:{
                    'Authentication-Token':localStorage.getItem('auth-token')
                }
            })
            if (res.ok){
                localStorage.clear()
                this.roles=null
                this.$router.push('/')
            }
         }
    }
}
</script>