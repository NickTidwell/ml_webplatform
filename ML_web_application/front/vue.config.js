const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: 'vue-app',
    client: {
      logging: 'verbose',
    },

  }
})
