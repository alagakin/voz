<template>
    <div :class="{'open': isOpen}"
         class="sidebar fixed top-0 left-0 bg-white p-4 shadow-xl h-full w-1/5 "
         style="z-index: 10000000;">

        <SearchInputs @setRoutes="(routes) => $emit('setRoutes', routes)" />
        <CloseButton :isOpen="isOpen" @toggle="toggle"/>
        <LoaderPlug v-if="isLoading"/>
    </div>
</template>
<script>

import CloseButton from "@/components/bar/CloseButton.vue";
import SearchInputs from "@/components/bar/SearchInputs.vue";
import LoaderPlug from "@/components/bar/LoaderPlug.vue";

export default {
    name: "RoutesSearcher",
    components: {LoaderPlug, SearchInputs, CloseButton},
    methods: {
        toggle(){
            this.isOpen = !this.isOpen
        }
    },
    data() {
        return {
            isOpen: true,
            isLoading: false
        }
    },
    emits: ['setRoutes']
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