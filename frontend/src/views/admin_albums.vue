<template>
    <div class="container" style="margin-top:70px">
    <div style="display: flex; justify-content: space-between;">
        <h2 style="display:inline-block">All Albums</h2>
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
            <th scope="col">Artist</th>
            <th scope="col">Songs</th>
            <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(album,index) in albums" v-if="!search_value">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ album.album_name }}</td>
            <td>{{ album.artist }}</td>
            <td>{{ album.songs.length }}</td>
            <td><router-link :to="{name:'album_page', params:{id:album.album_id}}" class="btn btn-outline-info">View</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':!album.flag, 'btn-outline-success':album.flag}" @click="flag_album(album.album_id)">{{ album.flag ? 'Unflag' : 'Flag' }}</button></td>
            </tr>
            <tr v-for="(album,index) in album_results" v-if="search_value">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ album.album_name }}</td>
            <td>{{ album.artist }}</td>
            <td>{{ album.songs.length }}</td>
            <td><router-link :to="{name:'album_page', params:{id:album.album_id}}" class="btn btn-outline-info">View</router-link> 
                <button :class="{'btn':true ,'btn-outline-danger':!album.flag, 'btn-outline-success':album.flag}" @click="flag_album(album.album_id)">{{ album.flag ? 'Unflag' : 'Flag' }}</button></td>
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
            albums:null,
            search_value:'',
            album_results:[]
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/admin_login')
        }
        else{
             this.get_all_albums()
        }
    
    },
    methods:{
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
        async flag_album(id){
            const res= await fetch(`http://127.0.0.1:5000/admin_flag/${id}?option=album`,{
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
                    this.album_results = this.albums.filter(album => searchEx.test(album.album_name));
                }
            else{
                this.album_results=[]
            }    
        }
    }
}
</script>