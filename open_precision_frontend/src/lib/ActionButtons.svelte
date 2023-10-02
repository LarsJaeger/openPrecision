<script lang="ts">
    import {add} from "./Modals/Modals.svelte";
    import configUpload from "./Modals/ConfigUpload.svelte";
    import {apiAddress} from "../App.svelte";
    import ActionButton from "./ActionButton.svelte";

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

<div class="u-position-absolute u-grid u-main-center u-cross-center u-gap-16 u-z-index-15"
     style="right: 2%; transform: translateY(-50%); top: 50%;">
    <ActionButton execFunc={generateCourse} iconName="icon-plus"/>
    <ActionButton execFunc={loadConfig} iconName="icon-cog"/>
    <ActionButton execFunc={calibrate} iconName="icon-support"/>
</div>