<template>
    <div class='container d-flex justify-content-center align-items-center' style='height: 100vh;'>
        <div>
            <h2>Admin Login</h2>
            <form class="form-control" @submit.prevent='login'>
                <div class="mb-3">
                    <label for="email" class="form-label">Email ID</label>
                    <input type="email" class="form-control" id="email" name="user_email" required
                        v-model="login_details.email">
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Password</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" name="password" required
                        v-model="login_details.password">
                    <div v-if='message' style="color:red">{{ message }}</div>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
                <div><a href="/">Go Back</a></div>
            </form>
        </div>
    </div>
</template>

<script>
export default{
    data() {
        return {
            login_details: {
                "email": null,
                "password": null,
            },
            message: null
        }
    },
    methods: {
        async login() {
            this.message = null
            console.log('hello')
            if (this.login_details.email!='admin@email.com'){
                this.message='Wrong Admin Email'
            }
            else{
            const res = await fetch(`http://127.0.0.1:5000/user-login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.login_details)
            })
            const data = await res.json()
            if (res.ok) {
                if (res.status == 200) {
                    if(data.role!='admin'){
                        this.message='Wrong Password'
                    }
                    else{
                    localStorage.setItem('auth-token', data.token)
                    localStorage.setItem('roles',data.role)
                    localStorage.setItem('reload',1)
                    this.$router.push({ name: 'admin_dashboard'})
                    }
                }
            } else {
                this.message = data.message
            }
        }
        }
    }
}
</script>