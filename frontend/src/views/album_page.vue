<template>
    <div class="conatiner-fluid" style="margin-top:70px" v-if="!album.flag || (role=='admin')">
       
        <div class="card mb-3" style="width:100%">
            <div class="row g-0">
                <div class="col-md-12">
                <div class="card-body">
                    <p class="card-text"><small class="text-body-secondary">Album</small></p>
                    <h1 class="card-title">{{ album.name }}</h1>
                    <p class="card-text">{{ album.songs.length }} songs</p>
                    <p class="card-text"><small class="text-body-secondary">By {{ album.artist }}</small></p>
                </div>
                </div>
            </div>
        </div>
         


    <div>
        <table class="table">
            <tbody>
                <tr v-for="(song,index) in album.songs" v-if="!song.flag">
                <th scope="row">{{ index+1 }}</th>
                <td style="display: flex; align-items: center;">
                            <div style="margin-right: 10px;">
                                <img :src="song.song_poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                            </div>
                            <div>
                                <div>{{ song.song_name }}</div>
                            </div>
                        </td>
                <td><router-link :to="{ name: 'song_page', params: { id: song.song_id } }" class="btn btn-primary"><i class="bi bi-play">Play</i></router-link></td>
                </tr>
            </tbody>
        </table>
    </div>



    </div>
    <div v-else style="margin-top:70px;display:flex;justify-content: center; align-items: center;">
        <h2>This Album is Flagged by Admin due to violation of community guidelines</h2>
    </div>
</template>


<script>
export default{
     data(){
        return{
            album:null,
            auth_token:null,
            role:localStorage.getItem('roles')
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
            const res= await fetch(`http://127.0.0.1:5000/album/${this.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data=await res.json()
            if (res.ok){
                 this.album=data
                 for (const song of this.album.songs){
                   song.song_poster='/src/assets/posters/'+song.song_poster
             }
            }
            else{
                console.log('error')
            }

        }
     }





}


</script>