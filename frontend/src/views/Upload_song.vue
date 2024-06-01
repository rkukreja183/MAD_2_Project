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
                                        v-model="song_name" required>
                                    <label for="floatingInput">Name your creation</label>
                                </div>
                            </div>
                            <div class="row mt-4">
                                <div class="btn-group-horizontal" role="group"
                                    aria-label="Horizontal radio toggle button group">
                                    <input type="radio" class="btn-check" name="song_option" id="album"
                                        autocomplete="off" v-model="song_option" value="album" required>
                                    <label class="btn btn-outline-primary" for="album">Album</label>
                                    <input type="radio" class="btn-check" name="song_option" id="song"
                                        autocomplete="off" v-model="song_option" value="single" required>
                                    <label class="btn btn-outline-primary" for="song">Single</label>
                                </div>
                                <div class="row" v-if="song_option == 'album'">
                                    <h5>Choose an Album</h5>
                                    <div v-if="albums.length>0">
                                    <ul class="list-group">
                                        <li class="list-group-item" v-for="album in albums" v-if="!album.flag">
                                            <input class="form-check-input me-1" type="radio" name="album_id"
                                                :value="album.album_id" id="firstRadio" v-model="album_id" required>
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
                                        <label for="formFile" class="form-label">Choose an audio file</label>
                                        <input class="form-control" type="file" id="formFile" required ref='audiofile'
                                            accept="audio/mp3">
                                    </div>
                                </div>
                            </div>

                        <div class="col-5">
                            <div class="row h-100">
                                <div class="col-12">
                                    <div class="mb-3">
                                        <label for="formFile" class="form-label">Choose a poster</label>
                                        <input class="form-control" type="file" id="formFile" required ref="posterfile"
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
                                        style="height: 100px" v-model="lyrics" required></textarea>
                                    <label for="floatingTextarea2">Add Lyrics</label>
                                </div>
                            </div>
                        </div>
                    <!-- <div class="row mt-4">
                        <div class="col-4">

                        </div>
                    </div> -->
                    <div class="row mt-4">
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Pop.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text">
                                        <input type="radio" class="btn-check" name="vbtn-radio" id="vbtn-radio1" autocomplete="off" v-model="genre" value="Pop" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio1">Pop</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Jazz.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text">
                                        <input type="radio" class="btn-check" name="vbtn-radio" id="vbtn-radio2" autocomplete="off" v-model="genre" value="Jazz" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio2">Jazz</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Classical.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio3" autocomplete="off" v-model="genre" value="Classical_Music"
                                            required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio3">Classical Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Rhythm & Blues.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio4" autocomplete="off" v-model="genre" value="R&B" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio4">R&B</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Electronic.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio5" autocomplete="off" v-model="genre"
                                            value="Dance/Electronic_Music" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio5">Dance/Electronic Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Indie.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio6" autocomplete="off" v-model="genre" value="Indie" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio6">Indie</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Country.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio7" autocomplete="off" v-model="genre" value="Country_Music"
                                            required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio7">Country Music</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-3 text-center">
                            <div class="card text-bg-secondary" style="width: 100%">
                                <img src="/src/assets/genres/Soul.png" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <p class="card-text"><input type="radio" class="btn-check" name="vbtn-radio"
                                            id="vbtn-radio8" autocomplete="off" v-model="genre" value="Soul" required>
                                        <label class="btn btn-outline-dark" for="vbtn-radio8">Soul</label>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-12 text-end">
                            <button class="btn btn-outline-primary" type="submit">Create</button>
                        </div>
                   </div>
                   </div>
                </form>
         </div>
         <div>  
                <b-modal ref="myModal" title="Song Uploaded" hide-header-close @ok="goBack">
                <p>Your song has been successfully uploaded.</p>
                </b-modal>
         </div>
    </div>
</template>

<script>
export default {
    props: ['creator_id'],
    data() {
        return {
            song_name: null,
            audio_file: null,
            poster_file: null,
            song_option: null,
            album_id: null,
            show_album_names: false,
            lyrics: null,
            genre: null,
            formdata: null,
            albums: null,
            auth_token:null

        }
    },
    created() {
        this.auth_token = localStorage.getItem('auth-token')
        if (!this.auth_token) {
            this.$router.push('/login')
        }
        else{
            this.fetch_albums()
        }

    },
    methods: {
        async upload_files() {
            this.formdata = new FormData()
            this.audio_file = this.$refs.audiofile.files[0]
            this.poster_file = this.$refs.posterfile.files[0]
            this.formdata.append('audio_file', this.audio_file)
            this.formdata.append('poster_file', this.poster_file)
            this.formdata.append('song_name', this.song_name)
            this.formdata.append('song_option', this.song_option)
            this.formdata.append('album_id', this.album_id)
            this.formdata.append('lyrics', this.lyrics)
            this.formdata.append('genre', this.genre)
            const res = await fetch(`http://127.0.0.1:5000/api/song`,
                {
                    method: 'POST',
                    body: this.formdata,
                    headers: {
                        'Authentication-Token': this.auth_token
                    }
                })
            if (res.ok) { this.$refs.myModal.show(); }
            else { console.log('error') }
        },
        async fetch_albums() {
            const res = await fetch(`http://127.0.0.1:5000/api/album?option=all`,{
                headers:{
                        'Authentication-Token':this.auth_token
                }
            })
            const data = await res.json()
            if (res.ok) {
                this.albums = data
            }
            else { console.log("error") }
        },
        goBack(){
            this.$refs.myModal.hide()
            this.$router.go(-1)
        }

    },
}
</script>