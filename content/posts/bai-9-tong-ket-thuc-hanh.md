---
title: "Bài 9: Tổng kết và Dự án thực hành"
date: 2025-01-01
draft: false
weight: 9
categories: ["Java"]
tags: ["java", "tổng kết", "thực hành", "dự án"]
description: "Tổng kết kiến thức và hướng dẫn xây dựng dự án thực hành hoàn chỉnh"
featuredImage: "images/bai-9-tong-ket-thuc-hanh.jpg"
featuredImagePreview: "images/bai-9-tong-ket-thuc-hanh.jpg"
images: ["images/bai-9-tong-ket-thuc-hanh.jpg"]
---

## Tổng kết kiến thức

Qua 8 bài học, chúng ta đã học:

1. **Java cơ bản**: Ngôn ngữ và môi trường phát triển
2. **Socket Programming**: TCP và UDP sockets
3. **TCP Server/Client**: Xây dựng ứng dụng client-server
4. **UDP Communication**: Giao tiếp không kết nối
5. **HTTP Client**: Gọi REST API từ Java
6. **Spring Boot**: Framework web hiện đại
7. **RESTful API**: Best practices và design patterns
8. **WebSocket**: Giao tiếp real-time

## Dự án thực hành: Chat Application

Hãy xây dựng một ứng dụng chat hoàn chỉnh kết hợp tất cả kiến thức đã học!

### Yêu cầu

1. **Backend (Spring Boot)**
   - REST API để quản lý users
   - WebSocket cho chat real-time
   - Lưu trữ tin nhắn vào database

2. **Frontend (HTML/JavaScript)**
   - Giao diện chat đơn giản
   - Kết nối WebSocket
   - Hiển thị danh sách users

### Cấu trúc Project

```
chat-app/
├── backend/
│   ├── src/main/java/
│   │   └── com/example/chat/
│   │       ├── ChatApplication.java
│   │       ├── controller/
│   │       │   ├── UserController.java
│   │       │   └── ChatController.java
│   │       ├── model/
│   │       │   ├── User.java
│   │       │   └── Message.java
│   │       ├── service/
│   │       │   └── ChatService.java
│   │       └── config/
│   │           └── WebSocketConfig.java
│   └── pom.xml
└── frontend/
    ├── index.html
    ├── chat.js
    └── style.css
```

### Backend Implementation

#### Message Model

```java
package com.example.chat.model;

import java.time.LocalDateTime;

public class Message {
    private Long id;
    private String sender;
    private String content;
    private LocalDateTime timestamp;
    private MessageType type;
    
    public enum MessageType {
        CHAT, JOIN, LEAVE
    }
    
    // Constructors, getters, setters
}
```

#### Chat Service

```java
package com.example.chat.service;

import com.example.chat.model.Message;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class ChatService {
    private List<Message> messages = new ArrayList<>();
    private Set<String> onlineUsers = new HashSet<>();
    
    public void saveMessage(Message message) {
        message.setId((long) (messages.size() + 1));
        message.setTimestamp(LocalDateTime.now());
        messages.add(message);
    }
    
    public List<Message> getRecentMessages(int limit) {
        return messages.stream()
            .sorted((a, b) -> b.getTimestamp()
                .compareTo(a.getTimestamp()))
            .limit(limit)
            .collect(Collectors.toList());
    }
    
    public void addUser(String username) {
        onlineUsers.add(username);
    }
    
    public void removeUser(String username) {
        onlineUsers.remove(username);
    }
    
    public Set<String> getOnlineUsers() {
        return new HashSet<>(onlineUsers);
    }
}
```

#### REST Controller

```java
@RestController
@RequestMapping("/api")
public class ApiController {
    
    @Autowired
    private ChatService chatService;
    
    @GetMapping("/users/online")
    public ResponseEntity<Set<String>> getOnlineUsers() {
        return ResponseEntity.ok(chatService.getOnlineUsers());
    }
    
    @GetMapping("/messages")
    public ResponseEntity<List<Message>> getMessages(
            @RequestParam(defaultValue = "50") int limit) {
        return ResponseEntity.ok(
            chatService.getRecentMessages(limit)
        );
    }
}
```

### Frontend Implementation

#### HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Chat Application</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="chat-header">
            <h2>Chat Room</h2>
            <div id="online-users"></div>
        </div>
        
        <div id="messages" class="messages"></div>
        
        <div class="input-area">
            <input type="text" id="message-input" 
                   placeholder="Nhập tin nhắn...">
            <button onclick="sendMessage()">Gửi</button>
        </div>
    </div>
    
    <script src="sockjs.min.js"></script>
    <script src="stomp.min.js"></script>
    <script src="chat.js"></script>
</body>
</html>
```

#### JavaScript

```javascript
let stompClient = null;
let username = null;

function connect() {
    username = prompt('Nhập tên của bạn:');
    
    const socket = new SockJS('/ws');
    stompClient = Stomp.over(socket);
    
    stompClient.connect({}, function(frame) {
        // Join chat
        stompClient.send("/app/chat.addUser", {},
            JSON.stringify({
                sender: username,
                type: 'JOIN'
            })
        );
        
        // Subscribe to messages
        stompClient.subscribe('/topic/public', function(message) {
            const chatMessage = JSON.parse(message.body);
            displayMessage(chatMessage);
        });
        
        // Load online users
        loadOnlineUsers();
    });
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const content = input.value.trim();
    
    if (content && stompClient) {
        const message = {
            sender: username,
            content: content,
            type: 'CHAT'
        };
        
        stompClient.send("/app/chat.sendMessage", {},
            JSON.stringify(message));
        
        input.value = '';
    }
}

function displayMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = 
        `<strong>${message.sender}</strong>: ${message.content}`;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function loadOnlineUsers() {
    fetch('/api/users/online')
        .then(response => response.json())
        .then(users => {
            const usersDiv = document.getElementById('online-users');
            usersDiv.innerHTML = 
                `Online: ${users.join(', ')}`;
        });
}

// Connect when page loads
connect();
```

## Mở rộng dự án

Sau khi hoàn thành cơ bản, bạn có thể thêm:

1. **Database**: Lưu tin nhắn vào MySQL/PostgreSQL
2. **Authentication**: Đăng nhập/đăng ký
3. **Private Chat**: Chat riêng tư giữa 2 users
4. **File Upload**: Gửi hình ảnh, file
5. **Emoji Support**: Hỗ trợ emoji
6. **Message History**: Lịch sử tin nhắn

## Tài nguyên học tập

- **Official Docs**: 
  - [Spring Boot](https://spring.io/projects/spring-boot)
  - [Spring WebSocket](https://docs.spring.io/spring-framework/reference/web/websocket.html)
  
- **Practice Platforms**:
  - LeetCode (Java problems)
  - HackerRank (Java challenges)
  
- **Projects Ideas**:
  - File sharing application
  - Real-time dashboard
  - Multiplayer game server

## Kết luận

Chúc mừng bạn đã hoàn thành khóa học! Bây giờ bạn đã có đủ kiến thức để:
- Xây dựng ứng dụng mạng với Java
- Tạo RESTful API với Spring Boot
- Phát triển tính năng real-time với WebSocket
- Áp dụng best practices trong lập trình mạng

Hãy tiếp tục thực hành và xây dựng các dự án của riêng bạn!

