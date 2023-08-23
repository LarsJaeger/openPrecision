<script>
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.121.1/build/three.module.js';
    //import * as THREE from 'three';
    import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js';
    import {onMount} from "svelte";
    //import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

    // init app constants
    const colorLight = 0xFFFDFA;
    const colorNeutral = 0x434345;
    const colorDark = 0x241F19;
    const colorBaseLight = 0xFCA647;
    const colorBase = 0xFB8604;
    const colorBaseDark = 0xc96b03;

    //init steering monitor
    let visualizedTargetSteeringAngle = 0;


    // set up three.js
    let canvas;


    const fov = 85;
    const aspect = 2;  // the canvas default
    const near = 0.1;
    const far = 50;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.up.set(0, 0, 1);

    camera.position.x = -6;
    camera.position.z = 6;
    // camera.rotation.x = Math.PI / 2;
    // camera.rotation.y = -  Math.PI / 2;
    camera.rotation.z = -Math.PI / 2;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(colorLight); // set background color of three.js scene
    // add lights
    const light = new THREE.AmbientLight(0x505050, 2);
    light.position.set(0, 0, 4);
    scene.add(light);

    // add axes helper
    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);

    // create main pointer
    const pointer = new THREE.Group();

    const tractor_pointer = new THREE.Mesh(new THREE.ConeGeometry(0.7, 2, 32), new THREE.MeshPhongMaterial({color: colorBase}));
    tractor_pointer.rotation.z = -Math.PI / 2;
    pointer.add(tractor_pointer);

    const plane_pointer = new THREE.Mesh(new THREE.CircleGeometry(1.5, 32), new THREE.MeshPhongMaterial({color: colorNeutral}));
    plane_pointer.rotation.z = -Math.PI / 2;
    pointer.add(plane_pointer);

    scene.add(pointer);

    function resizeRendererToDisplaySize(renderer) {
        const canvas = renderer.domElement;
        const pixelRatio = window.devicePixelRatio;
        const width = canvas.clientWidth * pixelRatio | 0;
        const height = canvas.clientHeight * pixelRatio | 0;
        const needResize = canvas.width !== width || canvas.height !== height;
        if (needResize) {
            renderer.setSize(width, height, false);
        }
        return needResize;
    }

    function makeRender(renderer, controls) {
        function render(time) {
            time *= 0.001;

            if (resizeRendererToDisplaySize(renderer)) {
                const canvas = renderer.domElement;
                camera.aspect = canvas.clientWidth / canvas.clientHeight;
                camera.updateProjectionMatrix();
            }
            controls.update()
            renderer.render(scene, camera);
            requestAnimationFrame(render);
        }

        return render;
    }

    onMount(() => {
        const renderer = new THREE.WebGLRenderer({canvas});
        const controls = new OrbitControls(camera, canvas);

        const render = makeRender(renderer, controls);

        // request first frame
        requestAnimationFrame(render);
    });

    // implement visualizer functions
    export function visualizeCourse(data) {
        data["connections"].forEach(conn => {
            // find and add starting point of path
            if (conn["a"].startsWith("Path") && conn["relationship"] === "BEGINS_WITH" && conn["b"].startsWith("Waypoint")) {
                let wp = data.objects[conn["b"]];
                console.log(wp);
                const pathLinePoints = [];
                pathLinePoints.push(new THREE.Vector3(wp.location.x, wp.location.y, wp.location.z));

                // iterate over successors and add to line
                data["connections"].forEach(sub_conn => {
                    if (sub_conn["a"] === conn["b"] && sub_conn["relationship"] === "SUCCESSOR" && sub_conn["b"].startsWith("Waypoint")) {
                        wp = data.objects[sub_conn["b"]];
                        pathLinePoints.push(new THREE.Vector3(wp.location.x, wp.location.y, wp.location.z));
                    }
                });
                const pathLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pathLinePoints), new THREE.LineBasicMaterial({color: 0x00ffff}));
                scene.add(pathLine);
            }
        });
    }

    export function visualizeMachineState(data) {
        console.log(data);
        pointer.position.x = data.position.location.x;
        pointer.position.y = data.position.location.y;
        pointer.position.z = data.position.location.z;
        pointer.rotation.setFromQuaternion(new THREE.Quaternion(data.position.orientation.x, data.position.orientation.y, data.position.orientation.z, data.position.orientation.w));
    }

    //currently just a stump:
    export function visualizeTargetSteeringAngle(data) {
        visualizedTargetSteeringAngle = data;
    }




</script>

<div>
    <canvas class="u-position-absolute u-full-screen-height u-width-full-line u-z-index-0" bind:this={canvas}></canvas>
    <div style="position: fixed; right: 7rem; bottom: 8rem;">
        <span aria-hidden="true" class="u-position-absolute icon-plus is-big u-z-index-1"
              style="color:black; font-size: 7em;"></span>
        <span aria-hidden="true"
              class="u-position-absolute icon-arrow-narrow-up is-big u-z-index-10" style="color:red; font-size: 7em; rotate: {visualizedTargetSteeringAngle}deg"></span>
    </div>
</div>
<style>
</style>