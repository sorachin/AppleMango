<template>
    <div class="review-table mx-3">
        <!--리뷰 헤더 시작-->
        <div class="d-flex justify-space-between mb-2">
            <h1 style="text-align: left;">식당 리뷰들</h1>

            <!--params 안에 동적라우팅 변수 추후에 변경 요망-->
            <!--리뷰 작성페이지 링크 시작-->
            <div class="my-auto">
                <router-link v-bind:to="{ name:'ReviewForm', params: {rid:restaurantId} }" style="text-decoration:none">
                    <v-btn color="#ffcb3b" class="font-weight-bold">리뷰 작성하러 가기!</v-btn>
                </router-link>
            </div>
            <!--리뷰 작성페이지 링크 종료-->
        </div>
        <!--리뷰 헤더 종료-->
        <!--리뷰 grid 시작-->
        <v-card
        rounded="xl"
        class="rounded mx-0 mx-auto mb-2"
        style="background-color:#FFF8E1"
        v-for="review in reviews" v-bind:key="review.reviewId"
        :id="review.title">
          <v-row class="ma-1">
              <!-- <v-col cols="4">
                  <v-img src="https://images.pexels.com/photos/704569/pexels-photo-704569.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
                  contain aspect-ratio="1.5"></v-img>
              </v-col> -->
              <v-col cols="12" class="text-left d-flex flex-column">
                  <div class="d-flex align-center justify-space-between">
                      <v-card-title class="h-5 px-0">{{ review.title }}</v-card-title>
                      <!--리뷰 삭제 버튼-->
                      <v-icon v-if="getUserInfo === review.userId" v-on:click="deleteReview(review.reviewId)" color="red">fa-trash</v-icon>
                  </div>
                  <div class="d-flex mb-3">
                      <div class="mr-2 d-flex align-center">
                          <div>평점: </div>
                          <v-rating
                          class="pb-1"
                          readonly v-model="review.star" color="orange" 
                          small dense background-color="orange">
                          </v-rating>
                      </div>
                      <div class="mr-2 align-self-center">작성자: {{ review.userId }}</div>
                      <!-- <div>작성일: {{ review.createdDate[0] + review.createdDate[1] }}</div> -->
                  </div>
                  <p class="body-1">
                      {{ review.description }}  
                  </p>
                  <div fixed class="d-flex justify-space-between mt-auto">
                      <p></p>
                      <div>
                        <!--리뷰수정버튼(리뷰 작성자에게만 표시)-->
                        <v-btn v-if="userInfo.uid == review.userId" 
                        small 
                        class="mr-3 font-weight-bold"
                        :to="{ name: 'ReviewEditForm', params:{rid:review.reviewId}}"
                        @click="editReview(review)">
                            리뷰 수정 하기
                        </v-btn>
                        <v-btn 
                        @click="commentToShow = review.reviewId; commentSwitch = !commentSwitch"
                        small color="#ffcb3b">
                            <span v-if="toggleComment(review.reviewId)" class="font-weight-bold">댓글 닫기</span>
                            <span v-else class="font-weight-bold">댓글 보기</span>
                        </v-btn>
                      </div>
                  </div>
              </v-col>
              <!-- <v-col v-if="commentToShow === review.reviewId" style="background-color:white"> -->
            <v-expand-transition>
              <v-col class="rounded-xl mb-1" v-if="toggleComment(review.reviewId)" style="background-color:white">
                <!-- <comment-form v-on:create="registerComment" v-bind:reid="review.reviewId"></comment-form> -->
                <comment-form v-on:create="createComment" v-bind:reid="review.reviewId" v-bind:commentCreated="commentCreated"></comment-form>
                <p v-if="filteredComments.length === 0">댓글이 아직 없습니다 ㅠㅠ</p>
                <h4 v-else class="text-left mb-2">댓글 목록</h4>
                <v-card v-for="(comment,index) in filteredComments" :key="index" 
                class="text-left mb-1">
                    <v-card-subtitle 
                    class="font-weight-bold d-flex justify-content-between">
                        작성자: {{ comment.userId }}
                        <div class="d-inline">
                            <!--댓글 수정-->
                            <v-icon small
                            v-if="commentToEdit == false"
                            @click="commentToEdit = comment.id"
                            >fa-edit
                            </v-icon> 

                            <!--댓글 삭제 버튼-->
                            <v-icon
                            class="ml-2"
                            v-if="getUserInfo === comment.userId" 
                            small color="red"
                            id="delete-comment" v-on:click="deleteComment(comment.id)">
                            fa-trash
                            </v-icon>
                        </div>
                    </v-card-subtitle>
                    <v-card-text v-if="commentToEdit == false">{{ comment.content }}</v-card-text>
                    <v-card-text v-if="commentToEdit == comment.id">
                        <v-textarea solo flat no-resize v-bind:placeholder="comment.content" v-model="comment.content"></v-textarea>
                        <v-btn @click="editComment(comment)">수정</v-btn>
                        <v-btn @click="commentToEdit = false">취소</v-btn>
                    </v-card-text>
                </v-card>
              </v-col>
            </v-expand-transition>
          </v-row>
        </v-card>
        <!--리뷰 grid 종료-->
    </div>
    
