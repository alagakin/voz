<template>
    <div class="mt-2 pb-2 max-h-fit overflow-y-auto">
        <div class="h-full max-h-fit overflow-scroll overflow-x-hidden overflow-y-auto"
             v-show="routes.length && detailRoute === null">
            <RouteInfoItem ref="item" v-for="(route, index) in routes" :route="route" v-bind:key="index"
                           @unselect-all="unselectAll"
                           @select-route="(rt) => $emit('selectRoute', rt)"
                           @show-more="showMore"
            />
        </div>
        <DetailRoute :route="detailRoute" @back="back" v-if="detailRoute != null"/>
        <NotFound v-if="routes.length === 0" />
    </div>
</template>
<script>


import RouteInfoItem from "@/components/RouteInfoItem.vue";
import {nextTick} from "vue";
import DetailRoute from "@/components/bar/DetailRoute.vue";
import NotFound from "@/components/bar/NotFound.vue";

export default {
    components: {NotFound, DetailRoute, RouteInfoItem},
    props: {
        routes: [Array, Boolean]
    },
    methods: {
        back() {
            this.detailRoute = null
        },
        showMore(route) {
            this.detailRoute = route
        },
        unselectAll() {
            this.$refs.item.forEach(item => {
                item.unselect()
            })
        },
        selectRoute(index) {
            nextTick(() => {
                if (this.$refs.item) {
                    this.$refs.item[index].select()
                }
            })
        }
    },
    data() {
        return {
            detailRoute: null
        }
    },
    emits: ["selectRoute"]
}

</script>