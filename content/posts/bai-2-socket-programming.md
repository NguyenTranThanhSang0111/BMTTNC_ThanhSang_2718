---
title: "Bài 2: Socket Programming cơ bản"
date: 2024-12-25
draft: false
weight: 2
categories: ["Java"]
tags: ["java", "socket", "lập trình mạng"]
description: "Tìm hiểu về Socket và cách sử dụng trong Java để giao tiếp qua mạng"
featuredImage: "/images/bai-2-socket-programming.jpg"
featuredImagePreview: "/images/bai-2-socket-programming.jpg"
images: ["/images/bai-2-socket-programming.jpg"]
---

## Socket là gì?

Socket là điểm cuối (endpoint) của kết nối hai chiều giữa hai chương trình chạy trên mạng. Trong Java, chúng ta sử dụng các class trong package `java.net` để làm việc với Socket.

## Các loại Socket

### 1. TCP Socket (Stream Socket)
- Kết nối đáng tin cậy, có đảm bảo thứ tự
- Sử dụng `ServerSocket` và `Socket`
- Phù hợp cho ứng dụng cần độ tin cậy cao

### 2. UDP Socket (Datagram Socket)
- Kết nối không đảm bảo, nhanh hơn
- Sử dụng `DatagramSocket` và `DatagramPacket`
- Phù hợp cho ứng dụng real-time

## Ví dụ TCP Socket đơn giản

### Server
```java
import java.io.*;
import java.net.*;

public class SimpleServer {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(8080);
            System.out.println("Server đang chờ kết nối...");
            
            Socket clientSocket = serverSocket.accept();
            System.out.println("Đã kết nối với client!");
            
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream())
            );
            
            String message = in.readLine();
            System.out.println("Nhận được: " + message);
            
            clientSocket.close();
            serverSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### Client
```java
import java.io.*;
import java.net.*;

public class SimpleClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 8080);
            
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            );
            
            out.println("Xin chào từ client!");
            
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Kết luận

Socket là nền tảng của lập trình mạng. Hiểu rõ Socket giúp bạn xây dựng các ứng dụng mạng hiệu quả.

