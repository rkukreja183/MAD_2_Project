<template>
    <div class="container d-flex justify-content-center align-items-center" style="height: 100vh; ">
        <div>
            <h2>Sign Up</h2>
            <form class="form-control" @submit.prevent='register'>
                <div class="mb-3">
                    <label for="user_name" class="form-label">Your Name</label>
                    <input type="text" class="form-control" id="user_name" name="user_name" required
                        v-model="register_details.user_name">
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" name="email" required
                        v-model="register_details.email">
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Password</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" name="password" required
                        v-model="register_details.password">
                    <div v-if='message' style="color:red">{{ message }}</div>
                </div>
                <button type="submit" class="btn btn-primary">Sign Up</button>
                <div><a href="/">Go Back</a></div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            register_details: {
                "user_name": null,
                "email": null,
                "password": null,
            },
            message: null
        }
    },
    methods: {
        async register() {
            this.message = null
            const res = await fetch('http://127.0.0.1:5000/user-register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.register_details)
            })
            const data = await res.json()
            if (res.ok) {
                if (res.status == 200) {
                    this.$router.push({ name: 'login' })
                }
            } else {
                this.message = data.message
            }
        }
    }
}
</script>