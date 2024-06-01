<template>
<div class="container-fluid" style="margin-top: 70px;">
    <div class="row">
            <h3>Playlists</h3>
                <b-button v-b-modal.modal-2 @click="show_modal2()">Create Playlist</b-button>
                <b-modal
                id="modal-2"
                ref="modal"
                title="Name your Playlist"
                @show="resetModal2"
                @hidden="resetModal2"
                @ok="handleOk2"
                hide-header-close
                >
                <form ref="form" @submit.stop.prevent="handleSubmit2">
                    <b-form-group
                    label="Playlist Name"
                    label-for="name-input2"
                    invalid-feedback="Playlist Name is required"
                    :state="nameState2"
                    >
                    <b-form-input
                        id="name-input2"
                        v-model="new_playlist_name"
                        :state="nameState2"
                        required
                    ></b-form-input>
                    </b-form-group>
                </form>
                </b-modal>  
    </div>        
    <div class="row">
        <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Songs</th>
                <th scope="col">View</th>
                <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(playlist,index) in playlists" :key="playlist.p_id">
                <th scope="row">{{ index+1 }}</th>
                <td>{{ playlist.playlist_name }} <i class="bi bi-pencil-square" v-b-modal.modal-1 @click="show_modal(playlist.p_id)"></i></td>
                <td>{{ playlist.songs.length }}</td>
                <td><router-link  :to="{name:'playlist', params: { id: playlist.p_id } }" class="btn btn-outline-success">View</router-link></td>
                <td>
                    <router-link :to="{name:'add_to_playlist', params:{playlist_id: playlist.p_id}}" class="btn btn-outline-info">Edit</router-link> 
                    <button class="btn btn-outline-danger" @click="delete_playlist(playlist.p_id)">Delete</button>
                </td>
                </tr>
            </tbody>
        </table> 
    </div>
    <div>  
                <b-modal ref="delete_success" title="Delete successful" hide-header-close @ok="refresh()" >
                <p>Deleted Sucessully</p>
                </b-modal>
         </div>

         <div>
                <b-modal
                id="modal-1"
                ref="modal"
                title="Change Playlist Name"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOk"
                hide-header-close
                >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                    <b-form-group
                    label="Playlist Name"
                    label-for="name-input"
                    invalid-feedback="Playlist Name is required"
                    :state="nameState"
                    >
                    <b-form-input
                        id="name-input"
                        v-model="playlist_name"
                        :state="nameState"
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
             auth_token:null,
             playlists:null,
             deleteBox:'',
             playlist_name:null,
             nameState:null,
             p_id:null,
             nameState2:null,
             new_playlist_name:null
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.get_playlists()
        }
    },
    methods:{
        async get_playlists(){
            const res= await fetch('http://127.0.0.1:5000/api/playlist?option=all',{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.playlists=data
                console.log('fetched')
            }
            else{
                console.log('error')
            }
        },
        show_modal(p_id){
                this.$bvModal.show('modal-1')
                this.p_id=p_id
            },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.nameState = valid
        return valid
      },
      resetModal() {
        this.playlist_name = ''
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
        const res= await fetch(`http://127.0.0.1:5000/api/add_playlist/0/${this.p_id}?option=change`,
                    {
                        method:'PUT',
                        headers : {
                           'Content-Type': 'application/json',
                           'Authentication-Token':this.auth_token
                               },
                        body: JSON.stringify({
                        playlist_name: this.playlist_name,
                        })
                        
                    })

        const data= await res.json()
        if (res.ok){
            this.refresh()
        }
        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
    },
        async delete_playlist(p_id){
            this.deleteBox = ''
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete the Playlist', {
          id:'delete_playlist',
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
                const res=await fetch(`http://127.0.0.1:5000/api/delete_playlist/${p_id}`,{
                    method:'DELETE',
                    headers:{
                        'Authentication-Token':this.auth_token
                    }
                })
                const data= await res.json()
                if (res.ok){
                     this.$bvModal.hide('delete_playlist')
                     this.$refs.delete_success.show()
                }
                else{
                    alert('An error ocurred')
                }
            }
            else{
                this.$bvModal.close('delete_playlist')
            }
          })
          .catch(err => {
            // An error occurred
          })
        },
        refresh(){
        this.$router.go(0)
    },
    show_modal2(){
                this.$bvModal.show('modal-2')
            },
      checkFormValidity2() {
        const valid = this.$refs.form.checkValidity()
        this.nameState2 = valid
        return valid
      },
      resetModal2() {
        this.new_playlist_name = ''
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
        const res= await fetch('http://127.0.0.1:5000/api/playlist',
                    {
                        method:'POST',
                        headers : {
                           'Content-Type': 'application/json',
                           'Authentication-Token':this.auth_token
                               },
                        body: JSON.stringify({
                        playlist_name: this.new_playlist_name,
                        })
                        
                    })

        const data= await res.json()
        if (res.ok){
            const playlist_id=data.playlist_id
            this.$router.push({name:'add_to_playlist', params:{playlist_id:playlist_id}})
        }
        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
    }
    }
}
</script>