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

    export function visualizeCourse(course) {
        for (const pathIndex in course.paths) {
            const path = course.paths[pathIndex];
            console.log(path);
            const pathLinePoints = [];
            pathLinePoints.push(new THREE.Vector3(0));
            for (const wpIndex in path.waypoints) {
                const wp = path.waypoints[wpIndex];
                pathLinePoints.push(new THREE.Vector3(wp.location.x, wp.location.y, wp.location.z));
            }
            const pathLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pathLinePoints), new THREE.LineBasicMaterial({color: 0x00ffff}));
            scene.add(pathLine);
        }
    }

    export function visualizeMachineState(data) {
        console.log(data);
        pointer.position.x = data.position.location.x;
        pointer.position.y = data.position.location.y;
        pointer.position.z = data.position.location.z;
        pointer.rotation.setFromQuaternion(new THREE.Quaternion(data.position.orientation.x, data.position.orientation.y, data.position.orientation.z, data.position.orientation.w));
    }



</script>

<div class="visualizer">
    <canvas id="c" bind:this={canvas}></canvas>
</div>
<style>
    #c {
        width: 100vw;
        height: 100vh;
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
    }
</style>