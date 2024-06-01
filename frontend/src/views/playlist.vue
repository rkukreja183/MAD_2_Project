<template>
<div class="container-fluid" style="margin-top:70px">
   <div class="row">
         <h3>{{ playlist.playlist_name }}</h3>
   </div>
   <div class="row">
    <table class="table">
            <tbody>
                <tr v-for="(song,index) in playlist.songs" :key="song.song_id" v-if="!song.flag">
                <th scope="row">{{ index+1 }}</th>
                <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                    <div>
                        <div style="font-size: 25px;">{{ song.song_name }}</div>
                        <div style="color:grey"> By{{ song.artist_name }}</div>
                    </div>
                </td>
                <td><router-link class="btn btn-primary" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link>
                    <button class="btn btn-danger" @click="remove_song(song.song_id)">Remove</button>
                </td>
                </tr>
            </tbody>
     </table>
   </div>
</div>
</template>

<script>
export default{
    data(){
        return{
              auth_token:null,
              playlist:null,
        }
    },
    props:['id'],
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_playlist()
        }
    },
    methods:{
        async get_playlist(){
            const res= await fetch(`http://127.0.0.1:5000/api/playlist?option=${this.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.playlist=data
                for (const song of this.playlist.songs){
                   song.poster='/src/assets/posters/'+song.poster
                   song.audio='/src/assets/songs/'+song.audio
             }
            }

        },
        async remove_song(song_id){
            const res = await fetch(`http://127.0.0.1:5000/api/add_playlist/${song_id}/${this.id}?option=remove`,{
                method:'PUT',
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.$router.go(0)
            }
        }
    }
}
</script>