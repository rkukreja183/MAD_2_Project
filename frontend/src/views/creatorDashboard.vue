<template>
<div class="container-fluid" style="margin-top:70px">

    <div class="row" style="margin-top:13px">
        <div class="mb-1">
            <div>
                <router-link :to="{name:'upload_song'}" class="btn btn-primary" style="width:100%;background-color: grey;">Upload Song</router-link>
                <b-button v-b-modal.modal-1 @click="show_modal()" style="width:100%">Create Album</b-button>
                <b-modal
                id="modal-1"
                ref="modal"
                title="Name your Album"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOk"
                hide-header-close
                >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                    <b-form-group
                    label="Album Name"
                    label-for="name-input"
                    invalid-feedback="Album Name is required"
                    :state="nameState"
                    >
                    <b-form-input
                        id="name-input"
                        v-model="name"
                        :state="nameState"
                        required
                    ></b-form-input>
                    </b-form-group>

                </form>
                </b-modal>
            </div>
        </div>
    </div>


    <div class="row">
        <div class="col-3">
                    <div class="card border-info mb-3 mt-2" style="max-width: 20rem;">
                        <div class="card-header text-center">Streams</div>
                        <div class="card-body text-center">
                            <h1 class="card-title">{{ creator_dets.total_streams }}</h1>
                        </div>
                    </div>
        </div>            
            
        <div class="col-3">
                <div class="card border-info mb-3 mt-2" style="max-width: 20rem;">
                    <div class="card-header text-center">Songs</div>
                    <div class="card-body text-center">
                        <h1 class="card-title">{{ songs.length }}</h1>
                    </div>
                </div>   
        </div>               

        <div class="col-3">
                <div class="card border-info mb-3 mt-2" style="max-width: 20rem;">
                    <div class="card-header text-center">Albums</div>
                    <div class="card-body text-center">
                        <h1 class="card-title">{{ albums.length }}</h1>
                    </div>
                </div>  
        </div>        
 
        <div class="col-3">
                <div class="card border-info mb-3 mt-2" style="max-width: 20rem;">
                    <div class="card-header text-center">Followers</div>
                    <div class="card-body text-center">
                        <h1 class="card-title">{{ followers }}</h1>
                    </div>
                </div> 
        </div>           
    </div>

    <div class="row">
            <div class="col-12">
                    <div>
                        <ul class="nav nav-underline">
                        <li class="nav-item">
                            <button :class="{ 'nav-link': true, 'active': option === 'songs' }" aria-current="page"  @click="option='songs'" >Songs</button>
                        </li>
                        <li class="nav-item">
                            <button :class="{ 'nav-link': true, 'active': option === 'albums' }" aria-current="page" @click="option='albums'" >Albums</button>
                        </li>
                        <li class="nav-item">
                            <button :class="{ 'nav-link': true, 'active': option === 'top_songs' }" aria-current="page"  @click="option='top_songs'" >Top Songs</button>
                        </li>
                        <li class="nav-item">
                            <button :class="{ 'nav-link': true, 'active': option === 'new_songs' }" aria-current="page"  @click="option='new_songs'" >Recent Uploads</button>
                        </li>
                        </ul>
                    </div>

                    <div>
                        <div v-if="option==='songs'">
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Flags</th>
                                    <th scope="col">Flagged By Admin</th>
                                    <th scope="col">Actions</th>
                                    </tr>
                                </thead>
                                    <tbody>
                                        <tr v-for="(song,index) in songs">
                                        <th scope="row">{{ index+1 }}</th>
                                        <td>{{ song.song_name }}</td>
                                        <td>{{ song.total_rating }}</td>
                                        <td>{{ song.user_flags }}</td>
                                        <td>{{ song.flag }}</td>
                                        <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link><router-link class="btn btn-outline-info btn-sm" :to="{ name: 'update_song', params: { song_id: song.song_id } }">Update</router-link> <button class="btn btn-outline-danger btn-sm" @click="delete_song(song.song_id)" >Delete</button></td>
                                        </tr>
                                    </tbody>
                                    </table>
                        
                        </div>

                        <div v-else-if="option==='albums'">
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Songs</th>
                                    <th scope="col">Flagged By Admin</th>
                                    <th scope="col">View</th>
                                    <th scope="col">Actions</th>
                                    </tr>
                                </thead>
                                    <tbody>
                                        <tr v-for="(album,index) in albums">
                                        <th scope="row">{{ index+1 }}</th>
                                        <td>{{ album.album_name }} <i class="bi bi-pencil-square" v-b-modal.name_change @click="show_modal2(album.album_id)"></i></td>
                                        <td>{{ album.songs.length }}</td>
                                        <td>{{ album.flag }}</td>
                                        <td><router-link  :to="{name:'view_album', params: { id:album.album_id } }" class="btn btn-outline-success">View</router-link></td>
                                        <td><router-link class="btn btn-outline-info btn-sm" :to="{ name: 'add_to_album', params: { album_id: album.album_id } }">Add Songs</router-link> <button class="btn btn-outline-danger btn-sm" @click="delete_album(album.album_id)" >Delete</button></td>
                                        </tr>
                                    </tbody>
                                    </table>
                        
                        </div>

                        <div v-if="option==='top_songs'">
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Flags</th>
                                    <th scope="col">Flagged By Admin</th>
                                    <th scope="col">Actions</th>
                                    </tr>
                                </thead>
                                    <tbody>
                                        <tr v-for="(song,index) in top_songs">
                                        <th scope="row">{{ index+1 }}</th>
                                        <td>{{ song.song_name }}</td>
                                        <td>{{ song.total_rating }}</td>
                                        <td>{{ song.user_flags }}</td>
                                        <td>{{ song.flag }}</td>
                                        <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link><router-link class="btn btn-outline-info btn-sm" :to="{ name: 'update_song', params: { song_id: song.song_id } }">Update</router-link> <button class="btn btn-outline-danger btn-sm" @click="delete_song(song.song_id)" >Delete</button></td>
                                        </tr>
                                    </tbody>
                                    </table>
                        
                        </div>

                        <div v-if="option==='new_songs'">
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Flags</th>
                                    <th scope="col">Flagged By Admin</th>
                                    <th scope="col">Actions</th>
                                    </tr>
                                </thead>
                                    <tbody>
                                        <tr v-for="(song,index) in new_uploads">
                                        <th scope="row">{{ index+1 }}</th>
                                        <td>{{ song.song_name }}</td>
                                        <td>{{ song.total_rating }}</td>
                                        <td>{{ song.user_flags }}</td>
                                        <td>{{ song.flag }}</td>
                                        <td><router-link class="btn btn-outline-primary btn-sm" :to="{name:'song_page', params:{id:song.song_id}}"><i class="bi bi-play">Play</i></router-link><router-link class="btn btn-outline-info btn-sm" :to="{ name: 'update_song', params: { song_id: song.song_id } }">Update</router-link> <button class="btn btn-outline-danger btn-sm" @click="delete_song(song.song_id)" >Delete</button></td>
                                        </tr>
                                    </tbody>
                                    </table>
                        
                        </div>
                    </div>
            </div>
        </div>  
        
        <div>  
                <b-modal ref="delete_success" title="Delete successful" hide-header-close @ok="refresh()" >
                <p>Deleted Sucessully</p>
                </b-modal>
         </div>

         <div>
                <b-modal
                id="name-change"
                ref="name-change"
                title="Change Album Name"
                @show="resetModal2"
                @hidden="resetModal2"
                @ok="handleOk2"
                hide-header-close
                >
                <form ref="form" @submit.stop.prevent="handleSubmit2">
                    <b-form-group
                    label="Album Name"
                    label-for="new_album_name"
                    invalid-feedback="Album Name is required"
                    :state="nameState2"
                    >
                    <b-form-input
                        id="new_album_name"
                        v-model="new_album_name"
                        :state="nameState2"
                        required
                    ></b-form-input>
                    </b-form-group>
                </form>
                </b-modal>
            </div>
    </div>
   

 



