<script lang="ts">
    import {add} from "./Modals/Modals.svelte";
    import configUpload from "./Modals/ConfigUpload.svelte";
    import {apiAddress} from "../App.svelte";

    function generateCourse() {
        console.log("[INFO]: Generating course");
        fetch(apiAddress + "/v1/navigator/generate_course", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        }).then((response) => {
            console.log("[INFO]: Course generated");
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });

        console.log("[INFO]: gen_course sent");
    }

    function loadConfig() {
        add(
            "Upload New Config",
            configUpload,
            null
        );
    }

    function calibrate(){
        fetch(apiAddress + "/v1/sensor/aos/calibrate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        }).then((response) => {
            console.log("[INFO]: Calibrated");
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }
</script>

<div class="u-position-absolute u-grid u-main-center u-cross-center u-gap-16" style="right: 2%; transform: translateY(-50%); top: 50%;">
    <button class="grid-item-1 button is-big u-padding-16" id="ab_a" on:click={generateCourse}>
        <span class="icon-plus is-big" aria-hidden="true"></span>
        <span class="text u-font-size-32">Generate Course</span>
    </button>
    <button class="grid-item-1 button is-big u-padding-16" id="ab_b" on:click={loadConfig}>
        <span class="icon-cog" aria-hidden="true"></span>
        <span class="text u-font-size-32">Configure</span>
    </button>
    <button class="grid-item-1 button is-big u-padding-16" id="ab_c" on:click={calibrate}>
        <span class="text u-font-size-32">Calibrate</span>
    </button>
</div>