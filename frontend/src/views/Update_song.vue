<template>
    <div class="container-fluid" style="margin-top:70px">
        <div>
            <form @submit.prevent="upload_files()" class="form-control" required>
                <div class="container">
                    <div class="row mt-4" style="border:solid 1px;border-radius: 5px;">
                        <div class="col-12">
                            Create a New Release
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-7">
                            <div class="row">
                                <div class="form-floating-padding-y">
                                    <input type="text" class="form-control" id="floatingInput" placeholder="abc"
                                        v-model="song_details.song_name" required>
                                    <label for="floatingInput">Name your creation</label>
                                </div>
                            </div>
                            <div class="row mt-4">
                                <div class="btn-group-horizontal" role="group"
                                    aria-label="Horizontal radio toggle button group">
                                    <input type="radio" class="btn-check" name="song_option" id="album"
                                        autocomplete="off" v-model="song_option" value="album" required :checked="check_song_option('album')">
                                    <label class="btn btn-outline-primary" for="album">Album</label>
                                    <input type="radio" class="btn-check" name="song_option" id="song"
                                        autocomplete="off" v-model="song_option" value="single" required  :checked="check_song_option('single')">
                                    <label class="btn btn-outline-primary" for="song">Single</label>
                                </div>
                                <div class="row" v-if="song_option == 'album'">
                                    <h5>Choose an Album</h5>
                                    <div v-if="albums.length>0">
                                    <ul class="list-group">
                                        <li class="list-group-item" v-for="album in albums" v-if="!album.flag">
                                            <input class="form-check-input me-1" type="radio" name="album_id"
                                                :value="album.album_id" id="firstRadio" v-model="song_details.album_id" required>
                                            <label class="form-check-label" for="firstRadio">{{ album.album_name }}</label>
                                        </li>
                                    </ul>
                                    </div>
                                    <div v-else>
                                         No Albums created yet
                                    </div>
                                </div>
                              </div>  
                                <div class="row mt-4">
                                    <div class="mb-3">
                                        <audio :src="song_details.path" controls></audio>
                                        <label for="formFile" class="form-label">Change the audio file</label>
                                        <input class="form-control" type="file" id="formFile" ref='audiofile'
                                            accept="audio/mp3">

                                    </div>
                                </div>
                            </div>

                        <div class="col-5">
                            <div class="row h-100">
                                <div class="col-12">
                                    <div class="mb-3">
                                        <img :src="song_details.poster">
                                        <label for="formFile" class="form-label">Change the poster</label>
                                        <input class="form-control" type="file" id="formFile" ref="posterfile"
                                            accept="image/jpeg, image/png">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                        <div class="row mt-4">
                            <div class="col-12">
                                <div class="form-floating">
                                    <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea2"
                                        style="height: 100px" v-model="song_details.lyrics" required ></textarea>
                                    <label for="floatingTextarea2">Add Lyrics</label>
                                </div>
                            </div>
                        </div>
                    <!-- <div class="row mt-4">
                        <div class="col-4">

                        </div>
                    </div> -->
                    <div class="row mt-4">
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text">
                                        <input type="radio" class="btn-check" name="vbtn-radio" id="vbtn-radio1" autocomplete="off" v-model="song_details.genre" value="Pop" required :checked="check_genre('Pop')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio1">Pop</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text">
                                        <input type="radio" class="btn-check" name="vbtn-radio" id="vbtn-radio2" autocomplete="off" v-model="song_details.genre" value="Jazz" required :checked="check_genre('Jazz')"> 
                                        <label class="btn btn-outline-dark" for="vbtn-radio2">Jazz</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio3" autocomplete="off" v-model="song_details.genre" value="Classical_Music"
                                            required :checked="check_genre('Classical_Music')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio3">Classical Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio4" autocomplete="off" v-model="song_details.genre" value="R&B" required :checked="check_genre('R&B')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio4">R&B</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio5" autocomplete="off" v-model="song_details.genre"
                                            value="Dance/Electronic_Music" required :checked="check_genre('Dance/Electronic_Music')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio5">Dance/Electronic Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio6" autocomplete="off" v-model="song_details.genre" value="Indie" required :checked="check_genre('Indie')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio6">Indie</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio7" autocomplete="off" v-model="song_details.genre" value="Country_Music"
                                            required :checked="check_genre('Country_Music')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio7">Country Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="..." class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio8" autocomplete="off" v-model="song_details.genre" value="Soul" required :checked="check_genre('Soul')">
                                        <label class="btn btn-outline-dark" for="vbtn-radio8">Soul</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-12 text-end">
                            <button class="btn btn-outline-primary" type="submit">Update</button>
                        </div>
                   </div>
                   </div>
                </form>
         </div>

         <div>  
                <b-modal ref="myModal" title="Song Updated" hide-header-close @ok="goBack">
                <p>Your song has been successfully updated.</p>
                </b-modal>
         </div>
    </div>