</template>

<script>
export default{
    data(){
        return{
        name:null,
        nameState:null,
        auth_token:null,
        creator_dets:null,
        songs:null,
        albums:null,
        new_uploads:null,
        top_songs:null,
        id:null,
        option:'songs',
        deleteBox:'',
        nameState2:null,
        new_album_name:null,
        album_id:null,
        followers:null,
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_creator_details()
        }
    },
    methods:{
        async get_creator_details(){
            const res= await fetch(`http://127.0.0.1:5000/creator_details`, {
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data=await res.json()
            if (res.ok){
                this.creator_dets=data 
                this.id=data.id
            }
            else{
                console.log('error')
            }
        },

        async get_creator_uploads(creator_id){
                  const res= await fetch(`http://127.0.0.1:5000/api/artist/${creator_id}`, {
                    headers:{
                        'Authentication-Token':this.auth_token
                    }
                  })
                  const data= await res.json()
                  if (res.ok){
                      this.songs=data.songs
                      this.albums=data.albums
                      this.new_uploads=data.new_uploads
                      this.top_songs=data.top_songs
                      this.followers=data.follower_len
                      console.log(this.top_songs)
                  }
                  else{
                    console.log('error')
                  }
        },
            show_modal(){
                this.$bvModal.show()
            },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.nameState = valid
        return valid
      },
      resetModal() {
        this.name = ''
        this.nameState = null
      },
      handleOk(bvModalEvent) {
        // Prevent modal from closing
        bvModalEvent.preventDefault()
        // Trigger submit handler
        this.handleSubmit()
      },
      async handleSubmit() {
        // Exit when the form isn't valid
        if (!this.checkFormValidity()) {
          return
        }
        console.log(this.name)
        const res= await fetch('http://127.0.0.1:5000/api/album',
                    {
                        method:'POST',
                        headers : {
                           'Content-Type': 'application/json',
                           'Authentication-Token':this.auth_token
                               },
                        body: JSON.stringify({
                        album_name: this.name,
                        })
                        
                    })

        const data= await res.json()
        if (res.ok){
            const album_id=data.album_id
            this.$router.push({name:'add_to_album', params:{album_id:album_id}})
        }
        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
    }, 
    async delete_song(song_id){
        this.deleteBox = ''
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete the song', {
          id:'delete_song',
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'YES',
          cancelTitle: 'NO',
          footerClass: 'p-2',
          hideHeaderClose: true,
          centered: true
        })
          .then( async value => {
            if (value===true){
                const res=await fetch(`http://127.0.0.1:5000/api/delete_song/${song_id}`,{
                    method:'DELETE',
                    headers:{
                        'Authentication-Token':this.auth_token
                    }
                })
                const data= await res.json()
                if (res.ok){
                     this.$bvModal.hide('delete_song')
                     this.$refs.delete_success.show()
                }
                else{
                    alert('An error ocurred')
                }
            }
            else{
                this.$bvModal.close('delete_song')
            }
          })
          .catch(err => {
            // An error occurred
          })
    },
    refresh(){
        this.$router.go(0)
    },
    async delete_album(album_id){
        this.deleteBox = ''
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete the Album', {
          id:'delete_album',
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'YES',
          cancelTitle: 'NO',
          footerClass: 'p-2',
          hideHeaderClose: true,
          centered: true
        })
          .then( async value => {
            if (value===true){
                const res=await fetch(`http://127.0.0.1:5000/api/delete_album/${album_id}`,{
                    method:'DELETE',
                    headers:{
                        'Authentication-Token':this.auth_token
                    }
                })
                const data= await res.json()
                if (res.ok){
                     this.$bvModal.hide('delete_album')
                     this.$refs.delete_success.show()
                }
                else{
                    alert('An error ocurred')
                }
            }
            else{
                this.$bvModal.close('delete_album')
            }
          })
          .catch(err => {
            // An error occurred
          })
    },
    show_modal2(album_id){
                this.$bvModal.show('name-change')
                this.album_id=album_id
            },
      checkFormValidity2() {
        const valid = this.$refs.form.checkValidity()
        this.nameState2 = valid
        return valid
      },
      resetModal2() {
        this.new_album_name = ''
        this.nameState2 = null
      },
      handleOk2(bvModalEvent) {
        // Prevent modal from closing
        bvModalEvent.preventDefault()
        // Trigger submit handler
        this.handleSubmit2()
      },
      async handleSubmit2() {
        // Exit when the form isn't valid
        if (!this.checkFormValidity2()) {
          return
        }
        const res= await fetch(`http://127.0.0.1:5000/api/add_album/0/${this.album_id}?option=change`,
                    {
                        method:'PUT',
                        headers : {
                           'Content-Type': 'application/json',
                           'Authentication-Token':this.auth_token
                               },
                        body: JSON.stringify({
                        album_name: this.new_album_name,
                        })
                        
                    })

        const data= await res.json()
        if (res.ok){
            this.refresh()
        }
        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
    }
    
},
     watch: {
        id (newValue,oldValue){
            if (newValue){
                this.get_creator_uploads(newValue)
                console.log('changed')
            }
        }
        }

}
</script>