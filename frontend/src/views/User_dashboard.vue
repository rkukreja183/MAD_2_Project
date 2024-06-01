
<template>
    <div class="container-fluid" style="margin-top:70px"> 
       <div class="row" >
        <div class="mb-1">
        </div>
    </div>
     
    <div>
      <h5>Top Songs</h5>
      <div class="card-group">
        <router-link v-for="song in top_songs" :key="song.song_id" :to="{ name: 'song_page', params: { id: song.song_id } }" v-if="!song.flag">
        <div class="card" style="width: 12.72rem;height:16rem; display:inline-block;margin-right: 10px;border: 1px solid #dee2e6;"  >
            <img :src="song.song_poster" class="card-img-top" alt="..." style="height: 10rem; width: 100%;">
            <div class="card-body" style="width:100%;overflow: hidden; white-space: normal;">
                <h6 class="card-title">{{ song.song_name }}</h6>
                <p class="card-text">By {{ song.song_singer }} | {{ song.album }}<br></p>
                </div>
        </div>
        </router-link>
      </div>
    </div>

    <div class="mt-4">
            <h5>Discover New Music</h5>
            <div class="card-group">
            <router-link  v-for="song in recent_songs" :key="song.song_id" :to="{ name: 'song_page', params: { id: song.song_id } }" v-if="!song.flag">
                <div class="card" style="width: 12.72rem;height:16rem; display:inline-block;margin-right: 10px;border: 1px solid #dee2e6;" >
                    <img :src="song.song_poster" class="card-img-top" alt="..." style="height: 10rem; width: 100%;">
                    <div class="card-body" style="width:100%;overflow: hidden; white-space: normal;">
                        <h6 class="card-title">{{ song.song_name }}</h6>
                        <p class="card-text">By {{ song.song_singer }} | {{ song.album }}</p>
                    </div>
                </div>    
            </router-link>
      </div> 
    </div>

    <div class="mt-4">
            <h5>Discover New Artists</h5>
            <div class="card-group">
            <router-link v-for="artist in artists" :key="artist.id" :to="{ name: 'artist_page', params: { id: artist.id } }" v-if="artist.active">
                <div class="card" style="width: 12.72rem;height:16rem; display:inline-block;margin-right: 10px;border: 1px solid #dee2e6;" >
                    <img :src="artist.profile" class="card-img-top" alt="..." style="height: 10rem; width: 100%;">
                    <div class="card-body" style="width:100%;overflow: hidden; white-space: normal;">
                        <h6 class="card-title">{{ artist.name }}</h6>
                        <p class="card-text">{{ artist.no_songs }} songs released | {{ artist.no_albums }} albums released</p>
                    </div>
                </div>  
         </router-link>
      </div> 
    </div>

    <div class="mt-4 mb-3 text-center">
            <h2>Genres</h2>
            <div class="row mt-2">
                <div class="col-3 d-flex justify-content-center align-items-center" >
                    <router-link :to="{name:'genre_songs', params:{genre:'Pop'}}">
                    <img src="/src/assets/genres/Pop.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                    </router-link>
                </div> 
               
                <div class="col-3 d-flex justify-content-center align-items-center" >
                    <router-link :to="{name:'genre_songs', params:{genre:'Classical_Music'}}">
                    <img src="/src/assets/genres/Classical.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link>
                </div> 
                
                
                <div class="col-3 d-flex justify-content-center align-items-center" >
                    <router-link :to="{name:'genre_songs', params:{genre:'Dance/Electronic_Music'}}">
                    <img src="/src/assets/genres/Electronic.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link>
                </div> 
                
                
                <div class="col-3 d-flex justify-content-center align-items-center">
                    <router-link :to="{name:'genre_songs', params:{genre:'Indie'}}">
                    <img src="/src/assets/genres/Indie.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link>
                </div> 
                 
            </div>
            <div class="row mt-2"> 
                
                <div class="col-3 d-flex justify-content-center align-items-center">
                    <router-link :to="{name:'genre_songs', params:{genre:'Jazz'}}">
                    <img src="/src/assets/genres/Jazz.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link>  
                </div>
                
                
                <div class="col-3 d-flex justify-content-center align-items-center">
                    <router-link :to="{name:'genre_songs', params:{genre:'Country_Music'}}">
                    <img src="/src/assets/genres/Country.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link> 
                </div>
                
                
                <div class="col-3 d-flex justify-content-center align-items-center" >
                    <router-link :to="{name:'genre_songs', params:{genre:'R&B'}}">
                    <img src="/src/assets/genres/Rhythm & Blues.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link> 
                </div> 
               
                
                <div class="col-3 d-flex justify-content-center align-items-center">
                    <router-link :to="{name:'genre_songs', params:{genre:'Soul'}}">
                    <img src="/src/assets/genres/Soul.png" class="card-img-top" alt="..." style="height:90%;width:90%">
                </router-link> 
                </div> 
                 

      </div> 
    </div>





   </div>
</template>

<script>
export default {
    data(){
        return{
             auth_token:null,
             top_songs:null,
             recent_songs:null,
             artists:null,
             genre_songs:null
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        const reload= localStorage.getItem('reload')
        if (reload==1){
            localStorage.setItem('reload',0)
            window.location.reload()
        }
        if (this.auth_token && reload==0) {
            this.get_top_songs()
            this.get_recent_songs()
            this.discover_artists()
        }
        else{
            this.$router.push('/login')
        }
    },
    props: ['id'],
    methods:{
    async get_top_songs(){
        const res = await fetch('http://127.0.0.1:5000/top_songs',{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
             this.top_songs=data
             for (const song of this.top_songs){
                   song.song_poster='/src/assets/posters/'+song.song_poster
                   song.song_audio='/src/assets/songs/'+song.song_audio
             }
        }
        else{
            console.log('error')
        }
    },
    async get_recent_songs(){
        const res= await fetch('http://127.0.0.1:5000/recent_uploads',{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
            this.recent_songs=data
             for (const song of this.recent_songs){
                   song.song_poster='/src/assets/posters/'+song.song_poster
                   song.song_audio='/src/assets/songs/'+song.song_audio
             }
        }
        else{
            console.log('error')
        }
    },
    async discover_artists(){
        const res= await fetch('http://127.0.0.1:5000/discover_artists',{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
            this.artists=data
            for (const artist of this.artists){
                   artist.profile='/src/assets/profiles/'+artist.profile
                   
             }
        }
    },
}
}
</script>