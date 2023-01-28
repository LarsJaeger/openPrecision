<script lang="ts">
    import Visualizer from "./lib/Visualizer.svelte";
    import io from "socket.io-client";

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

    function generateCourse() {
        console.log("[INFO]: Generating course");
        sendAction({
            function_identifier: 'plugins.Navigator.set_course_from_course_generator',
            args: [],
            kw_args: {'course_generator_identifier': 'a_heading_parallel'}
        });

        console.log("[INFO]: gen_course sent");
    }
</script>

<main>

    <div>
        <div class="visualizer">
            <Visualizer bind:visualizeMachineState={visualizeMachineState} bind:visualizeCourse={visualizeCourse}/>
        </div>
        <div class="metaButtons">
            <button class="metaButton material-symbols-outlined">info</button>
            <button class="metaButton material-symbols-outlined">settings</button>
        </div>
        <div class="actionButtons">
            <button style="top:0" class="actionButton disableControls" id="ab_a" on:click={generateCourse}>
                <div class="actionButtonContent material-symbols-outline">gen</div>
            </button>
            <button style="top:0" class="actionButton disableControls" id="ab_b">
                <div class="actionButtonContent material-symbols-outline">B</div>
            </button>
            <button style="top:0" class="actionButton disableControls" id="ab_c">
                <div class="actionButtonContent material-symbols-outline">C</div>
            </button>
        </div>
        <div class="statusBar">
            <div class="statusBarItem disableControls">1</div>
            <div class="statusBarItem disableControls">2</div>
            <div class="statusBarItem disableControls">3</div>
            <div class="statusBarItem disableControls">4</div>
        </div>
    </div>
</main>