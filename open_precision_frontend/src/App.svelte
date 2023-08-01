<script context="module" lang="ts">
    export let apiAddress: string = window.location.href.slice(0, window.location.href.length - window.location.pathname.length) + "/api" + "/v1";
    console.log("[INFO]: using API address: " + apiAddress);
</script>
<script>
    import Visualizer from "./lib/Visualizer.svelte";
    import io from "socket.io-client";
    import ActionButtons from "./lib/ActionButtons.svelte";
    import Modals, {add} from "./lib/Modals/Modals.svelte";


    let visualizeMachineState;
    let visualizeCourse;
    let sid;

    function course_update(data) {
        console.log("[INFO]: (course): Received message: " + data);
        visualizeCourse(JSON.parse(data));
    }

    function sub_to_course() {
        // subscribe to course
        fetch(apiAddress + "/course/?" + new URLSearchParams({
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
            sock.on(data, course_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }


    // vehicle data
    function vehicle_data_update(data) {
        console.log("[INFO]: (vehicle_state): Received message: " + data);
        visualizeMachineState(JSON.parse(data));
    }

    function sub_to_vehicle_data() {
        // subscribe to course
        fetch(apiAddress + "/vehicle_state?" + new URLSearchParams({
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
            sock.on(data, vehicle_data_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    // vehicle data
    function target_steering_angle_update(data) {
        console.log("[INFO]: (target_vehicle_state): Received message: " + data);
        visualizeMachineState(JSON.parse(data));
    }

    function sub_to_target_steering_angle() {
        // subscribe to course
        fetch(apiAddress + "/navigator/target_steering_angle?" + new URLSearchParams({
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
            sock.on(data, target_steering_angle_update);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    let sock = io("ws://localhost:8000", {
        path: "/sockets/socket.io",
        transports: ['websocket', 'polling', 'flashsocket']
    });

    sock.on("connect", () => {
        console.log("[INFO]: Registered with socket id: " + sock.id);
        sid = sock.id;
        sub_to_course();
        //sub_to_vehicle_data();
        sub_to_target_steering_angle();
    });
    sock.connect();


</script>

<main>
    <Modals/>
    <Visualizer bind:visualizeMachineState={visualizeMachineState} bind:visualizeCourse={visualizeCourse}/>
    <!--<MetaButtons/> -->
    <ActionButtons/>
    <!--<StatusBar/> -->
</main>
