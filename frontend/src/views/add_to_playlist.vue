<template>
  <div class="container-fluid" style="margin-top:70px">
    <table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Song</th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(song,index) in songs" v-if="!song.flag">
      <td>{{ index+1 }}</td>
      <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                    <div>
                        <div style="font-size: 25px;">{{ song.song_name }}</div>
                        <div style="color:grey"> By{{ song.artist_name }}</div>
                    </div>
                </td>
      <td><button class="btn btn-light btn-sm" :style="{backgroundColor: song.added ? '#DC6868 ' : '#9BDD6D'}" @click="add_song(song.song_id)">{{ song.added ? 'Remove' : 'Add'}}</button></td>
    </tr>
  </tbody>
</table> 
<button @click="go_back" class="btn btn-primary">Done</button></div>
</template>

<script>
export default{
  data(){
    return{
      songs:null,
      auth_token:null
    }
  },
  created(){
    this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
      else{ this.get_all_songs()}
  },
  props:['playlist_id'],
  methods:{
    async get_all_songs(){
      const res= await fetch(`http://127.0.0.1:5000/api/song`,{
        headers:{
          'Authentication-Token':this.auth_token
        }
      })
      const data= await res.json()
      if (res.ok){
        this.songs=data.map((song) => ({ ...song, added: false }))
        for (const song of this.songs){
                   song.poster='/src/assets/posters/'+song.poster
                   song.audio='/src/assets/songs/'+song.audio
                   if (song.in_playlists.includes(this.playlist_id)){
                      song.added=true
                   }
             }
      }
      else {
        console.log("error")
      }
    },
    async add_song(song_id){
      let current_song=null
        for (const song of this.songs){
          if(song.song_id==song_id){
            current_song=song
          }
        }
        if (!current_song.added){
        const url=`http://127.0.0.1:5000/api/add_playlist/${song_id}/${this.playlist_id}?option=add`
        const res=await fetch(url,
                              {
                                method:'PUT',
                                headers:{
                                    'Authentication-Token':this.auth_token
                                }
                              }
                            )
        const data= await res.json()
        if (res.ok){
            current_song.added=true
        }
        else{
            console.log("error")
        }
      }
      else{
        const url=`http://127.0.0.1:5000/api/add_playlist/${song_id}/${this.playlist_id}?option=remove`
        const res= await fetch(url,
                              {
                                method:'PUT',
                                headers:{
                                    'Authentication-Token':this.auth_token
                                }
                              }
                                )
        if (res.ok){
          current_song.added=false
        } 
        else{
          console.log('error')
        }                      
      }
    },
    go_back(){
      this.$router.go(-1)
    }

  }
}


</script>