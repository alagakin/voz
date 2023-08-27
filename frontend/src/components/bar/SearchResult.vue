<template>
    <div class="p-2"
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