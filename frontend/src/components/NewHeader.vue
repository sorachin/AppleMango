<template>
    <v-app-bar app color="#FFCB3C" height="80">
        <v-row id="nav-menus">
            <v-col align-self="center" cols="2">
                <!-- <v-toolbar-title v-on:click="home" style="cursor:grab"></v-toolbar-title> -->
                <img id="logo" v-on:click="home" style="cursor:pointer" src="../assets/applemango_logo.png"/>
            </v-col>
            <!-- <v-col align-self="center" cols="3">
                <v-select
                :select="searchFilter"
                hide-details 
                solo 
                :items="searchOptions"
                v-model="searchFilter"></v-select>
            </v-col> -->
            <v-col class="d-flex justify-space-between" align-self="center" cols="7">
                <v-text-field
                hide-details
                height="10px"
                single-line 
                solo placeholder="검색어를 입력해주세요"
                prepend-inner-icon="fa-search"
                v-model="keyword"
                @keyup.enter="search"
                id="search-bar"
                ></v-text-field>
                <div v-if="this.$store.getters.getLocation === false" class="d-flex ml-3">
                    <v-icon class="align-self-center" color="gray">fa-location-arrow</v-icon>
                </div>
                <div v-else class="d-flex ml-3">
                    <v-icon class="align-self-center" color="blue">fa-location-arrow</v-icon>
                </div>
            </v-col>
            <v-col align-self="center" cols="1">
                <v-btn @click="search" height="46">검색하기</v-btn>
            </v-col>
            <v-col cols="1" align-self="center" class="d-flex justify-end">
                <div class="d-flex align-center" v-if="this.$cookies.get('auth-token')">
                    <v-avatar size="3rem"><v-icon size="2.2rem">fa-user-circle</v-icon></v-avatar>
                    <div><strong style="font-size:18px">{{ this.$store.getters.getUserId }}</strong></div>
                </div>
            </v-col>
            <v-col align-self="center" cols="1">
                <!-- <v-icon
                class="pa-3"
                color="black" 
                v-if="this.$store.state.userType === 'Admin'"
                @click="$router.push({ name: 'AdminPage' })"
                >
                fa-user-cog
                </v-icon>
                <v-icon
                class="pa-3"
                color="black" 
                v-if="this.$cookies.get('auth-token')"
                >
                fa-envelope
                </v-icon> -->

                
                <v-menu bottom left>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        icon
                        color="black"
                        v-bind="attrs"
                        v-on="on"
                    >
                        <v-icon>fa-bars</v-icon>
                    </v-btn>
                    </template>

                    <v-list>
                        <!--Home-->
                        <v-list-item  @click="$router.push({ name: 'Home' })">
                            <v-list-item-icon>
                            <v-icon>mdi-home</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Home</v-list-item-title>
                        </v-list-item>

                        

                        <div v-if="this.$store.state.userType === 'Owner'">
                            <v-subheader>OWNER</v-subheader>
                            <!--MyStore-->
                            <v-list-item  @click="$router.push({ name: 'mystore',params: { ruid: $cookies.get('auth-token')} })">
                                <v-list-item-icon>
                                <v-icon>fas fa-utensils</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title>MyStore</v-list-item-title>
                            </v-list-item>
                            
                            <v-list-item  @click="$router.push({ name: 'comment' })">
                                <v-list-item-icon>
                                <v-icon>fab fa-instagram</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title>Instagram</v-list-item-title>
                            </v-list-item>

                            <v-list-item  @click="$router.push({ name: 'reg' })">
                                <v-list-item-icon>
                                <v-icon>far fa-plus-square</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title>Reg New Store</v-list-item-title>
                            </v-list-item>
                        </div>

                        <div v-else>
                            <v-subheader>OWNER</v-subheader>
                             <v-list-item  @click="$router.push({ name: 'reg' })">
                                <v-list-item-icon>
                                <v-icon>far fa-plus-square</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title>Reg New Store</v-list-item-title>
                            </v-list-item>
                        </div>



                        <div v-if="this.$store.state.userType === 'Admin'">
                            <v-subheader>ADMIN</v-subheader>
                            <!--MyStore-->
                            <v-list-item  @click="$router.push({ name: 'AdminPage' })">
                                <v-list-item-icon>
                                <v-icon>fa-user-cog</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title>Admin</v-list-item-title>
                            </v-list-item>
                        </div>



                        <v-subheader>USER</v-subheader>
                        <!--MyPage-->
                        <v-list-item  @click="$router.push({ name: 'mypage' })">
                            <v-list-item-icon>
                            <v-icon>fas fa-child</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Mypage</v-list-item-title>
                        </v-list-item>
                        <!--Setting-->
                        <v-list-item  @click="$router.push({ name: 'mypage' })">
                            <v-list-item-icon>
                            <v-icon>fas fa-cog</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Setting</v-list-item-title>
                        </v-list-item>
                        <!--Logout-->

                        <v-list-item  v-if="!this.$cookies.isKey('auth-token')" @click="$router.push({ name: 'Login' })">
                            <v-list-item-icon>
                            <v-icon>fas fa-sign-in-alt</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Login</v-list-item-title>
                        </v-list-item>

                        <v-list-item  v-if="!this.$cookies.isKey('auth-token')" @click="$router.push({ name: 'SignUp' })">
                            <v-list-item-icon>
                            <v-icon>fas fa-user-plus</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Sign Up</v-list-item-title>
                        </v-list-item>


                        <v-list-item  v-else @click="logout">
                            <v-list-item-icon>
                            <v-icon>fas fa-sign-out-alt</v-icon>
                            </v-list-item-icon>

                            <v-list-item-title>Logout</v-list-item-title>
                        </v-list-item>
                        

                    </v-list>
                </v-menu>


            </v-col>
        </v-row>
    </v-app-bar>
