import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Welcome from "../views/Welcome.vue";
import Dashboard from "../views/User_dashboard.vue";
import Song from "../views/Song_page.vue";
import Upload_song from "../views/Upload_song.vue";
import Update_song from "../views/Update_song.vue";
import creatorDashboard from "../views/creatorDashboard.vue";
import Add_to_album from "../views/add_to_album.vue";
import Add_to_playlist from "../views/add_to_playlist.vue";
import Artist_page from "../views/artist_page.vue";
import Album_page from "../views/album_page.vue";
import Playlist_page from "../views/playlists_page.vue";
import Playlist from "../views/playlist.vue";
import Creators_album_page from "../views/creators_album_page.vue";
import Search from "../views/search.vue";
import Liked_songs from "../views/liked_songs.vue";
import AdminLogin from "../views/AdminLogin.vue";
import Admin_dash from "../views/admin_dashboard.vue";
import Admin_songs from "../views/admin_songs.vue";
import Admin_albums from "../views/admin_albums.vue";
import Admin_artists from "../views/admin_artists.vue";
import Followed_artists from "../views/followed_artists.vue";
import Genre_page from "../views/genre_songs.vue";
import Creator_Signup from "../views/creator_signup.vue";



Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: "/",
      component: Welcome,
      name:'welcome'
    },
    {
      path: "/login",
      component: Login,
      name: "login",
    },
    {
      path: "/register",
      component: Register,
      name: "register",
    },
    {
      path: "/dashboard",
      component: Dashboard,
      props: true,
      name: "dashboard",
    },
    {
      path: "/song/:id",
      component: Song,
      props: true,
      name: "song_page",
    },
    {
      path: "/upload",
      component: Upload_song,
      props: true,
      name: "upload_song",
    },
    {
      path: "/update_song/:song_id",
      component: Update_song,
      name: "update_song",
      props: true,
    },
    {
      path:'/creator_dashboard',
      component:creatorDashboard,
      name:'creatorDashboard',
      props:true
    },
    {
      path:'/add_to_album/:album_id',
      component:Add_to_album,
      name:'add_to_album',
      props:true
    },
    {
      path:'/add_to_playlist/:playlist_id',
      component:Add_to_playlist,
      name:'add_to_playlist',
      props:true
    },
    {
      path:'/artist/:id',
      component:Artist_page,
      name:'artist_page',
      props:true
    },
    {
      path:'/album/:id',
      component:Album_page,
      name:'album_page',
      props:true
    },
    {
      path:'/playlists',
      component:Playlist_page,
      name:'playlist_page',
      props:true
    },
    {
      path:'/playlist/:id',
      component:Playlist,
      name:'playlist',
      props:true
    },
    {
      path:'/creator_view_album/:id',
      component:Creators_album_page,
      name:'view_album',
      props:true
    },
    {
      path:'/search',
      component:Search,
      name:'search',
      props:true
    },
    {
      path:'/liked_songs',
      component:Liked_songs,
      name:'liked_songs',
      props:true
    },
    {
      path:'/admin_login',
      component:AdminLogin,
      name:'admin_login',
    },
    {
      path:'/admin_dashboard',
      component:Admin_dash,
      name:'admin_dashboard',
    },
    {
      path:'/admin_all_songs',
      component:Admin_songs,
      name:'a_all_songs',
    },
    {
      path:'/admin_all_artists',
      component:Admin_artists,
      name:'a_all_artists',
    },
    {
      path:'/admin_all_albums',
      component:Admin_albums,
      name:'a_all_albums',
    },
    {
      path:'/followed_artist',
      component:Followed_artists,
      name:'followed_artists',
    },
    {
      path:'/genre_page/:genre',
      component:Genre_page,
      name:'genre_songs',
      props:true
    },
    {
      path:'/creator_signup',
      component:Creator_Signup,
      name:'creator_signup',
    }



    
  ],
});


export default router;
