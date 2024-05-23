const WebSocket = require('ws');


// websocketClient.js

class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.socket = null;
    }

    connect() {
        this.socket = new WebSocket(this.url);

        this.socket.onopen = (event) => {
            console.log("WebSocket is open now.");
        };

        this.socket.onmessage = (event) => {
            console.log("WebSocket message received:", event.data);
        };

        this.socket.onclose = (event) => {
            console.log("WebSocket is closed now.");
        };

        this.socket.onerror = (error) => {
            console.log("WebSocket error:", error);
        };
    }

    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        }
    }
}

module.exports = WebSocketClient;
