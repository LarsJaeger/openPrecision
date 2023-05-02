import {readable} from "svelte/store";
import io from "socket.io-client";

export const socket = readable(null, function start(set) {
    let socket = io("ws://localhost:8000/"); //("ws://" + window.location.hostname + "/")
    set(socket);

	return function stop() {
        socket.close()
	};
});