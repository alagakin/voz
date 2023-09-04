<template>
    <div :class="{'open': isOpen}"
         class="sidebar fixed top-0 left-0 bg-white shadow-xl h-full w-1/5 max-h-screen"
         style="z-index: 10000000;">
        <div class="flex flex-col h-full">
            <div class="p-4">
                <SearchInputs @setRoutes="setRoutes" @set-date="setDate" @set-request-param="setRequestParam"
                              :request="request" @reverse="reverse"/>
            </div>
            <SearchResult ref="result" :routes="routes" @select-route="(route) => $emit('selectRoute', route)"/>

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
                this.routes = []
                return
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
            this.routes = this.sortRoutes(all_routes)
            let route = this.routes[0]
            this.$emit('selectRoute', route)
            this.$refs.result.selectRoute(0)
            this.$refs.result.dropDetail()
        },
        sortRoutes(routes) {
            let available_routes = []
            let not_available_routes = []
            let now = new Date()
            routes = routes.sort((a, b) => a.from.departure - b.from.departure)
            routes.forEach((route) => {
                if (route.from.departure > now) {
                    available_routes.push(route)
                } else {
                    route['not_available'] = true
                    not_available_routes.push(route)
                }
            })
            return available_routes.concat(not_available_routes)
        },
        search() {
            if (!this.isSearchEnabled) {
                return
            }
            let params = {
                date: this.request.date
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
        },
        reverse() {
            let temp = this.request.from
            this.request.from = this.request.to
            this.request.to = temp
            this.search()
        },
        setUrl(request) {
            const params = {};
            if (request.date) {
                params.date = request.date
            }
            if (request.from.type) {
                params.from_type = request.from.type
                params.from_id = request.from.id
            }
            if (request.to.type) {
                params.to_type = request.to.type
                params.to_id = request.to.id
            }
            const queryString = Object.keys(params)
                .map((key) => `${key}=${encodeURIComponent(params[key])}`)
                .join('&');
            const newUrl = `/?${queryString}`;
            history.pushState(null, null, newUrl);
        },
        recoverUrl() {
            const queryString = window.location.search;
            const params = new URLSearchParams(queryString);
            const date = params.get('date')
            const from_type = params.get('from_type')
            const from_id = params.get('from_id')
            const to_type = params.get('to_type')
            const to_id = params.get('to_id')

            let request = {
                date: null,
                from: {},
                to: {}
            }
            if (date) {
                request.date = date
            }
            if (from_type && from_id) {
                request.from.type = from_type
                request.from.id = from_id
            }
            if (to_type && to_id) {
                request.to.type = to_type
                request.to.id = to_id
            }
            this.request = request
        }
    },
    computed: {
        isSearchEnabled() {
            return this.request.from.id && this.request.to.id && this.request.date
        }
    },
    beforeMount() {
        this.recoverUrl()
    },
    watch: {
        request: {
            deep: true,
            handler(value) {
                this.setUrl(value)
                if (this.isSearchEnabled) {
                    this.search()
                }
            }
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
            routes: false,
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