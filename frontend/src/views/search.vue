<template>
<div style="margin-top:70px">
    <nav class="navbar bg-body-tertiary" style= "padding: 20px ;bottom: 0; width: 100%;">
        <div class="container-fluid">
          <a class="navbar-brand"><h3>What are you looking for?</h3></a>
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search_value" v-model="search_value">
            <button class="btn btn-outline-success disabled">Search</button>
          </form>
        </div>
      </nav>
      <br>
    <div class="mx-2">
    <div style="display:flex;align-items:center;justify-content:center;"><h2>Search Results</h2></div>
    <div style="display:flex;align-items:center;justify-content:center;" v-if="!search_value"><h4>Type in a search value</h4></div>
    <div class="mb-3" v-if="search_value">
        <h3>Search Results</h3>
        <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home-tab-pane" type="button" role="tab" aria-controls="home-tab-pane" aria-selected="true">Songs</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile-tab-pane" type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false">Albums</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="contact-tab" data-bs-toggle="tab" data-bs-target="#contact-tab-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Artists</button>
            </li>
        </ul>
            <div class="tab-content" id="myTabContent">
            <div class="tab-pane fade show active" id="home-tab-pane" role="tabpanel" aria-labelledby="home-tab" tabindex="0">
                <div v-if="song_results.length!=0">
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Artist</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(song,index) in song_results" v-if="!song.flag">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ song.song_name }}</td>
                            <td>{{ song.artist_name }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            
            </div>
            <div class="tab-pane fade" id="profile-tab-pane" role="tabpanel" aria-labelledby="profile-tab" tabindex="0">
                <div v-if="album_results.length!=0">
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Artist</th>
                            <th scope="col">Songs</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(album,index) in album_results" v-if="!album.flag">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ album.album_name }}</td>
                            <td>{{ album.artist }}</td>
                            <td>{{ album.songs.length }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'album_page', params:{id:album.album_id}}">View</router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            
            </div>
            <div class="tab-pane fade" id="contact-tab-pane" role="tabpanel" aria-labelledby="contact-tab" tabindex="0">
                <div v-if="artist_results.length!=0">
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Albums</th>
                            <th scope="col">Songs</th>
                            <th scope="col">Followers</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(artist,index) in artist_results" v-if="artist.active">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ artist.user_name }}</td>
                            <td>{{ artist.albums.length }}</td>
                            <td>{{ artist.songs.length }}</td>
                            <td>{{ artist.follower_len }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'artist_page', params:{id:artist.id}}">View</router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            </div>
            
            </div>
        
    </div>

    <div class="mb-3" v-else>
        <h3>Browse All</h3>
        <ul class="nav nav-tabs" id="myTab2" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="home-tab2" data-bs-toggle="tab" data-bs-target="#home-tab-pane2" type="button" role="tab" aria-controls="home-tab-pane2" aria-selected="true">Songs</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="profile-tab2" data-bs-toggle="tab" data-bs-target="#profile-tab-pane2" type="button" role="tab" aria-controls="profile-tab-pane2" aria-selected="false">Albums</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="contact-tab2" data-bs-toggle="tab" data-bs-target="#contact-tab-pane2" type="button" role="tab" aria-controls="contact-tab-pane2" aria-selected="false">Artists</button>
            </li>
        </ul>
            <div class="tab-content" id="myTab2Content">
            <div class="tab-pane fade show active" id="home-tab-pane2" role="tabpanel" aria-labelledby="home-tab2" tabindex="0">
                <div>
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Artist</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(song,index) in songs" v-if="!song.flag">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ song.song_name }}</td>
                            <td>{{ song.artist_name }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            
            </div>
            <div class="tab-pane fade" id="profile-tab-pane2" role="tabpanel" aria-labelledby="profile-tab2" tabindex="0">
                <div>
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Artist</th>
                            <th scope="col">Songs</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(album,index) in albums" v-if="!album.flag">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ album.album_name }}</td>
                            <td>{{ album.artist }}</td>
                            <td>{{ album.songs.length }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'album_page', params:{id:album.album_id}}">View</router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            
            </div>
            <div class="tab-pane fade" id="contact-tab-pane2" role="tabpanel" aria-labelledby="contact-tab2" tabindex="0">
                <div>
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Albums</th>
                            <th scope="col">Songs</th>
                            <th scope="col">Followers</th>
                            <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(artist,index) in artists" v-if="artist.active">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ artist.user_name }}</td>
                            <td>{{ artist.albums.length }}</td>
                            <td>{{ artist.songs.length }}</td>
                            <td>{{ artist.follower_len }}</td>
                            <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'artist_page', params:{id:artist.id}}">View</router-link></td>
                            </tr>
                        </tbody> 
                        </table>
                </div> 
            </div>
            
            </div>
    </div>
    
  </div>
</div> 
</template>

<script>
export default{
    data(){
        return{
            search_value:'',
            songs:null,
            artists:null,
            albums:null,
            auth_token:null,
            song_results:[],
            album_results:[],
            artist_results:[]
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
              this.get_all_songs()
              this.get_all_albums()
              this.get_all_artists()
        }
    },
    methods:{
        async get_all_songs(){
             const res = await fetch('http://127.0.0.1:5000/api/song',{
                headers:{
                    'Authentication-Token':this.auth_token
                }
             })
             const data= await res.json()
             if (res.ok){
                this.songs=data
                console.log(this.songs)
             }
        },
        async get_all_albums(){
            const res= await fetch('http://127.0.0.1:5000/all_albums',{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.albums=data
                console.log(this.albums)
            }
        },
        async get_all_artists(){
            const res= await fetch('http://127.0.0.1:5000/api/artist/0?option=all',{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.artists=data
                console.log(this.artists)
            }
        }
    },
    watch:{
        search_value(newValue,oldValue){
            if (newValue!=''){
                    const searchEx = new RegExp(this.search_value, 'i')
                    this.song_results = this.songs.filter(song => searchEx.test(song.song_name));
                    this.artist_results = this.artists.filter(artist => searchEx.test(artist.user_name));
                    this.album_results = this.albums.filter(album => searchEx.test(album.album_name));
                }
            else{
                this.song_results=[]
                this.album_results=[]
                this.artist_results=[]
            }    
        }
    }
}
</script>