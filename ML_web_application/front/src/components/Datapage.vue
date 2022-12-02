<template>
    <FileUpload v-if="mounted_data == false" @uploaded_data=get_cache />
    <Datatable v-if="mounted_data == true && hide_chart == false" />
    <button @click="clear_data" class="btn btn-outline-danger">Clear Chart</button>
    <button @click="hide_chart = true" v-if="hide_chart == false" class="btn btn-outline-danger">Hide
        Chart</button>
    <button @click="hide_chart = false" v-if="hide_chart == true" class="btn btn-outline-danger">Show
        Chart</button>
    <div style="max-width: 800px; margin: 16px 0">
        <BarChart v-if="mounted_data == true" :filters="this.submitted_filters" :group_by="this.group_by" />
    </div>
    <div style="max-width: 800px; margin: 16px 0">
        <LineChart v-if="mounted_data == true" :filters="this.submitted_filters" :group_by="this.group_by" />
    </div>
    <div style="border: solid; border-color: #00bfff; border-radius: 8px; margin: 10px; ">
        <h5 style="float: left; margin: 8px;">Selected Filters:</h5>
        <div
            style="padding-right: 10px; margin: auto; display: flex; flex-wrap: wrap; ">
            <div v-for="(type, name) in filters" :key="name" style="margin: 10px; ">
                <button @click=remove_from_filters(name) v-if="selected_filters.has(name)" type="submit"
                    class="btn btn-info" style="background-color:#00bfff; min-width: 120px; width: fit-content"
                    name="filter_btn" value={{label}}>
                    {{ name }} <span class="badge badge-light"></span>
                </button>
                <button @click=add_to_filters(name) v-if="!selected_filters.has(name)" type="submit"
                    class="btn btn-info" style="background-color:white; min-width: 120px; width: fit-content"
                    name="filter_btn" value={{label}}>
                    {{ name }} <span class="badge badge-light"></span>
                </button>
            </div>
            
        </div>
        <h5 style="float: left; margin: 8px;">Group By:</h5>
        <div
            style="padding-right: 10px; margin: auto; display: flex; flex-wrap: wrap; ">
            <div v-for="(type, name) in filters" :key="name" style="margin: 10px; ">
                <button @click="group_by = name" v-if="group_by == name" type="submit"
                    class="btn btn-info" style="background-color:#00bfff; min-width: 120px; width: fit-content"
                    name="filter_btn" value={{label}}>
                    {{ name }} <span class="badge badge-light"></span>
                </button>
                <button @click="group_by = name" v-if="group_by !== name" type="submit"
                    class="btn btn-info" style="background-color:white; min-width: 120px; width: fit-content"
                    name="filter_btn" value={{label}}>
                    {{ name }} <span class="badge badge-light"></span>
                </button>
            </div>
            
        </div>
        <button @click="submit_filters" class="btn btn-primary" style="float: left; margin: 8px;" >Submit Fitlers</button>

    </div>

</template>

<script>
import axios from 'axios'
import BarChart from './common/BarChart.vue';
import Datatable from './common/Datatable.vue';
import FileUpload from './common/FileUpload.vue'
import LineChart from "./common/LineChart.vue"
export default {
    name: "DatapageVue",
    data: () => ({

        mounted_data: false,
        hide_chart: false,
        chart_title: "Default Title: received data",
        filters: {},
        selected_filters: new Set(),
        submitted_filters: new Set(),
        group_by: "",
    }),
    async mounted() {
        await this.get_cache();
    },
    props: {},
    methods: {

        submit_filters(){
            this.submitted_filters = structuredClone(this.selected_filters)
        },

        remove_from_filters(filter) {
            this.selected_filters.delete(filter)
        },
        add_to_filters(filter) {
            this.selected_filters.add(filter)
        },
        get_filters() {
            axios.get("charts/get_data_filters").then((response) => {
                console.log(response)
                if (response.status === 200) {
                    console.log(response.data)
                    this.filters = response.data.filters
                }
            });
        },
        get_cache() {
            axios.get("charts/check_cache").then((response) => {
                this.status = response.data.status;
                if (response.data.status == "sucess") {
                    this.mounted_data = true
                    this.get_filters()
                }
            });
        },
        clear_data() {
            axios.get('charts/clear_chart').then((response) => {
                this.status = response.data.status
                if (response.data.status == "sucess") {
                    this.status = "no mounted file"
                    this.mounted_data = false
                }

            })
        },
    },

    components: { FileUpload, Datatable, BarChart, LineChart }
}



</script>
