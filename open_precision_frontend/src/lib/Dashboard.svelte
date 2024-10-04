<script>
    import GeostoreAdd from "./Modals/GeostoreAdd.svelte";
    import GeoStore from "./GeoStore.svelte"
</script>
<div class="u-z-index-0 u-width-full-line">
    <div class="tabs">
        <ul class="tabs-list">
            <li class="tabs-item">
                <button class="tabs-button is-selected">
                    <img alt="Open Precision" class="u-width-full-line is-center" src="../assets/logo.svg">
                </button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Sessions</span></button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Activity</span></button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Settings</span></button>
            </li>
        </ul>
        <div class="container">
            <GeoStore />
        </div>
    </div>
</div>
