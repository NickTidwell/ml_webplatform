<template>
  <NavbarVue title="Nicks Django Site" />
  <DatapageVue/>

</template>

<script>
import NavbarVue from './components/common/Navbar.vue'
import DatapageVue from './components/Datapage.vue';

import axios from 'axios'
import Cookies from 'js-cookie'
const csrftoken = Cookies.get('csrftoken', {withCredentials: true});
axios.defaults.headers.common = {
    'X-CSRFToken': csrftoken,
    'Access-Control-Allow-Credentials': true
};

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.baseURL = "http://localhost/api"

export default {
  name: 'App',
  components: {
    NavbarVue,
    DatapageVue
  },

}


</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
