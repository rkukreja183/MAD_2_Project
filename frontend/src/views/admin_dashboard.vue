
<template>
    <div class="container" style="margin-top: 70px;">

        <div class="row mt-2" style="border: 1px solid;width:100%;border-color: #e0f2f1;">
            <div class="col-2">
                <div class="card" style="border:none">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary">Users</h6>
                    <button class="btn btn-light" @click="get_uploads('users')"><h2 class="card-title">{{ numbers.users }}</h2></button>
                </div>
                </div>
            </div>
            <div class="col-3">
                <div class="card" style="border:none">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary">Creators</h6>
                    <button class="btn btn-light"  @click="get_uploads('creators')"><h2 class="card-title">{{ numbers.artists }}</h2></button>
                </div>
                </div>
            </div>
            <div class="col-2">
                <div class="card" style="border:none">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary">Songs</h6>
                    <button class="btn btn-light"  @click="get_uploads('songs')"><h2 class="card-title">{{ numbers.songs }}</h2></button>
                </div>
                </div>
            </div>
            <div class="col-3">
                <div class="card" style="border:none">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary">Albums</h6>
                    <button class="btn btn-light disabled"><h2 class="card-title">{{ numbers.albums }}</h2></button>
                </div>
                </div>
            </div>
            <div class="col-2">
                <div class="card" style="border:none">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary" >Genres</h6>
                    <button class="btn btn-light" @click="get_uploads('genres')"><h2 class="card-title">7</h2></button>
                </div>
                </div>
            </div>
        </div>    

        <div class="row mt-3 justify-content-center">
                        <div style="height:500px;width:800px">
                            <canvas id="chart" ></canvas>
                        </div>
        </div>
        
  </div>
</template>

<script>
export default{
    data(){
        return{
            auth_token:null,
            genre_songs:null,
            chart:'line',
            ChartInstance:null,
            numbers:null,
            title:''
        }
    },
    created(){
        this.auth_token = localStorage.getItem('auth-token')
        const reload= localStorage.getItem('reload')
        if (reload==1){
            localStorage.setItem('reload',0)
            window.location.reload()
        }
        if (this.auth_token && reload==0) {
            this.get_numbers()
            
           
        }
        else{
            this.$router.push('/admin_login')
        }
    
    },
    methods:{
    async get_uploads(option){
        if (option=='songs'){
        const res=await fetch(`http://127.0.0.1:5000/uploads?option=${option}`,{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
            this.chart='line'
            this.title='New Songs Over the last Week'
            this.create_chart(data)
            console.log(data)
        }
    }
        if (option=='users'){
            const res=await fetch(`http://127.0.0.1:5000/uploads?option=${option}`,{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
            this.chart='line'
            this.title='New Users Over the last Week'
            this.create_chart(data)
            console.log(data)
        }
        }
        if (option=='genres'){
            const res= await fetch('http://127.0.0.1:5000/genre_songs',{
                headers:{
                    'Authentication-Token':this.auth_token
                }
            })
            const data= await res.json()
            if (res.ok){
                this.genre_songs=data
                this.title='Genre-wise distribution of Songs'
                this.chart='doughnut'
                this.create_chart(this.genre_songs)
            }
        }
        if (option=='creators'){
            const res=await fetch(`http://127.0.0.1:5000/uploads?option=${option}`,{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
            this.chart='line'
            this.title='New Creators Over the last Week'
            this.create_chart(data)
            console.log(data)
        }
        }
        
    },
    create_chart(data){
        if (this.ChartInstance){
            this.ChartInstance.destroy()
        }
        const ctx = document.getElementById('chart').getContext('2d');
        
        this.ChartInstance=new Chart(ctx,{
            type:this.chart,
            data:{
                labels:Object.keys(data),
                datasets: [{
                    label: this.title,
                    data: Object.values(data),
                    fill: false,
                    // borderColor: 'rgb(75, 192, 192)',
                    borderColor: 'black',
                    tension: 0.1,
                    backgroundColor: [
                            "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#f7b6d2", "#c49c94", "#dbdb8d"
                        ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins:{
          }
        } 
        })
    },
    async get_numbers(){
        const res= await fetch(`http://127.0.0.1:5000/get_numbers`,{
            headers:{
                'Authentication-Token':this.auth_token
            }
        })
        const data= await res.json()
        if (res.ok){
             this.numbers=data
             this.get_uploads('users')
        }
    }
    },
}
</script>