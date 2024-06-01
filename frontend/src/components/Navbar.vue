

<template>
    <div v-show="!($route.name == 'login') && !($route.name == 'register') && !($route.name == 'welcome') && !($route.name == 'admin_login')">
        <nav class="navbar navbar-expand-lg fixed-top bg-dark navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Meloverse</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
                <li class="nav-item">
                <router-link class="nav-link active" aria-current="page" :to="{name:'dashboard'}">Home</router-link>
                </li>
                <li class="nav-item" v-if="roles=='creator'">
                    <router-link :to="{name:'creatorDashboard'}" class="nav-link">Creator Dash</router-link>
                </li>
                <li class="nav-item" v-if="roles=='user'">
                    <router-link :to="{name:'creator_signup'}" class="nav-link">Creator Signup</router-link>
                </li>
                <li class="nav-item">
                        <router-link :to="{name:'search'}" class="nav-link">Search</router-link>
                    </li>
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Library
                </a>
                <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" :to="{name:'playlist_page'}">Playlists</router-link></li>
                    <li ><router-link class="dropdown-item" :to="{name:'liked_songs'}">Liked Songs</router-link></li>
                    <li><router-link class="dropdown-item" :to="{name:'followed_artists'}">Followed Artists</router-link></li>
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
            roles:null
      }
    },
    methods:{
         async creator_signup(){
             const res= await fetch('http://127.0.0.1:5000/creator_signup',{
                headers:{
                    'Authentication-Token':localStorage.getItem('auth-token')
                }
             })
             if (res.ok){
                localStorage.setItem('roles','creator')
                this.$router.push({name:'creatorDashboard'})
             }
         },
         async logout(){
            const res= await fetch('http://127.0.0.1:5000/logout',{
                headers:{
                    'Authentication-Token':localStorage.getItem('auth-token')
                }
            })
            if (res.ok){
                localStorage.clear()
                this.$router.push('/login')
            }
         }

    },
    created(){
        this.roles=localStorage.getItem('roles')
    },
    

    

}
</script>