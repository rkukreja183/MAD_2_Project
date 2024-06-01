<template>
    <div style="margin-top:70px" class="container-fluid" v-if="active || (role=='admin') ">
     
        <div class="card mb-3" style="width:100%">
            <div class="row g-0">
                <div class="col-md-2">
                <img :src="profile_pic" class="img-fluid rounded-start" alt="...">
                </div>
                <div class="col-md-10">
                <div class="card-body">
                    <h1 class="card-title">This is {{ name }}</h1>
                    <button class="btn btn-outline-info" @click="follow_artist()"> {{ follow ? 'UnFollow' : 'Follow'}}</button>
                    <p class="card-text">{{ songs.length }} songs  |   {{ albums.length }} albums</p>
                    <p class="card-text"><small class="text-body-secondary">Over {{ streams }} streams</small></p>
                </div>
                </div>
            </div>
        </div>

        <div class="container-fluid">
            <div class="row">
                <div class="col-6">
                    <h5>New Releases</h5>
                    <table class="table" v-if="new_songs.length>0" >
                        <thead>
                            <th>#</th>
                            <th>Song</th>
                            <th>Streams</th>
                        </thead>
                        <tbody>
                            <tr v-for="(song,index) in new_songs" v-if="!song.flag">
                            <th scope="row" style="padding-top: 18px;">{{ index+1 }}</th>
                            <td style="display: flex; align-items: center;">
                            <div style="margin-right: 10px;">
                                <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                            </div>
                            <div>
                                <div>{{ song.song_name }}</div>
                            </div>
                        </td>
                            <td>{{ song.plays }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else>
                      No new Songs
                    </div>
                   </div>
                <div class="col-6">
                    <h5>Popular</h5>
                    <table class="table" v-if="new_songs.length>0">
                        <thead>
                            <th>#</th>
                            <th>Song</th>
                            <th>Rating</th>
                        </thead>
                        <tbody>
                            <tr v-for="(song,index) in top_songs" v-if="!song.flag">
                            <th scope="row">{{ index+1 }}</th>
                            <td style="display: flex; align-items: center;">
                            <div style="margin-right: 10px;">
                                <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                            </div>
                            <div>
                                <div>{{ song.song_name }}</div>
                            </div>
                        </td>
                            <td>{{ song.total_rating }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else>
                        No Popular Songs
                    </div>
                </div>  
        </div>
 

    <div>
        <ul class="nav nav-underline">
        <li class="nav-item">
            <button :class="{ 'nav-link': true, 'active': option === 'songs' }" aria-current="page"  @click="option='songs'" >Songs</button>
        </li>
        <li class="nav-item">
            <button :class="{ 'nav-link': true, 'active': option === 'albums' }" aria-current="page" @click="option='albums'" >Albums</button>
        </li>
        </ul>
    </div>
        <div class="mt-4" v-if="option==='songs'">
            <div style="display: flex; justify-content: space-between;">
                <h5>Songs</h5>
            </div>
            <div class="card-group" v-if="songs.length>0">
                <router-link v-for="(song,index) in songs" :key="song.song_id" :to="{ name: 'song_page', params: { id: song.song_id } }" v-if="!song.flag">
                <div class="card" style="width: 12.72rem;height:15.5rem; display:inline-block;margin-right: 10px;border: 1px solid #dee2e6;">
                    <img :src="song.poster" class="card-img-top" alt="..." style="height: 10rem; width: 100%;">
                    <div class="card-body" style="width:100%;overflow: hidden; white-space: normal;">
                        <h5 class="card-title">{{ song.song_name }}</h5>
                        <p class="card-text">{{ song.plays }} streams</p>
                    </div> 
                </div> 
                </router-link>  
            </div>
            <div v-else>
                No Songs Uploaded Yet
            </div>
        </div>
         
        <div class="mt-4" v-else-if="option==='albums'">
            <div style="display: flex; justify-content: space-between;">
                <h5>Albums</h5>
            </div>
            <div class="card-group" v-if="albums.length>0">
                <router-link v-for="(album,index) in albums" :key="album.album_id" :to="{ name: 'album_page', params: { id: album.album_id } }" v-if="!album.flag">
                    <div class="card" style="width: 12.72rem;height:8rem; display:inline-block;margin-right: 10px;border: 1px solid #dee2e6;" >
                        <div class="card-body" style="width:100%;overflow: hidden; white-space: normal;">
                            <h5 class="card-title">{{ album.album_name }}</h5>
                            <p class="card-text">{{ album.songs.length }} songs</p>
                        </div>
                    </div>    
                </router-link>   
            </div>
            <div v-else>
                  No Albums created yet
            </div>
        </div> 
    </div>
    </div>
    <div v-else style="margin-top:70px;display:flex;justify-content: center; align-items: center;">
        <h2>This Artist is Flagged by Admin due to violation of community guidelines</h2>
    </div>
</template>

<script>
export default{
    data(){
        return{
           auth_token:null,
           songs:null,
           albums:null,
           top_songs:null,
           new_songs:null, 
           name:null,
           option:'songs',
           role:localStorage.getItem('roles'),
           active:'',
           follow:null,
           streams:null,
           profile_pic:null
        }
    },
    props:['id'],
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_artist()
        }
    },

    methods:{
        async get_artist(){
            const res = await fetch(`http://127.0.0.1:5000/api/artist/${this.$route.params.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.name=data.user_name
                this.songs=data.songs
                this.albums=data.albums
                this.top_songs=data.top_songs
                this.new_songs=data.new_uploads
                this.active=data.active,
                this.follow=data.follow
                this.streams=data.streams
                this.profile_pic='/src/assets/profiles/'+data.profile_pic
                for (const song of this.songs){
                   song.poster='/src/assets/posters/'+song.poster
             }

             for (const song of this.top_songs){
                   song.poster='/src/assets/posters/'+song.poster
             }

             for (const song of this.new_songs){
                   song.poster='/src/assets/posters/'+song.poster
             }
            }
            else{
                console.log(error)
            }
        },
        async follow_artist(){
            const res = await fetch(`http://127.0.0.1:5000/follow_artist/${this.$route.params.id}`,{
                headers:{
                    'Authentication-Token': this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.follow=!this.follow
            }
        }
    }
}


</script>