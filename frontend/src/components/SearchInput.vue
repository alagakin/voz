<template>
  <div class="fixed top-0 left-0 bg-gray-100 p-4 shadow-md z-100" style="z-index: 10000000;">
    <div class="flex gap-4">
      <input v-model="station_from" placeholder="Station from" class="p-2 border rounded"/>
      <input v-model="station_to" placeholder="Station to" class="p-2 border rounded"/>
      <button @click="search" class="px-4 py-2 bg-blue-500 text-white rounded">
        Search
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchInput",
  methods: {
    search() {
      const params = {
        station_from: this.station_from,
        station_to: this.station_to
      };

      axios.get("http://localhost:8000/api/v1/find-routes/", { params })
        .then(response => {
          this.$emit('setRoutes', response.data)
        })
        .catch(error => {
          console.error("Error fetching data:", error);
        });

    }
  },
  data() {
    return {
      station_from: "",
      station_to: "",
    };
  },


};
</script>