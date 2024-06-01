<template>
<div class="container-fluid" style="margin-top:70px">
    <div class="row">
        <h3>{{ album.album_name }}</h3>
    </div>
    <div class="row">
    <table class="table">
        <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Song</th>
            <th scope="col">Actions</th>
            </tr>
        </thead>
            <tbody>
                <tr v-for="(song,index) in album.songs" :key="song.song_id">
                <th scope="row">{{ index+1 }}</th>
                <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                        <div style="font-size: 25px;">{{ song.song_name }}</div>
                </td>
                <td>
                    <router-link class="btn btn-outline-primary" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link>
                    <router-link class="btn btn-outline-warning" :to="{name:'update_song', params:{song_id:song.song_id}}">Update</router-link>
                    <button class="btn btn-outline-danger" @click="remove_song(song.song_id)">Remove</button>
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
           album:null
        }
    },
    props:['id'],
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_album()
        }
    },
    methods:{
        async get_album(){
            const res= await fetch(`http://127.0.0.1:5000/api/album?option=${this.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data = await res.json()
            if (res.ok){
                this.album=data
                for (const song of this.album.songs){
                   song.poster='/src/assets/posters/'+song.poster
             }
                console.log(this.album)
            }
            else{
                console.log('error')
            }
        },
        async remove_song(song_id){
            const res = await fetch(`http://127.0.0.1:5000/api/add_album/${song_id}/${this.id}?option=remove`,{
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