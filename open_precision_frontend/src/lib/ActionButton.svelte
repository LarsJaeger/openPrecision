<script lang="ts">
    export let execFunc;
    export let iconName;
    let classes = "button u-font-size-32 is-big " + iconName;
</script>
<div class={classes} on:click={execFunc}/>