<template>
    <div class="container" style="margin-top:70px">
    <div style="display: flex; justify-content: space-between;">
        <h2>All Songs</h2>
        <form class="d-flex" role="search" >
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="search_value">
        <button class="btn btn-outline-primary disabled">Search</button>
        </form>
    </div>
    <table class="table">
        <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Rating</th>
            <th scope="col">Streams</th>
            <th scope="col">User Flags</th>
            <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(song,index) in songs" v-if="!search_value">
            <th scope="row">{{ index+1 }}</th>
            <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                    <div>
                        <div style="font-size: 20px;">{{ song.song_name }}</div>
                        <div style="color:grey"> By {{ song.artist_name }}</div>
                    </div>
                </td>
            <td>{{ song.total_rating }}</td>
            <td>{{ song.plays }}</td>
            <td>{{ song.user_flags }}</td>
            <td><router-link :to="{name:'song_page', params:{id:song.song_id}}" class="btn btn-outline-info">Play</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':!song.flag, 'btn-outline-success':song.flag}" @click="flag_song(song.song_id)">{{ song.flag ? 'Unflag' : 'Flag' }}</button></td>
            </tr>
            <tr v-for="(song,index) in song_results" v-if="search_value">
            <th scope="row">{{ index+1 }}</th>
            <td style="display: flex; align-items: center;">
                    <div style="margin-right: 10px;">
                        <img :src="song.poster" alt="..." style="height: 2.8rem; width: 2.8rem;">
                    </div>
                    <div>
                        <div style="font-size: 20px;">{{ song.song_name }}</div>
                        <div style="color:grey"> By {{ song.artist_name }}</div>
                    </div>
                </td>
            <td>{{ song.total_rating }}</td>
            <td>{{ song.plays }}</td>
            <td>{{ song.user_flags }}</td>
            <td><router-link :to="{name:'song_page', params:{id:song.song_id}}" class="btn btn-outline-info">Play</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':song.flag, 'btn-outline-success':!song.flag}" @click="flag_song(song.song_id)">{{ song.flag ? 'Unflag' : 'Flag' }}</button></td>
            </tr>
            
        </tbody>
    </table>
    </div>
</template>

<script>
export default{
    data(){
        return{
            auth_token:null,
            songs:null,
            search_value:'',
            song_results:[]
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/admin_login')
        }
        else{
             this.get_all_songs()
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
                for (const song of this.songs){
                   song.poster='/src/assets/posters/'+song.poster
             }
             }
        },
        async flag_song(id){
            const res= await fetch(`http://127.0.0.1:5000/admin_flag/${id}?option=song`,{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.$router.go(0)
            }
        }
    },
    watch:{
        search_value(newValue,oldValue){
            if (newValue!=''){
                    const searchEx = new RegExp(this.search_value, 'i')
                    this.song_results = this.songs.filter(song => searchEx.test(song.song_name));
                }
            else{
                this.song_results=[]
            }    
        }
    }
}
</script>