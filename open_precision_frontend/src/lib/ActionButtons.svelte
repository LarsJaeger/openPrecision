<script lang="ts">
    import {openModal} from "./Modals.svelte";
    import configUpload from "./configUpload.svelte";

    export let socket;

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

    function loadConfig() {
        openModal(
            "Upload New Config",
            configUpload,
            "footer"
        );
    }
</script>

<div class="actionButtons">
    <button style="top:0" class="actionButton disableControls" id="ab_a" on:click={generateCourse}>
        <div class="actionButtonContent ">gen</div>
    </button>
    <button style="top:0" class="actionButton disableControls" id="ab_b" on:click={loadConfig}>
        <div class="actionButtonContent ">B</div>
    </button>
    <button style="top:0" class="actionButton disableControls" id="ab_c">
        <div class="actionButtonContent ">C</div>
    </button>
</div>