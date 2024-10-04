<script>
    export let execFunc;
    export let iconName;
    let classes = "button u-font-size-32 is-big " + iconName;
</script>
<button class={classes} on:click={execFunc}/>
