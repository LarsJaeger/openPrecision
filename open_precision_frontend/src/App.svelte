<script lang="ts">
    import Visualizer from "./lib/Visualizer.svelte";
    import io from "socket.io-client";
    import ActionButtons from "./lib/ActionButtons.svelte";
    import StatusBar from "./lib/StatusBar.svelte";
    import MetaButtons from "./lib/MetaButtons.svelte";
    import {closeModal, Modals} from 'svelte-modals'
    import {fade} from 'svelte/transition'


    const socket = io();//("ws://" + window.location.hostname + "/");

    let visualizeMachineState;
    let visualizeCourse;

    // action responses
    socket.on("action_response", (data) => {
        console.log("[INFO]: action_response received: " + data);
    });

    // target_machine_state
    socket.on("target_machine_state", (data) => {
        console.log("[INFO]: (target_machine_state): Received message: " + data);
        // updateTargetMachineState(JSON.parse(data));
    });

    // course
    socket.on("course", (data) => {
        console.log("[INFO]: (course): Received message: " + data);
        visualizeCourse(JSON.parse(data));
    });

    // machine_state
    socket.on("machine_state", (data) => {
        console.log("[INFO]: (machine_state): Received message: " + data);
        visualizeMachineState(JSON.parse(data));
    });

    function sendAction(action) {
        const actionString = JSON.stringify(action);
        console.log("[INFO]: Sending action: " + actionString);
        socket.emit("action", actionString);
    }
</script>

<main>
    <Modals>
        <div
                slot="backdrop"
                class="backdrop"
                transition:fade
                on:click={closeModal}
        />
    </Modals>
    <Visualizer bind:visualizeMachineState={visualizeMachineState} bind:visualizeCourse={visualizeCourse}/>
    <MetaButtons/>
    <ActionButtons socket={socket}/>
    <StatusBar/>

</main>