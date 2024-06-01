<template>
    <div class="container" style="margin-top:70px">
    <div style="display: flex; justify-content: space-between;">
        <h2>All Artists</h2>
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
            <th scope="col">Songs</th>
            <th scope="col">Albums</th>
            <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(artist,index) in artists" v-if="!search_value">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ artist.user_name }}</td>
            <td>{{ artist.songs.length }}</td>
            <td>{{ artist.albums.length }}</td>
            <td><router-link :to="{name:'artist_page', params:{id:artist.id}}" class="btn btn-outline-info">View</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':artist.active, 'btn-outline-success':!artist.active}" @click="flag_artist(artist.id)">{{ artist.active ? 'Flag' : 'Unflag' }}</button></td>
            </tr>
            <tr v-for="(artist,index) in artist_results" v-if="search_value">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ artist.user_name }}</td>
            <td>{{ artist.songs.length }}</td>
            <td>{{ artist.albums.length }}</td>
            <td><router-link :to="{name:'artist_page', params:{id:artist.id}}" class="btn btn-outline-info">View</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':artist.active, 'btn-outline-success':!artist.active}" @click="flag_artist(artist.id)">{{ artist.active ? 'Flag' : 'Unflag' }}</button></td>
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
            artists:null,
            search_value:'',
            artist_results:[]
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/admin_login')
        }
        else{
             this.get_all_artists()
        }
    
    },
    methods:{
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
        },
        async flag_artist(id){
            const res= await fetch(`http://127.0.0.1:5000/admin_flag/${id}?option=artist`,{
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
                    this.artist_results = this.artists.filter(artist => searchEx.test(artist.user_name));
                }
            else{
                this.artist_results=[]
            }    
        }
    }
}
</script>