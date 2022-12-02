<template>
    <div>
        <Bar :chart-options="chartOptions" :chart-data="chartData" 
             :width="width" :height="height" />
    </div>

</template>

<script>
import axios from 'axios'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
ChartJS.defaults.color = "#ffffff";
export default {
    name: 'BarChartVue',
    data: () => ({
        chartData: {
            labels: [],
            datasets: [{
                data: [], label: 'Data One',
                backgroundColor: '#f87979',
            }]
        },
        chartOptions: {
            responsive: true,
            scales: {
                y: {
                    grid: {
                        color: '#ffffff'
                    }
                },

            }
        }
    }),
    components: { Bar },
    props: {
        chartId: {
            type: String,
            default: 'bar-chart'
        },
        datasetIdKey: {
            type: String,
            default: 'label'
        },
        width: {
            type: Number,
            default: 200
        },
        height: {
            type: Number,
            default: 100
        },

        filters: {
            type: Set,
            default: new Set()
        },
        group_by: {
            default: '',
            type: String
        }
    },
    async mounted() {
        await this.get_chart_data()
    },
    watch: {
        filters: function (newVal, oldVal) { 
            if (newVal != oldVal) {
                console.log('Prop changed: ', newVal, ' | was: ', oldVal)
                this.get_chart_data()
            }

        }
    },
    methods: {

        get_chart_data() {
            let params = new URLSearchParams();
            params.append('filters', Array.from(this.filters).join(','));
            params.append("group_by", this.group_by);
            axios.post(`charts/get_bar_chart`, params).then((response) => {
                if(Object.prototype.hasOwnProperty.call(response.data.default_filters, 'filter_list')){
                    console.log("HAS DEFAULT FILTER")
                    console.log(response.data.default_filters.filter_list)

                }
                if(Object.prototype.hasOwnProperty.call(response.data.default_filters, 'group_filter')){
                    console.log("HAS DEFAULT FILTER")
                    console.log(response.data.default_filters.group_filter)

                }
   
                let columns = response.data.columns.split(",")
                var mtx = JSON.parse(response.data.values)
                let [row] = mtx
                let tranpose = row.map((value, column) => mtx.map(row => row[column]))
                let new_dataset = []
                tranpose.forEach((element, idx) => {
                    new_dataset.push({
                        data: element, label: columns[idx],
                        backgroundColor: '#' + (Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0')
                    })
                })
                this.chartData = {
                    backgroundColor: '#212529',
                    labels: response.data.categories,
                    datasets: new_dataset
                }
            })
        },



    }
}



</script>