</template>

<script>
import axios from 'axios'
import CommentForm from '../review/CommentForm.vue'
import constants from '../../constants.js'
//import ReviewList from '../review/ReviewList.vue'

//local
// const BACKEND_URL = "http://localhost:8080/"
const BACKEND_URL = constants.URL

export default {
    name: "Review",
    components: {
      CommentForm,
      //ReviewList
    },
    props:{
        restaurantId:Number
    },
    data(){
        return {
            reviews: [],
            comments: [],
            filteredComments: [],
            commentToShow:'',
            commentSwitch: false,
            isLoggedIn: '',
            userInfo:'',
            commentToEdit: false,
            commentCreated: false,
        }
    },
    methods:{
        createComment: function(commentData){
            axios.post(`${BACKEND_URL}comment/new`,commentData)
            .then(response => {
                // console.log(response.data)
                this.comments.unshift(response.data) //새로운댓글 배열에 추가후 배열의 처음으로 이동.
                this.commentCreated = !this.commentCreated
            })
        },
        toggleComment: function(reviewId){
            if (this.commentSwitch === true && this.commentToShow === reviewId){
                return true
            }
        },
        filterComment: function(){
            this.comment = this.comment.filter(function(v){
                // console.log(this.commentToShow)
                return v === this.commentToShow
            })
        },
        editComment: function(comment){
            this.commentToEdit = false
            axios.put(BACKEND_URL + 'comment/modify', comment)
            .then(response => {
                this.comments = response.data
            })
            
        },
        deleteComment: function(commentId){
            if (confirm('댓글을 삭제하시겠습니까?')) {
                console.log(commentId)
                axios.delete(BACKEND_URL + 'comment/delete', { params: { 'commentId': commentId }})
                .then(response => {
                    // console.log(response)
                    this.comments = response.data
                })
            }
        },
        deleteReview: function(reviewId){
            if (confirm('정말 삭제하시겠습니까?')) {
                axios.delete(BACKEND_URL + 'review/delete', {params: { 'reviewId': reviewId }})
                .then(response => {
                    alert('성공적으로 삭제되었습니다')
                    // console.log(response)
                    this.reviews = response.data
                })
            }

            
        },
        refresh: function(data){
            this.comments.unshift(data)
        },
        //Method to open comment editing window
    },
    mounted(){
        //Get all reviews and filter by restaurant id
        axios.get(`${BACKEND_URL}review`)
        .then(response => {
            this.reviews = response.data;
            this.reviews = this.reviews.filter(review => {
                return review.restaurantId === this.restaurantId
            })
            
        })

        //Get All comments
        axios.get(`${BACKEND_URL}comment/all`)
        .then(response => {
            this.comments = response.data;
            // console.log(response)
        })
        //login check
        if (this.$cookies.isKey('auth-token')) {
            this.isLoggedIn = true
            axios.get(`${BACKEND_URL}user/info`, {params: {'uid':`${this.$cookies.get('auth-token')}`}})
            .then(reponse => {
                this.userInfo = reponse.data
            })
        }
    },
    watch: {
        commentToShow: function(){
            this.filteredComments = this.comments.filter(comment => {
                return comment.review.reviewId === this.commentToShow
            })
        },
        comments: function(){
            this.filteredComments = this.comments.filter(comment => {
                return comment.review.reviewId === this.commentToShow
            })
        },
    },
    computed: {
        getUserInfo: function(){
            return this.$cookies.get('auth-token')
        }
    }

}
</script>

<style>
.review-table{
    margin: 0px 100px;
}
</style>