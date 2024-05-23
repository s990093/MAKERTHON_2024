// tests/websocketClient.test.js

import WebSocket from 'ws';
const SERVER_URL = 'ws://127.0.0.1:8000/ws/chat/test/';
// const SERVER_URL = 'ws://49.213.238.75:5000/ws/chat/test/';
const PORT = 5000
// Mock the WebSocket
global.WebSocket = WebSocket;
// 创建 WebSocket 连接



test('接收广播消息', (done) => {
    const socket = new WebSocket(SERVER_URL);

    socket.on('open', () => {
        console.log('WebSocket 连接已打开');
        // 这里可以添加任何你需要执行的逻辑
    });

    socket.on('message', (data) => {
        const message = JSON.parse(data);
        console.log('接收到消息:', message.message);
        // 这里可以进行断言，或者执行其他测试逻辑
        expect(message.message).toBe('Hello, world!');
        done(); // 调用 done() 表示测试完成
    });

    socket.on('close', () => {
        console.log('WebSocket 连接已关闭');
    });

    socket.on('error', (error) => {
        console.error('WebSocket 错误:', error);
        done(error); // 如果发生错误，调用 done() 并传递错误表示测试失败
    });
});
