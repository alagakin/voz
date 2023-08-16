<template>
    <div class="absolute top-0 right-0 bg-gray-100 p-4 text-lg w-1/4 rounded-b-lg" style="z-index: 100000;"
         v-show="routes.length">
        <RouteInfoItem v-for="route in routes" :route="route" v-bind:key="route"/>
    </div>
</template>
<script>


import RouteInfoItem from "@/components/RouteInfoItem.vue";

export default {
    components: {RouteInfoItem},
    props: {
        routes: {
            type: Array,
        }
    },
    data() {
        return {}
    }
}

</script>