</template>

<script>
export default {
    props: ['song_id'],
    data() {
        return {
            song_details: null,
            song_option:null,
            albums:null,
            formdata:null,
            audio_file:null,
            poster_file:null,
            auth_token:null
        }
    },
    async created() {
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else {    
        const res = await fetch(`http://127.0.01:5000/song/${this.song_id}`,{
            headers: {
                        'Authentication-Token': this.auth_token
                    }
        })
        const data = await res.json()
        if (res.ok) {
            this.song_details = data
            console.log(data)
            if (!this.song_details.album_id) {
                this.song_option = 'single'
            }
            else {
                this.song_option = 'album'
                this.fetch_albums()
            }
            this.song_details.path='/src/assets/songs/'+this.song_details.path
            this.song_details.poster='/src/assets/posters/'+ this.song_details.poster
        }
        else {
            console.log('error')
        }}
    },
    methods: {
        check_song_option(option) {
            return option == this.song_option
        },
        check_album_id(id) {
            return id == this.song_details.album_id
        },
        check_genre(genre){
            return genre=this.song_details.genre
        },
        async fetch_albums() {
            const res = await fetch(`http://127.0.0.1:5000/api/album?option=all`,
                    { headers: {
                        'Authentication-Token': this.auth_token
                    }})
            const data = await res.json()
            console.log('data is fetched')
            if (res.ok) {
                this.albums = data
                console.log(data)
            }
            else { console.log("error") }
        },

        async upload_files() {
            this.formdata = new FormData()
            if (this.$refs.audiofile.files.length>0){
                this.audio_file = this.$refs.audiofile.files[0]
            }
            else{
                this.audio_file=null
            }
            if (this.$refs.posterfile.files.length>0){
                this.poster_file = this.$refs.posterfile.files[0]
            }
            else{
                this.poster_file=null
            }
            this.formdata.append('audio_file', this.audio_file)
            this.formdata.append('poster_file', this.poster_file)
            this.formdata.append('song_name', this.song_details.song_name)
            this.formdata.append('song_option', this.song_option)
            this.formdata.append('album_id', this.song_details.album_id)
            this.formdata.append('lyrics', this.song_details.lyrics)
            this.formdata.append('genre', this.song_details.genre)
            console.log(this.audio_file,this.poster_file)
            const res = await fetch(`http://127.0.0.1:5000/api/update_song/${this.song_details.song_id}`,
                {
                    method: 'PUT',
                    body: this.formdata,
                    headers: {
                        'Authentication-Token': this.auth_token
                    }
                })
            if (res.ok) { this.$refs.myModal.show(); }
            else { console.log('error') }
        },
        goBack(){
            this.$refs.myModal.hide()
            this.$router.go(-1)
        }
    },
    watch:{
        song_option(newValue,oldValue){
            if (newValue=='album'){
                this.fetch_albums()
            }
        }
    }
}
</script>