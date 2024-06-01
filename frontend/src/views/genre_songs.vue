<template>
<div class="container-fluid" style="margin-top:70px">
   <div class="row">
         <h3>{{ genre }}</h3>
   </div>
   <div class="row" v-if="songs.length>0">
    <table class="table">
            <tbody>
                <tr v-for="(song,index) in songs" :key="song.song_id" v-if="!song.flag">
                <th scope="row">{{ index+1 }}</th>
                <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                    <div>
                        <div style="font-size: 25px;">{{ song.song_name }}</div>
                        <div style="color:grey"> By {{ song.song_singer }}</div>
                    </div>
                </td>
                <td><router-link class="btn btn-primary" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link></td>
                </tr>
            </tbody>
     </table>
   </div>
   <div v-else>
    No songs in this genre yet
    </div>
</div>
</template>
<script>
export default{
    data(){
        return{
            songs:null,
            auth_token:null
        }
    },
    props:['genre'],
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_genre_songs()
        }
    },
    methods:{
         async get_genre_songs(){
            const res= await fetch(`http://127.0.0.1:5000/songs_by_genres/${this.genre}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if(res.ok){
                this.songs=data
                for (const song of this.songs){
                   song.poster='/src/assets/posters/'+song.poster
             }
            }
         }
    }
}
</script>