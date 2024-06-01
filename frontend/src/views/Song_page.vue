<template>
    <div v-if="!song_details.admin_flag || (role=='admin')">
        <div class="card mb-3" style="width:100%;margin-top:70px">
            <div class="row g-0">
                <div class="col-md-8">
                <div class="card-body">
                    <div>
                    <h1 class="card-title" style="display:inline-block;margin-right: 20px;">{{ song_details.name }}</h1>
                    <button @click="like_song()" class="btn btn-outline-danger" v-if="!song_details.user_is_artist && !(role=='admin')"><i :class="{'bi':true, 'bi-heart-fill':song_details.like, 'bi-heart':!song_details.like}" style="font-size:15px" ></i></button>
                    <button @click="flag_song()" class="btn btn-outline-dark" v-if="!song_details.user_is_artist && !(role=='admin')"><i :class="{'bi':true, 'bi-flag-fill':song_details.flag, 'bi-flag':!song_details.flag}" style="font-size:15px" ></i></button>
                </div>
                    <p class="card-text">by {{ song_details.artist_name }}</p>
                    <p class="card-text"><small class="text-body-secondary">Over {{ song_details.streams }} streams</small></p>
                               
                </div>
                </div>
                <div class="col-md-4 mt-2">
                    <p class="card-text"> 
                        <div>
                            <label for="rating-disabled">Total Rating</label>
                            <button class="btn btn-outline-light"><b-form-rating id="rating-disabled" :value="song_details.total_rating" disabled inline></b-form-rating></button>
                        </div>
                    </p>    
                    <p class="card-text" v-if="!song_details.user_is_artist && !(role=='admin')"> 
                                <label for="rating-inline"> Your Rating</label>
                                <button @click="change_rating()" class="btn btn-outline-light"><b-form-rating id="rating-inline" inline v-model="value" ></b-form-rating></button>
                    </p>
                </div>
            </div>
        </div>


       <div class="container-fluid">
        <div class="row mb-3 mt-4">
            <div class="col-6">
                <img :src="song_details.poster" style="height:400px;width:400px;padding-left: 100px;">
            </div>
            <div class="col-6">
                <div class="outer_custom">
                <div class="inner_custom">
                    <p v-for="(line, index) in song_details.lyrics.split('\n')" :key="index">{{ line }}</p>
                </div>
            </div>
            </div>
        </div>


        <div class="row mt-5">
             <audio :src="song_details.url" controls style="width:100%"></audio>
        </div>
       </div>





    </div>

    <div v-else style="margin-top:70px;display:flex;justify-content: center; align-items: center;">
        <h2>This song is Flagged by Admin due to violation of community guidelines</h2>
    </div>
</template>

<script>
export default {
    data() {
        return {
            song_details: {
                name: null,
                url: null,
                poster: null,
                lyrics: null,
                artist_name:null,
                streams:null,
                total_rating:null,
                user_is_artist:null,
                like:null,
                flag:null,
                admin_flag:null
            },
            auth_token: null,
            value:null,
            role:localStorage.getItem('roles')
        }
    },

    props: ['id'],
    created() {
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else { this.get_song() }
    },
    methods: {
        async get_song() {
            this.song_details.name = null
            this.song_details.url = null
            this.song_details.poster = null
            this.song_details.lyrics = null
            const res = await fetch(`http://127.0.0.1:5000/song/${this.$route.params.id}`,
                {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.auth_token
                    }
                })
            const data = await res.json()
            if (res.ok) {
                this.song_details.name = data.song_name
                this.song_details.url ='/src/assets/songs/'+data.path
                this.song_details.poster ='/src/assets/posters/'+data.poster
                this.song_details.lyrics = data.lyrics
                this.song_details.artist_name=data.creator_name
                this.song_details.streams=data.plays
                this.song_details.total_rating=data.total_rating
                this.song_details.user_is_artist=data.user_is_artist
                this.song_details.like=data.like
                this.song_details.flag=data.flag
                this.song_details.admin_flag=data.admin_flag
                this.value=data.current_user_rating
                console.log(this.song_details.like)
            } else { console.log('error') }
        },
        async change_rating(){
            const res= await fetch(`http://127.0.0.1:5000/rate_song/${this.$route.params.id}`,{
                method:'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.auth_token
                },
                body: JSON.stringify({
                        value: this.value,
                        })
            })
            const data=await res.json()
            if (res.ok){
                this.song_details.total_rating=data.total_rating
            }
        },
        async like_song(){
            const res= await fetch(`http://127.0.0.1:5000/like_song/${this.$route.params.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.song_details.like=!this.song_details.like
            }
        },
        async flag_song(){
            const res= await fetch(`http://127.0.0.1:5000/flag_song/${this.$route.params.id}`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.song_details.flag=!this.song_details.flag
            }
        }
    },

}
</script>

<style>

.inner_custom{
            display:flex;
            justify-content:center;
            align-items:center;
            flex-direction:column;
            text-align:justify;
            max-width: 400px;
            margin:0 auto
        }
        .outer_custom{
            max-height:37.5vh;
            overflow-y:auto
        }
</style>