</template>

<script>
import axios from 'axios'
import constants from '../constants.js'

import logo from '../assets/applemango.png'

const BACKEND_URL = constants.URL

export default {

    name : 'NewHeader',
    data(){
        return {
            searchOptions : ['거리순', '평점순'],
            keyword:'',
            searchFilter: '거리순',
            navLogo: logo,
            userType: '',

            admins: [
                ['Management', 'fas fa-dice-one'],
                ['Settings', 'fas fa-dice-one'],
            ],
            cruds: [
                ['Create', 'add'],
                ['Read', 'insert_drive_file'],
                ['Update', 'update'],
                ['Delete', 'delete'],
            ],
        }
    },
    // created(){
    //     if(this.$cookies.get('auth-token')){
    //         console.log(this.$cookies.get('auth-token'))
    //         axios.get(BACKEND_URL + 'user/info?uid=' + this.$cookies.get('auth-token'))
    //         .then(response => {
    //             console.log(response.data)
    //             this.userInfo = response.data
    //             if (response.data.ukind == 3){ //관리자
    //                 this.isAdmin = true
    //             }
    //             else if (response.data.ukind == 1){ //사업자
    //                 this.isOwner = true
    //             }
    //             else {
    //                 this.isCutomer = true //일반회원
    //             }
    //         })
    //     }
    // },
    methods:{
        home: function(){
            this.$router.push({ name: 'Home' })
        },
        search: function(){
            this.$store.commit('search', this.keyword)
            this.$router.push({ name: 'SearchResult', params: { keyword: this.keyword }})
        },

        logout : function () {
            this.$cookies.remove('auth-token');
            axios.get(BACKEND_URL + 'user/logout')
                .then(response => {
                    if (response.data.status){
                        alert("로그아웃 성공");
                        alert(response.data.object);
                        //this.setCookies(this.user.id);
                        //alert(ses);
                    }
                    //this.$router.push({ path: '/'}) 같은 페이지로 새로고침 시 오류
                    
                    //Vuex통해 로그인 상태관리
                    this.$store.commit('logout')
                    location.reload();
                })
        },
    }

}
</script>

<style scoped>
#logo{
    height:80px;
}
</style>

