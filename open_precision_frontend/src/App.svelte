<script context="module">
    let waiting_for_ar = {};
    export function sendAction(socket, action, resultProcessingF) {
        const actionString = JSON.stringify(action);
        console.log("[INFO]: Sending action: " + actionString);
        socket.emit("action", actionString);
        waiting_for_ar[action] = resultProcessingF;
    }
</script>
<script lang="ts">
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


    // action responses
    $socket.on("action_response", (data) => {
        let parsed_data = JSON.parse(data);
        if (parsed_data.success == false) {
            console.log("[INFO]: action_response received: error");
            add("Action failed", ActionResponseError, {response: parsed_data.response});
            console.log("[ERROR]: action_response: " + parsed_data.response);
        }
        else {
            console.log("[INFO]: action_response received: success");
            // check if answer is in waiting_for_ar and execute its fn
            if (waiting_for_ar[parsed_data.action] && typeof waiting_for_ar[parsed_data.action] !== null) {
                waiting_for_ar[parsed_data.action](parsed_data.response);
                delete waiting_for_ar[parsed_data.action];
            }
        }
    });

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
    $socket.on("machine_state", (data) => {
        console.log("[INFO]: (machine_state): Received message: " + data);
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
