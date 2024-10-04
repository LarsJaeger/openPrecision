<script>
    import {closeCurrent} from "./Modals.svelte";
    import {apiAddress} from "../../App.svelte";

    export let locationNames = [];

    function generateCourse(){
        alert("not yet implemented");
    }

    function calibrateAccelerometer(){
        fetch(apiAddress + "/api/v1/sensor/aos/calibrate?" + new URLSearchParams(), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
              "waypoint_name_1":locationNames[0],
              "waypoint_name_2":locationNames[1],
            })
        }).then(async (response) => {
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }
</script>
<div class="modal-content">
    <ul class="clickable-list">
        <li class="clickable-list-item">
            <a href="/" class="clickable-list-button">
                <h5 class="clickable-list-title u-trim-1" on:keypress={generateCourse}>
                    <span class="">AB Course</span>
                </h5>
            </a>
        </li>
        <li class="clickable-list-item">
            <a href="/" class="clickable-list-button">
                <h5 class="clickable-list-title u-trim-1" on:keypress={calibrateAccelerometer}>
                    <span class="">calibrate accelerometer</span>
                </h5>
            </a>
        </li>
    </ul>
</div>
<div class="modal-footer">
    <div class="u-flex u-main-end u-gap-16">
        <button class="button is-secondary" on:click={closeCurrent} on:keypress><span class="text">Cancel</span>
        </button>
    </div>
</div>
