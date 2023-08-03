import {readable} from "svelte/store";
import io from "socket.io-client";
import {backendAddress} from "./App.svelte";

export const socket = readable(null, function start(set) {
    let socket = io(backendAddress, {
        path: "/sockets/socket.io",
        transports: ['websocket', 'polling', 'flashsocket']
    }); //("ws://" + window.location.hostname + "/"):
    set(socket);

    return function stop() {
        socket.close()
    };
});