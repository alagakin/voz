<template>
    <div class="h-full max-h-fit overflow-scroll overflow-x-hidden overflow-y-auto"
         v-show="routes.length">
        <RouteInfoItem ref="item" v-for="route in routes" :route="route" v-bind:key="route" @unselect-all="unselectAll"
                       @select-route="(route) => $emit('selectRoute', route)"/>
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
    methods: {
        unselectAll() {
            this.$refs.item.forEach(item => {
                item.unselect()
            })
        }
    },
    data() {
        return {}
    },
    emits: ["selectRoute"]
}

</script>