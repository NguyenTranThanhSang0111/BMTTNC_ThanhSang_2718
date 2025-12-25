---
title: "Bài 8: WebSocket - Giao tiếp Real-time"
date: 2024-12-31
draft: false
weight: 8
categories: ["Java"]
tags: ["java", "websocket", "real-time", "spring"]
description: "Học cách sử dụng WebSocket để xây dựng ứng dụng real-time với Spring"
featuredImage: "/images/bai-8-websocket.jpg"
featuredImagePreview: "/images/bai-8-websocket.jpg"
images: ["/images/bai-8-websocket.jpg"]
---

## WebSocket là gì?

WebSocket là giao thức cho phép giao tiếp hai chiều (full-duplex) giữa client và server qua một kết nối TCP duy nhất. Khác với HTTP request/response, WebSocket duy trì kết nối mở để trao đổi dữ liệu real-time.

## Khi nào dùng WebSocket?

- **Chat applications**: Tin nhắn tức thời
- **Gaming**: Cập nhật trạng thái game real-time
- **Trading platforms**: Giá cổ phiếu, tiền điện tử
- **Collaborative tools**: Google Docs, Figma
- **Notifications**: Thông báo push real-time

## WebSocket vs HTTP

| HTTP | WebSocket |
|------|----------|
| Request/Response | Full-duplex |
| Mỗi request mới kết nối | Kết nối persistent |
| Server không thể gửi trước | Server có thể gửi bất kỳ lúc nào |
| Overhead lớn | Overhead nhỏ |

## Spring WebSocket Setup

### Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

### Configuration

```java
package com.example.demo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.*;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*")
                .withSockJS();
    }
    
    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic", "/queue");
        registry.setApplicationDestinationPrefixes("/app");
    }
}
```

## WebSocket Controller

```java
package com.example.demo.controller;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
public class ChatController {
    
    @MessageMapping("/chat.sendMessage")
    @SendTo("/topic/public")
    public ChatMessage sendMessage(@Payload ChatMessage chatMessage) {
        return chatMessage;
    }
    
    @MessageMapping("/chat.addUser")
    @SendTo("/topic/public")
    public ChatMessage addUser(@Payload ChatMessage chatMessage,
                               SimpMessageHeaderAccessor headerAccessor) {
        headerAccessor.getSessionAttributes()
            .put("username", chatMessage.getSender());
        return chatMessage;
    }
}
```

## Message Model

```java
package com.example.demo.model;

public class ChatMessage {
    private MessageType type;
    private String content;
    private String sender;
    
    public enum MessageType {
        CHAT,
        JOIN,
        LEAVE
    }
    
    // Getters and setters
    public MessageType getType() { return type; }
    public void setType(MessageType type) { this.type = type; }
    
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    
    public String getSender() { return sender; }
    public void setSender(String sender) { this.sender = sender; }
}
```

## Client-side (JavaScript)

```javascript
// Kết nối WebSocket
const socket = new SockJS('http://localhost:8080/ws');
const stompClient = Stomp.over(socket);

stompClient.connect({}, function (frame) {
    console.log('Connected: ' + frame);
    
    // Subscribe để nhận tin nhắn
    stompClient.subscribe('/topic/public', function (message) {
        const chatMessage = JSON.parse(message.body);
        displayMessage(chatMessage);
    });
});

// Gửi tin nhắn
function sendMessage() {
    const message = {
        type: 'CHAT',
        content: document.getElementById('message').value,
        sender: username
    };
    
    stompClient.send("/app/chat.sendMessage", {}, 
        JSON.stringify(message));
}

// Hiển thị tin nhắn
function displayMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = 
        message.sender + ': ' + message.content;
    document.getElementById('messages')
        .appendChild(messageElement);
}
```

## Private Messaging

Để gửi tin nhắn riêng tư:

```java
@MessageMapping("/chat.private")
public void sendPrivateMessage(@Payload ChatMessage message,
                               SimpMessageHeaderAccessor headerAccessor) {
    String sender = (String) headerAccessor.getSessionAttributes()
        .get("username");
    
    message.setSender(sender);
    
    messagingTemplate.convertAndSendToUser(
        message.getReceiver(),
        "/queue/private",
        message
    );
}
```

## Broadcasting với @SendToUser

```java
@MessageMapping("/notifications")
@SendToUser("/queue/notifications")
public Notification sendNotification(@Payload Notification notification) {
    return notification;
}
```

## Xử lý Connection Events

```java
@Component
public class WebSocketEventListener {
    
    @EventListener
    public void handleWebSocketConnectListener(SessionConnectedEvent event) {
        System.out.println("Received a new web socket connection");
    }
    
    @EventListener
    public void handleWebSocketDisconnectListener(SessionDisconnectEvent event) {
        StompHeaderAccessor headerAccessor = 
            StompHeaderAccessor.wrap(event.getMessage());
        
        String username = (String) headerAccessor.getSessionAttributes()
            .get("username");
        
        if (username != null) {
            ChatMessage chatMessage = new ChatMessage();
            chatMessage.setType(ChatMessage.MessageType.LEAVE);
            chatMessage.setSender(username);
            
            messagingTemplate.convertAndSend("/topic/public", chatMessage);
        }
    }
}
```

## Security

Bảo mật WebSocket connection:

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketSecurityConfig 
    implements WebSocketMessageBrokerConfigurer {
    
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*")
                .withSockJS();
    }
    
    @Override
    public void configureClientInboundChannel(
            ChannelRegistration registration) {
        registration.interceptors(new ChannelInterceptor() {
            @Override
            public Message<?> preSend(Message<?> message, 
                                     MessageChannel channel) {
                // Validate token, check authentication
                return message;
            }
        });
    }
}
```

## Kết luận

WebSocket là công nghệ mạnh mẽ cho ứng dụng real-time. Với Spring WebSocket, bạn có thể dễ dàng xây dựng chat, notification, và các tính năng real-time khác.

