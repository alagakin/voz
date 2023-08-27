<template>
    <div :class="{'open': isOpen}"
         class="sidebar fixed top-0 left-0 bg-white p-4 shadow-xl h-full w-1/5 "
         style="z-index: 10000000;">

        <div class="flex flex-col h-full">
            <SearchInputs @setRoutes="setRoutes"/>

            <div class="border mt-2 h-full pb-2">
                <SearchResult :routes="routes"/>
            </div>
        </div>

        <LoaderPlug v-if="isLoading"/>
        <CloseButton :isOpen="isOpen" @toggle="toggle"/>
    </div>
</template>
<script>

import CloseButton from "@/components/bar/CloseButton.vue";
import SearchInputs from "@/components/bar/SearchInputs.vue";
import LoaderPlug from "@/components/bar/LoaderPlug.vue";
import SearchResult from "@/components/bar/SearchResult.vue";

export default {
    name: "RoutesSearcher",
    components: {SearchResult, LoaderPlug, SearchInputs, CloseButton},
    methods: {
        toggle() {
            this.isOpen = !this.isOpen
        },
        setRoutes(routes) {
            this.stations = []
            if (!routes.length) {
                alert('Not found')
            }
            //todo function for formatting
            routes.forEach(route => {
                route.stations.forEach(station => {
                    station.arrival = new Date(station.arrival)
                    station.departure = new Date(station.departure)
                })
            })

            this.routes = routes
            let route = routes[0]

            this.$emit('showRouteOnMap', route)
        }
    },
    data() {
        return {
            isOpen: true,
            isLoading: false,
            routes: [],
        }
    },
    emits: ['setRoutes', 'showRouteOnMap']
}
</script>


<style scoped>

.sidebar {
    width: 20%;
    transform: translateX(-100%);
    transition: transform 0.3s ease-out;
}

.sidebar.open {
    transform: translateX(0);
}

.content {
    flex: 1;
    background-color: #ffffff;
    padding: 20px;
}
</style>