<template>
    <div style="margin-top:70px" class="container-fluid">
        <div class='container-fluid'>
            <h2>Creator Signup</h2>
             <h5>Terms and Conditions</h5>
             <ul>
                <li>You can upload songs, creator Albums</li>
                <li>Users can Flag your songs if they feel that the song violated community guidelines</li>
                <li>Admin will be notified of the flags given to your songs and the admin can decide to hide the songs from other users</li>
                <li>Admin can also suspend your account</li>
            </ul>
             
        </div>
        <div class='container' style='height: 100vh;width:100%'>
                <div>
                    <form class="form-control" @submit.prevent='creator_signup'>
                        <div class="mb-3">
                                                <label for="formFile" class="form-label">Upload a Profile picture</label>
                                                <input class="form-control" type="file" id="formFile" required ref="profile"
                                                    accept="image/jpeg, image/png">
                                            </div>
                        
                        <button type="submit" class="btn btn-primary">Signup</button>
                        <div><router-link :to="{name:'dashboard'}">Go Back</router-link></div>
                    </form>
                </div>
            </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            formdata:null,
            profile_file:null
        }
    },
    methods:{
        async creator_signup(){
            this.formdata = new FormData()
            this.profile_file = this.$refs.profile.files[0]
            this.formdata.append('profile', this.profile_file)
             const res= await fetch('http://127.0.0.1:5000/creator_signup',{
                method:'POST',
                body: this.formdata,
                headers:{
                    'Authentication-Token':localStorage.getItem('auth-token')
                }
             })
             if (res.ok){
                localStorage.setItem('roles','creator')
                this.$router.push({name:'creatorDashboard'})
             }
         }
    }
}
</script>