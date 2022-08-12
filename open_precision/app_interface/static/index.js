import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.121.1/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js';

// init app constants
const colorLight = 0xFFFDFA;
const colorNeutral= 0x434345;
const colorDark = 0x241F19;
const colorBaseLight = 0xFCA647;
const colorBase = 0xFB8604;
const colorBaseDark = 0xc96b03;



// set up three.js
const canvas = document.querySelector('#c');
const renderer = new THREE.WebGLRenderer({canvas});

const fov = 85;
const aspect = 2;  // the canvas default
const near = 0.1;
const far = 50;
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
camera.up.set( 0, 0, 1 );
const controls = new OrbitControls(camera, canvas);
camera.position.x = -6;
camera.position.z = 6;
// camera.rotation.x = Math.PI / 2;
// camera.rotation.y = -  Math.PI / 2;
camera.rotation.z = -  Math.PI / 2;

controls.update();
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
const tractor_pointer = new THREE.Mesh(new THREE.ConeGeometry(0.7, 2, 32), new THREE.MeshPhongMaterial({color: colorBase}));
tractor_pointer.rotation.z = - Math.PI / 2;
const plane_pointer = new THREE.Mesh(new THREE.CircleGeometry(1.5, 32), new THREE.MeshPhongMaterial({color: colorNeutral}));
plane_pointer.rotation.z = - Math.PI / 2;

const pointer = new THREE.Group();
pointer.add(tractor_pointer)
pointer.add(plane_pointer)
scene.add(pointer)

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

// implement project specific functions

function renderCourse(course) {
    console.log('rendering course');
    console.log(course.paths);
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



// target_machine_state websocket
function updateTargetMachineState(data){
    console.log("steering_angle: " + data.steering_angle);
}


var ws_target_machine_state = new WebSocket("ws://localhost:8000/ws/target_machine_state");
console.log('[INFO]: (target_machine_state): waiting for connection');

ws_target_machine_state.onopen = function(event) {
    console.log('[INFO]: (target_machine_state): Listening...]');
    ws_target_machine_state.send('');
}

ws_target_machine_state.onmessage = function(event) {
    updateTargetMachineState(JSON.parse(event.data));
    console.log("[INFO]: (target_machine_state): Received message: " + event.data);
};

ws_target_machine_state.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[INFO]: (target_machine_state): Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    alert('[ERROR]: (target_machine_state): Connection died');
  }
};

ws_target_machine_state.onerror = function(error) {
  alert(`[error] (target_machine_state): ${error.message}`);
};

// position websocket

function updatePosition(data) {
    console.log(data);
    pointer.position.x = data.location.x;
    pointer.position.y = data.location.y;
    pointer.position.z = data.location.z;
    pointer.rotation.setFromQuaternion(new THREE.Quaternion(data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w));
}


var ws_position = new WebSocket("ws://localhost:8000/ws/position");
console.log('[INFO]: (position): waiting for connection');

ws_position.onopen = function(event) {
    console.log('[INFO]: (position): Listening...]');
    ws_position.send('');
}

ws_position.onmessage = function(event) {
    updatePosition(JSON.parse(event.data));
    console.log("[INFO]: (position): Received message: " + event.data);
};

ws_position.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[INFO]: (position): Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    alert('[ERROR]: (position): Connection died');
  }
};

ws_position.onerror = function(error) {
  alert(`[error] (position): ${error.message}`);
};

requestAnimationFrame(render);