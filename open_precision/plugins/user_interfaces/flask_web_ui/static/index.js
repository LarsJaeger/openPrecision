import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.121.1/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js';
import { io } from "https://cdn.socket.io/4.3.2/socket.io.esm.min.js";

function main() {
    const canvas = document.querySelector('#c');
    const renderer = new THREE.WebGLRenderer({canvas});

    const fov = 85;
    const aspect = 2;  // the canvas default
    const near = 0.1;
    const far = 50;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

    const controls = new OrbitControls(camera, renderer.domElement);

    camera.position.z = -6;
    camera.position.y = 6
    controls.update()
    const scene = new THREE.Scene();



    const light = new THREE.AmbientLight( 0x505050, 2);
    light.position.set(0, 0, 4);
    scene.add(light);

    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);

    // create main pointer
    const tractor_pointer = new THREE.Mesh(new THREE.ConeGeometry(0.7, 2, 32), new THREE.MeshPhongMaterial({ color:0xff0000}));
    tractor_pointer.rotation.x = Math.PI / 2;
    const plane_pointer =  new THREE.Mesh(new THREE.CircleGeometry(1.5, 32), new THREE.MeshPhongMaterial({ color:0x0000ff}));
    plane_pointer.rotation.x = -Math.PI / 2;

    const pointer = new THREE.Group();
    pointer.add(tractor_pointer)
    pointer.add(plane_pointer)
    scene.add(pointer)

    // drawing lines
    const points = [];
    points.push( new THREE.Vector3( -10, 1, 0 ) );
    points.push( new THREE.Vector3( 0, 0, 0 ) );
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), new THREE.LineBasicMaterial({ color: 0x00ffff }));
    scene.add(line);

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

    function render(time) {
        time *= 0.001;

        if (resizeRendererToDisplaySize(renderer)) {
            const canvas = renderer.domElement;
            camera.aspect = canvas.clientWidth / canvas.clientHeight;
            camera.updateProjectionMatrix();
        }

        /* cubes.forEach((cube, ndx) => {
          const speed = 1 + ndx * .1;
          const rot = time * speed;
          cube.rotation.x = rot;
          cube.rotation.y = rot;
        }); */

        controls.update()
        renderer.render(scene, camera);

        requestAnimationFrame(render);
    }

    requestAnimationFrame(render);
}
var course;
var socket = io();
socket.on('course', (arg) => {
    //socket.emit('ping_response', {data: 'I\'m connected!'});
    course = arg['Course'];
    console.log(course);
});
socket.emit('ping', true)
main();
