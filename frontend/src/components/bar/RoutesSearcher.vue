<template>
    <div :class="{'open': isOpen}"
         class="sidebar fixed top-0 left-0 bg-white shadow-xl h-full w-1/5 max-h-screen"
         style="z-index: 10000000;">
        <div class="flex flex-col h-full">

            <div class="p-4">
                <SearchInputs @setRoutes="setRoutes" @set-date="setDate" @set-request-param="setRequestParam"
                              :request="request"/>
                <button @click="search" class="mt-6 px-4 py-2 bg-blue-500 text-white rounded"
                        :class="{'bg-gray-400': !isSearchEnabled}">
                    Search
                </button>
            </div>

            <div class="mt-2 pb-2 max-h-fit overflow-y-auto">
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
import axios from "axios";

export default {
    name: "RoutesSearcher",
    components: {SearchResult, LoaderPlug, SearchInputs, CloseButton},
    methods: {
        setDate(date) {
            this.request.date = date
        },
        setRequestParam(param) {
            if (param.direction === 'from') {
                this.request.from = {
                    id: param.id,
                    type: param.type
                }
            } else {
                this.request.to = {
                    id: param.id,
                    type: param.type
                }
            }
        },
        toggle() {
            this.isOpen = !this.isOpen
        },
        setRoutes(routes) {
            if (!routes.length) {
                alert('Not found')
            }
            //date-time-formatting
            routes.forEach(route => {
                route.stations.forEach(station => {
                    station.arrival = new Date(station.arrival)
                    station.departure = new Date(station.departure)
                })
                route["stations_from"].forEach(station => {
                    station.arrival = new Date(station.arrival)
                    station.departure = new Date(station.departure)
                })
                route["stations_to"].forEach(station => {
                    station.arrival = new Date(station.arrival)
                    station.departure = new Date(station.departure)
                })
            })
            let all_routes = []
            routes.forEach(route => {
                route["stations_from"].forEach(station_from => {
                    route["stations_to"].forEach(station_to => {
                        let new_route = {...route}
                        delete new_route["stations_from"]
                        delete new_route["stations_to"]
                        new_route["from"] = station_from
                        new_route["to"] = station_to
                        all_routes.push(new_route)
                    })
                })
            })
            this.routes = all_routes
            let route = this.routes[0]

            this.$emit('selectRoute', route)
        },
        search() {
            if (!this.isSearchEnabled) {
                return
            }
            let params = {
                data: this.date
            }
            if (this.request.from.type === 'station') {
                params['station_from_id'] = this.request.from.id
            } else if (this.request.from.type === 'city') {
                params['city_from_id'] = this.request.from.id
            }
            if (this.request.to.type === 'station') {
                params['station_to_id'] = this.request.to.id
            } else if (this.request.to.type === 'city') {
                params['city_to_id'] = this.request.to.id
            }
            this.isLoading = true
            axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/routes/", {params})
                .then(response => {
                    this.setRoutes(response.data)
                    this.isLoading = false
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    this.isLoading = false
                });
        }
    },
    computed: {
        isSearchEnabled() {
            return true
        }
    },
    data() {
        return {
            request: {
                date: null,
                from: {},
                to: {}
            },
            isOpen: true,
            isLoading: false,
            routes: [],
        }
    },
    emits: ['setRoutes', 'selectRoute']
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
</style>