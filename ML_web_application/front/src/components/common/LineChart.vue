<template>
    <div>
        <Line :chart-options="chartOptions" :chart-data="chartData" :width="width" :height="height" />
    </div>

</template>

<script>
import axios from 'axios'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, CategoryScale, LinearScale, LineElement } from 'chart.js'
ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
)

export default {
    name: 'LineChartVue',
    data: () => ({
        chartData: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [
                {
                    label: 'Data One',
                    backgroundColor: '#f87979',
                    borderColor: 'rgb(75, 192, 192)',
                    data: [40, 39, 10, 40, 39, 80, 40]
                }
            ]
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
    components: { Line },
    props: {
        chartId: {
            type: String,
            default: 'line-chart'
        },
        width: {
            type: Number,
            default: 400
        },
        height: {
            type: Number,
            default: 400
        },
        cssClasses: {
            default: '',
            type: String
        },
        filters: {
            type: Set,
            default: new Set()
        },
        group_by: {
            default: '',
            type: String
        },
        methods: {

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
                backgroundColor: '#' + (Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'),
                borderColor:  '#' + (Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0')
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
