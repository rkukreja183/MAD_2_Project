<template>
<div class="container-fluid" style="margin-top:70px">
        <h3>Followed Artists</h3>
            <div class="row" v-if="followed_artists.length!=0">
                <table class="table">
                    <thead>
                        <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Songs</th>
                        <th scope="col">Albums</th>
                        <th scope="col">View</th>
                        </tr>
                    </thead>
                        <tbody>
                            <tr v-for="(artist,index) in followed_artists" :key="artist.id" v-if="artist.active">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ artist.name }}</td>
                            <td>{{ artist.songs }}</td>
                            <td>{{ artist.albums }}</td>
                            <td><router-link class="btn btn-primary" :to="{name:'artist_page', params:{id:artist.id}}"><i class="bi bi-play">View</i></router-link></td>
                            </tr>
                        </tbody>
                </table>
            </div>
            <div class="row" v-else>
                 No Followed Artists
            </div>
   </div>
</template>

<script>
export default{
    data(){
        return{
            auth_token:null,
            followed_artists:null
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_followed_artists()
        }
    },
    methods:{
        async get_followed_artists(){
            const res= await fetch(`http://127.0.0.1:5000/followed_artists`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data=await res.json()
            if (res.ok){
               this.followed_artists=data
            }
        }
    }
}
</script>