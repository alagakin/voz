<template>
    <div class="bg-white absolute bottom-0 right-0 overflow-hidden text-sm p-1" style="z-index: 1000000">
        <span class="user-select-none">
            Created by Alexandr Agakin
        </span>
        <span class="mr-1">
            <a href="https://www.linkedin.com/in/alexandar-agakin/" target="_blank">
                <font-awesome-icon :icon="['fab', 'linkedin']" size="lg"/>
            </a>
        </span>
        <span class="mr-1">
            <a href="https://t.me/alagakin" target="_blank">
                <font-awesome-icon :icon="['fab', 'telegram']" size="lg"/>
            </a>
        </span>
        <span class="mr-1">
            <a href="https://github.com/alagakin" target="_blank">
                <font-awesome-icon :icon="['fab', 'github']" size="lg"/>
            </a>
        </span>
    </div>
</template>
<script>
export default {
    name: "AuthorBlock"
}
</script>
