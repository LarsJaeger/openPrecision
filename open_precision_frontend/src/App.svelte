<script context="module">
    let waiting_for_ar = {};
    export function sendAction(socket, action, resultProcessingF) {
        // set id of action to random int if not set yet
        if (!action.id || action.id === null) {
            action.id = Math.floor(Math.random() * 1000000);
        }
        const actionString = JSON.stringify(action);
        console.log("[INFO]: Sending action: " + actionString);
        waiting_for_ar[action.id] = resultProcessingF;
        socket.emit("action", actionString);
    }
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
