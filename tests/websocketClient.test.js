// tests/websocketClient.test.js

const WebSocket = require('ws');
const WebSocketClient = require('../src/websocketClient');
const SERVER_URL = 'ws://127.0.0.1:8000/ws/chat/test/';

// Mock the WebSocket
global.WebSocket = WebSocket;

describe('WebSocketClient', () => {
    let server;
    let client;

    beforeAll((done) => {
        // Start a WebSocket server
        server = new WebSocket.Server({ port: 8000 });

        server.on('connection', (ws) => {
            ws.on('message', (message) => {
                const data = JSON.parse(message);
                if (data.type === 'request_person_count') {
                    ws.send(JSON.stringify({ person: 5 }));
                } else if (data.type === 'other_type') {
                    ws.send(JSON.stringify({ other: 'This is another type of message' }));
                }
            });
        });

        // Allow some time for the server to start
        setTimeout(done, 100);
    });

    afterAll((done) => {
        // Close the WebSocket server
        server.close(done);
    });

    beforeEach(() => {
        // Initialize the client
        client = new WebSocketClient(SERVER_URL);
    });

    test('should connect to the WebSocket server', (done) => {
        client.connect();

        client.socket.onopen = () => {
            expect(client.socket.readyState).toBe(WebSocket.OPEN);
            done();
        };
    });

    test('should receive the number of people from the WebSocket server', (done) => {
        client.connect();

        client.socket.onopen = () => {
            client.sendMessage({ type: 'request_person_count' });
        };

        client.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            expect(data.person).toBe(5);
            done();
        };
    });

    test('should receive another type of message from the WebSocket server', (done) => {
        client.connect();

        client.socket.onopen = () => {
            client.sendMessage({ type: 'other_type' });
        };

        client.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            expect(data.other).toBe('This is another type of message');
            done();
        };
    });
});
