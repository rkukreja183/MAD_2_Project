<template>
  <div v-if="error_message">{{ error_message }}</div>
 <div class="container" v-else style="margin-top:70px">
        <div class="col-12">
        <table class="table">
  <thead>
    <tr>
      <th scope="col">Song Name</th>
      <th scope="col">Album/Single</th>
      <th scope="col">Streams</th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="song in songs">
      <td>{{ song.song_name }}</td>
      <td v-if="song.album_id">Album</td>
      <td v-if="!song.album_id">Single</td>
      <td>{{ song.streams }}</td>
      <td>
        <button class="btn btn-light btn-sm" :style="{backgroundColor: song.added ? '#DC6868 ' : '#9BDD6D'}" @click="add_song(song.song_id)">{{ song.added ? 'Remove' : 'Add'}}</button>
    </td>
    </tr>
  </tbody>
</table>
<button @click="go_back" class="btn btn-primary">Done</button>
</div>
    </div>
</template>

<script>
export default{
   data(){
    return{
      auth_token:null,
      songs:null,
      error_message:null,
    }
   },
   props:['album_id'],
   created(){
    this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
      else{this.fetch_available_songs()}
   },
   methods:{
   async fetch_available_songs(){
    console.log('running')
        const res=await fetch('http://127.0.0.1:5000/artist_songs',
        {
            headers:{
                'Authentication-Token':this.auth_token
            }
        }
        
        )
        const data= await res.json()
        if (res.ok){
            this.songs=data.map((song) => ({ ...song, added: false }))
            for (const song of this.songs){
              if (song.album_id==this.album_id){
                song.added=true
              }
            }
            console.log(this.songs)
        }
        else {
           console.log('error')
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
        const url=`http://127.0.0.1:5000/api/add_album/${song_id}/${this.album_id}?option=add`
        const res=await fetch(url,
                              {
                                method:'PUT',
                                headers:{
                                    'Authentication-Token':this.auth_token,
                                    'Content-Type': 'application/json'
                                }
                              }
                            )
        const data= await res.json()
        if (res.ok){
            current_song.added=true
        }
        else{
            this.error_message=data.message
        }
      }
      else{
        const url=`http://127.0.0.1:5000/api/add_album/${song_id}/${this.album_id}?option=remove`
        const res= await fetch(url,
                              {
                                method:'PUT',
                                headers:{
                                    'Authentication-Token':this.auth_token,
                                    'Content-Type': 'application/json'
                                }
                              }
                                )
        if (res.ok){
          current_song.added=false
        } 
        else{
          this.error_message=data.message
        }                      
      }
    },
    add_or_remove(album){
        return album==this.album_id
    },
    go_back(){
      this.$router.go(-1)
    }
   }
}
</script>