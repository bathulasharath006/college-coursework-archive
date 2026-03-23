<template>
    <div>
        <h4 class="err_msg">Book ID already in use, try different Book ID</h4>
        <BackButton />
        <div class="container">
            <div class="row">
                <div class="col-md-7">
                    <iframe class="iframe-container" :src="`/book_files/${book_id}.pdf`" frameborder="0" alt="PDF FILE NOT FOUND"></iframe>
                </div>
                
                <div class="col-md-5">
                    <div class="card ">
                        <div class="card-body">
                            <h3 class="card-title">Highlights</h3>
                            <p><b>Section:</b> {{ sect }}</p>
                            <p><b>Book ID:</b> {{ book_id }}</p>
                            <p><b>Book Name:<h4> {{ book_name }}</h4></b></p>
                            <p><b>Author(s):</b> {{ authors }}</p>
                            <p><b>Synopsis:</b> <br><br>{{ synopsis }}</p>
                            <p><b>Average Rating:</b> {{ avg_rating }}</p>
                            <p><b>Pages:</b> {{ pages }}</p>
                            <p><b>Added on:</b> {{ added_on }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '../axiosConfig';

export default {
    name: 'AleadyExist',
    data() {
        return {
            sect: null,
            book_id: null,
            book_name: null,
            authors: null,
            synopsis: null,
            pages: null,
            added_on: null,
            avg_rating: null,
        }
    },
    methods: {
        async loadPage() {
            await axios.get(`/adm_book_details/${this.book_id}`)
            .then(response => {
                const data = response.data;
                this.sect = data.sect;
                this.book_id = data.book_id;
                this.book_name = data.book_name;
                this.authors = data.authors;
                this.synopsis = data.synopsis;
                this.pages = data.pages;
                this.added_on = data.added_on;
                this.avg_rating = data.avg_rating;
            })
        }
    },
    mounted() {
        this.book_id = this.$route.params.book_id;
        this.loadPage();
    }
}
</script>

<style scoped>
.iframe-container {
  position: relative;
  width: 100%;
  height: 110%;
}
</style>