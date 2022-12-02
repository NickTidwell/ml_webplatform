<template>
    <div>
        <h3>Django File Upload</h3>
        <input type="file" ref="file" @change="onFileChange" />
        <button @click.once="upload_data" class="btn btn-info" style="background-color:#00bfff"> Submit </button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'FileUpload',
    data: () => ({
        selectedFile: "",
    }),
    props: {
    },
    methods: {
        upload_data() {
            const formData = new FormData();
            formData.append("data_file", this.selectedFile);
            axios.post('charts/upload', formData, { headers: { "Content-Type": "multipart/form-data" } }).then((response) => {

                if (response.data.status == "sucess") {
                    this.$emit('uploaded_data')
                }
            })
        },
        onFileChange(e) {
            const selectedFile = e.target.files[0]; // accessing file
            this.selectedFile = selectedFile;
        },

    }
}



</script>
