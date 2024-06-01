<template>
    <div class="container d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div>
            <form class="form-control">
                <h1 style="text-align:center">Welcome to Meloverse</h1><br>
                <div id="passwordHelpBlock" class="form-text d-flex justify-content-center align-items-center">
                    Already a User?</div>
                <div><router-link :to="{ name: 'login' }" class="btn btn-primary" style="width:100%">Login</router-link>
                </div>
                <br>
                <div id="passwordHelpBlock" class="form-text d-flex justify-content-center align-items-center">
                    Don't Have an Account?
                </div>
                <div><router-link :to="{ name: 'register' }" class="btn btn-primary"
                        style="width:100%">Register</router-link>
                </div>
                <br>
                <div id="passwordHelpBlock" class="form-text d-flex justify-content-center align-items-center">
                    <router-link :to="{name:'admin_login'}"> Admin Login</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Welcome',
}
</script>