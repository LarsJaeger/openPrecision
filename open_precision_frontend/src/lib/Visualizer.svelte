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
    let controls;

    const scene = new THREE.Scene();

    const fov = 85;
    const aspect = 2;  // the canvas default
    const near = 0.1;
    const far = 5000;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.up.set(0, 0, 1);

    camera.position.x = -6;
    camera.position.y = 0;
    camera.position.z = 6;
    // camera.rotation.x = Math.PI / 2;
    // camera.rotation.y = -  Math.PI / 2;
    camera.rotation.z = -Math.PI / 2;
    camera.lookAt(0, 0, 0);
    scene.background = new THREE.Color(colorLight); // set background color of three.js scene

    scene.add(camera);
    const proxy_camera = camera.clone();

    // let world_offset = null; TODO
    let locError = null;

    let pathIdPathMap = new Map();
    let currentPathId= null;
    const pathMaterialColor = 0x00ffff;
    const currentPathMaterialColor = 0x1313ff;
    const course_group = new THREE.Group();
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
    // add lights
    const light = new THREE.AmbientLight(0x505050, 2);
    light.position.set(0, 0, 4);
    pointer.add(light);
    //pointer.add(camera);

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

    function makeRender(renderer, inner_controls) {
        controls = inner_controls;

        function animate(time) {
            time *= 0.001;

            if (resizeRendererToDisplaySize(renderer)) {
                const canvas = renderer.domElement;
                camera.aspect = canvas.clientWidth / canvas.clientHeight;
                proxy_camera.aspect = canvas.clientWidth / canvas.clientHeight;
                camera.updateProjectionMatrix();
                proxy_camera.updateProjectionMatrix();
            }
            controls.update();
            const translatedCameraPosition = pointer.position.clone().add(proxy_camera.position.clone().applyQuaternion(pointer.quaternion));
            const translatedCameraRotation = pointer.quaternion.clone().multiply(proxy_camera.quaternion);

            camera.rotation.setFromQuaternion(translatedCameraRotation);
            camera.position.set(
                translatedCameraPosition.x,
                translatedCameraPosition.y,
                translatedCameraPosition.z);


            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        return animate;
    }

    onMount(() => {
        const renderer = new THREE.WebGLRenderer({canvas});
        const controls = new OrbitControls(proxy_camera, canvas);
        controls.update();
        // request first frame
        const render = makeRender(renderer, controls);
        requestAnimationFrame(render);
    });

    export function visualizeCurrentPathId(data){
        if (currentPathId !== null) {
            const oldPath = pathIdPathMap.get(currentPathId);
            oldPath.material = new THREE.LineBasicMaterial({color: pathMaterialColor});
            oldPath.material.needsUpdate = true;
        }
        const newCurrentPathId = data.current_path_id;
        if (newCurrentPathId !== null) {
            const newPath = pathIdPathMap.get(newCurrentPathId);
            newPath.material = new THREE.LineBasicMaterial({color: currentPathMaterialColor});
            newPath.material.needsUpdate = true;
        }
        currentPathId = newCurrentPathId;
    }

    // implement visualizer functions
    export function visualizeCourse(data) {
        console.log("[DEBUG]: visualizing course");
        console.log(data);
        scene.remove(course_group);
        data["relations"].forEach(conn => {
            // find and add starting point of path
            if (conn["a"].startsWith("Path") && conn["name"] === "BEGINS_WITH" && conn["b"].startsWith("Waypoint")) {
                let wp = data.nodes[conn["b"]];
                const pathLinePoints = [];
                pathLinePoints.push(new THREE.Vector3(wp.location.x, wp.location.y, wp.location.z));


                // iterate over successors and add to line
                data["relations"].forEach(sub_conn => {
                    if (sub_conn["b"] === conn["b"] && sub_conn["name"] === "SUCCESSOR" && sub_conn["a"].startsWith("Waypoint")) {
                        wp = data.nodes[sub_conn["a"]];
                        pathLinePoints.push(new THREE.Vector3(wp.location.x, wp.location.y, wp.location.z));
                    }
                });
                const pathLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pathLinePoints), new THREE.LineBasicMaterial({color: pathMaterialColor}));
                const pathId = conn["a"].split(" ")[1]; 
                pathIdPathMap.set(pathId, pathLine);
                course_group.add(pathLine);
            }
        });
        scene.add(course_group);
        // update current path color
        if (currentPathId !== null) {
            const currentPath = pathIdPathMap.get(currentPathId);
            currentPath.material = new THREE.LineBasicMaterial({color: currentPathMaterialColor});
            currentPath.material.needsUpdate = true;
        }
    }

    export function visualizeMachineState(data) {
        pointer.position.set(
            data.position.location.x,
            data.position.location.y,
            data.position.location.z
        );
        const quat = new THREE.Quaternion(data.position.orientation.q[1], data.position.orientation.q[2], data.position.orientation.q[3], data.position.orientation.q[0]);
        pointer.rotation.setFromQuaternion(quat);
        axesHelper.position.set(
            data.position.location.x,
            data.position.location.y,
            data.position.location.z
        );
    }

    //currently just a stump:
    export function visualizeTargetSteeringAngle(data) {
        visualizedTargetSteeringAngle = data;
    }

    const geometry = new THREE.SphereGeometry(0.1, 8, 8); //radius, widthSegments, heightSegments
    const material = new THREE.MeshBasicMaterial({color: 0xffff00});
    // const sphere = new THREE.Mesh(geometry, material);
    // scene.add(sphere);

    export function visualizeRawLocation(data) {
        locError=data.error
        const sphere = new THREE.Mesh(geometry, material);
        sphere.position.x = data.x;
        sphere.position.y = data.y;
        sphere.position.z = data.z;
        scene.add(sphere);
    }


</script>
<canvas bind:this={canvas} class="u-position-absolute u-full-screen-height u-width-full-line u-z-index-0"></canvas>
<!-- precision indicator -->
{#if locError !== null}
<div class="u-z-index-10 u-position-fixed" style="left: 6rem; bottom: 0.5rem;"> 
    <p class="text u-large u-bold" style="color:black">&pm;{(locError * 100).toFixed(2)}cm</p>
</div>
{/if}
<!-- steering indicator: -->
<div class="u-z-index-10 u-position-fixed" style="right: 7rem; bottom: 8rem;">
    <span aria-hidden="true" class="u-position-absolute icon-plus is-big"
          style="color:black; font-size: 7em;"></span>
    <span aria-hidden="true"
          class="u-position-absolute icon-arrow-narrow-up is-big"
          style="color:red; font-size: 7em; rotate: {visualizedTargetSteeringAngle}rad"></span>
</div>
<style>
</style>
