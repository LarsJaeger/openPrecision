<script context="module">
    export const backendAddress = "http://localhost:8000"// window.location.href.slice(0, window.location.href.length - window.location.pathname.length); //"http://192.168.9.129:8000", //window.location.href.slice(0, window.location.href.length - window.location.pathname.length);
    export const apiAddress = backendAddress + "/api";
    console.log("[INFO]: using API address: " + apiAddress);
</script>
<script>
    import Visualizer from "./lib/Visualizer.svelte";
    import io from "socket.io-client";
    import ActionButtons from "./lib/ActionButtons.svelte";
    import Dashboard from "./lib/Dashboard.svelte";
    import Modals, {add} from "./lib/Modals/Modals.svelte";
    import {socket} from "./stores.js";
    import SwitchButton from "./lib/SwitchButton.svelte";

    let visualizeCourse; // set by Visualizer
    let visualizeMachineState; // set by Visualizer
    let visualizeTargetSteeringAngle; // set by Visualizer
    let visualizeRawLocation; // set by Visualizer
    let visualizeCurrentPathId; // set by visualizer


    let sid;
    let event_id_to_function_map = new Map();
    let showVisualizer = true;

    function course_update(data) {
        const parsedData = JSON.parse(data);
        console.log("[INFO]: (course): Received message: ");
        console.log(parsedData);
        if (parsedData != null) {
            visualizeCourse(parsedData);
        }
    }

    function sub_to_course() {
        // subscribe to course
        fetch(apiAddress + "/v1/navigator/course?" + new URLSearchParams({
            subscription_socket_id: sid,
            subscription_period_length: "0",
        }), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            return response.json();
        }).then((data) => {
            console.log("[INFO]: subscribed to hash " + data)
            event_id_to_function_map.set(data, course_update);
            $socket.on(data, course_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    function current_path_update(data) {
        const parsedData = JSON.parse(data);
        console.log("[INFO]: (current_path_id): Received message: ");
        console.log(parsedData);
        if (parsedData != null) {
            visualizeCurrentPathId(parsedData);
        }
    }

    function sub_to_current_path() {
        // subscribe to course
        fetch(apiAddress + "/v1/navigator/current_path_id?" + new URLSearchParams({
            subscription_socket_id: sid,
            subscription_period_length: "0",
        }), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            return response.json();
        }).then((data) => {
            console.log("[INFO]: subscribed to hash " + data)
            event_id_to_function_map.set(data, current_path_update);
            $socket.on(data, current_path_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }


    // vehicle data
    function vehicle_data_update(data) {
        const parsedData = JSON.parse(data);
        console.log("[INFO]: (vehicle_state): Received message: ");
        console.log(parsedData);
        visualizeMachineState(parsedData);
    }

    function sub_to_vehicle_data() {
        // subscribe to course
        fetch(apiAddress + "/v1/vehicle_state/?" + new URLSearchParams({
            subscription_socket_id: sid,
            subscription_period_length: "0",
            ignore_uuid: "true"
        }), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            return response.json();
        }).then((data) => {
            console.log("[INFO]: subscribed to hash " + data)
            event_id_to_function_map.set(data, vehicle_data_update);
            $socket.on(data, vehicle_data_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    // target_steering_angle data
    function target_steering_angle_update(data) {
        const parsedData = JSON.parse(data);
        console.log("[INFO]: (target_vehicle_state): Received message: ");
        console.log(parsedData);
        visualizeTargetSteeringAngle(parsedData);
    }

    function sub_to_target_steering_angle() {
        // subscribe to course
        fetch(apiAddress + "/v1/navigator/target_steering_angle?" + new URLSearchParams({
            subscription_socket_id: sid,
            subscription_period_length: "0",
        }), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            return response.json();
        }).then((data) => {
            console.log("[INFO]: subscribed to hash " + data)

            event_id_to_function_map.set(data, target_steering_angle_update);
            $socket.on(data, target_steering_angle_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    // uncorrected location data
    function raw_location_update(data) {
        const parsedData = JSON.parse(data);
        console.log("[INFO]: (raw_location): Received message: ");
        console.log(parsedData);
        visualizeRawLocation(parsedData);
    }

    function sub_to_raw_location() {
        // subscribe to course
        fetch(apiAddress + "/v1/sensor/gps/location?" + new URLSearchParams({
            subscription_socket_id: sid,
            subscription_period_length: "100",
        }), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            return response.json();
        }).then((data) => {
            console.log("[INFO]: subscribed to hash " + data)

            event_id_to_function_map.set(data, raw_location_update);
            $socket.on(data, raw_location_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    $socket.on("connect", () => {
        console.log("[INFO]: Registered with socket id: " + $socket.id);
        sid = $socket.id;
        sub_to_course();
        sub_to_current_path();
        sub_to_vehicle_data();
        sub_to_target_steering_angle();
        sub_to_raw_location();
    });
    $socket.onAny((event, ...args) => {
        setTimeout(function () {
            if (event_id_to_function_map.has(event)) {
                event_id_to_function_map.get(event)(...args);
            } else {
                console.log("[INFO]: Received unknown event: " + event + " with args: " + args);
            }
        }, 1000);
    });
    $socket.connect();


</script>

<main>
    <Modals/>
    {#if showVisualizer}
        <Visualizer bind:visualizeCourse={visualizeCourse}
                    bind:visualizeMachineState={visualizeMachineState}
                    bind:visualizeRawLocation={visualizeRawLocation}
                    bind:visualizeTargetSteeringAngle={visualizeTargetSteeringAngle}
                    bind:visualizeCurrentPathId={visualizeCurrentPathId}
        />
        <!--<MetaButtons/> -->
        <ActionButtons/>
        <!--<StatusBar/> -->
    {:else}
        <Dashboard/>
    {/if}
    <SwitchButton bind:showVisualizer={showVisualizer}/>
</main>
