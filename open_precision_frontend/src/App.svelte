<script context="module" lang="ts">
    export let apiAddress: string = window.location.href.slice(0, window.location.href.length - window.location.pathname.length) + "/api";
    console.log("[INFO]: using API address: " + apiAddress);
</script>
<script>
    import Visualizer from "./lib/Visualizer.svelte";
    import io from "socket.io-client";
    import ActionButtons from "./lib/ActionButtons.svelte";
    import StatusBar from "./lib/StatusBar.svelte";
    import MetaButtons from "./lib/MetaButtons.svelte";
    import Modals, {add} from "./lib/Modals/Modals.svelte";
    import {socket} from "./stores";
    import ActionResponseError from "./lib/Modals/ActionResponseError.svelte";


    let visualizeMachineState;
    let visualizeCourse;

    // target_machine_state
    $socket.on("target_machine_state", (data) => {
        console.log("[INFO]: (target_machine_state): Received message: " + data);
        // updateTargetMachineState(JSON.parse(data));
    });

    // course
    $socket.on("course", (data) => {
        console.log("[INFO]: (course): Received message: " + data);
        visualizeCourse(JSON.parse(data));
    });

    // machine_state
    $socket.on("vehicle_state", (data) => {
        console.log("[INFO]: (vehicle_state): Received message: " + data);
        visualizeMachineState(JSON.parse(data));
    });
</script>

<main>
    <Modals />
    <Visualizer bind:visualizeMachineState={visualizeMachineState} bind:visualizeCourse={visualizeCourse}/>
    <!--<MetaButtons/> -->
    <ActionButtons />
    <!--<StatusBar/> -->
</main>
