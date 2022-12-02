<template>
    <div>
        <div class="p-3 mb-2 bg-body text-dark">{{ chart_title }}</div>
        <table class="table table-striped table-dark table-hover">
            <thead>
                <tr>
                    <th scope="col" v-for="(header, index) in table_data.columns" :key="index">{{ header }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(column, col_index) in table_data.data" :key="col_index">
                    <td v-for="(val, val_index) in column" :key="val_index">
                        {{ val }}
                    </td>
                </tr>

            </tbody>
        </table>
        <nav aria-label="Page navigation example">
            <ul class="pagination">
                <li v-if="page_id > 0" class="page-item">
                    <a class="page-link" @click="page_id = 0; get_data()">{{ "<<" }}</a>
                </li>
                <li v-if="page_id > 0" class="page-item"><a class="page-link"
                        @click="page_id = page_id - 1; get_data()">Previous</a></li>
                <li v-for="(record, rec_index) in Math.ceil(total_records / record_per_page) " :key="rec_index">

                    <a v-if="(record > page_id - 4 && (record < page_id + 4)) || (page_id - 4 <= 0 && record < 8)"
                        class="page-link" @click="page_id = rec_index; get_data()">{{ rec_index + 1 }}</a>
                </li>

                <li v-if="page_id < Math.ceil(total_records / record_per_page) - 1" class="page-item"><a
                        class="page-link" @click="page_id = page_id + 1; get_data()">Next</a>
                </li>
                <li v-if="page_id < Math.ceil(total_records / record_per_page) - 1" class="page-item"><a
                        class="page-link"
                        @click="page_id = Math.ceil(total_records / record_per_page) - 1; get_data()">{{ ">>" }}</a>
                </li>
            </ul>
        </nav>
        <p>total records: {{ total_records }}</p>

        <div class="form-floating">
            <input v-model="chart_title" type="text" class="form-control me-2" id="floatingInputGrid"
                placeholder="Title">
            <label for="floatingInputGrid">Chart Title</label>
        </div>

    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'DatatableVue',
    data: () => ({
        table_data: "",
        total_records: 0,
        page_id: 0,
        record_per_page: 10,
    }),
    props: {
    },
   mounted() {           
        this.get_data()
   },
    methods: {
        get_data() {
            axios.get(`charts/get_table_data?page_id=${this.page_id}&per_page=${this.record_per_page}`).then((response) => {
                this.total_records = response.data.total_records
                this.table_data = JSON.parse(response.data.table_content)
            })
        },
    }
}



</script>
