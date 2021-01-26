import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);

export const store = new Vuex.Store({
         plugins: [
            createPersistedState({
                storage: window.sessionStorage
            })
         ],
         state: {
           userInfo: {
             isLoggedin: false,
             userId: ''
            //  isAdmin: false,
            //  isUser: false,
            //  isOwner: false,
           },
           userType: '', //유저타입 변수
           keyword: '', //메인화면 검색어
           currentLocation: false, //longitude, latitude //현재 위치 정보
         },
         mutations: {
             //CHECK USERTYPE
             login(state, userInfo){
                 const userType = userInfo.ukind;
                 state.userInfo.userId = userInfo.uid;
                 if (userType === 0){
                    //  state.userInfo.isUser = true
                     state.userType = 'User'  
                 }
                 else if (userType === 1){
                    //  state.userInfo.isOwner = true
                     state.userType = 'Owner';
                 }
                 else if (userType === 3){
                    //  state.userInfo.isConsultant = true;
                     state.userType = 'Consultant';
                 }
                 else if(userType === 4){
                    //  state.userInfo.isAdmin = true;
                     state.userType = 'Admin';
                 }
             },
             //로그아웃시 유저 타입 초기화 
             logout(state){
                 state.userType = ''
             },

             search(state, keyword){
                 state.keyword = keyword
             },
            //현재 위치 정보 저장
             getLocation(state, coordinates){
                 console.log(coordinates)
                 state.currentLocation = {
                     longitude: coordinates[1],
                     latitude: coordinates[0]
                 }
             }
         },
         getters: {
             getUserType: state => {
                 return state.userType;
             },
             getKeyword: state => {
                 return state.keyword;
             },
             //현재 위치 정보 getter
             getLocation: state => {
                 return state.currentLocation
             },
             getUserId: state => {
                 return state.userInfo.userId
             }
         }
       });