---
title: "Bài 3: Xây dựng TCP Server và Client"
date: 2024-12-26
draft: false
weight: 3
categories: ["Java"]
tags: ["java", "tcp", "server", "client"]
description: "Học cách xây dựng ứng dụng TCP Server/Client hoàn chỉnh với Java"
featuredImage: "/images/bai-3-tcp-server-client.jpg"
featuredImagePreview: "/images/bai-3-tcp-server-client.jpg"
images: ["/images/bai-3-tcp-server-client.jpg"]
---

## TCP Server/Client Architecture

Mô hình Client-Server là kiến trúc phổ biến nhất trong lập trình mạng:
- **Server**: Lắng nghe kết nối và xử lý yêu cầu
- **Client**: Kết nối đến server và gửi yêu cầu

## TCP Server đa luồng

Để server có thể xử lý nhiều client đồng thời, chúng ta sử dụng đa luồng (multithreading).

```java
import java.io.*;
import java.net.*;

public class MultiThreadedServer {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(8080);
            System.out.println("Server đang chạy trên port 8080...");
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client mới kết nối: " + 
                    clientSocket.getInetAddress());
                
                // Tạo thread mới cho mỗi client
                ClientHandler handler = new ClientHandler(clientSocket);
                new Thread(handler).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {
    private Socket socket;
    
    public ClientHandler(Socket socket) {
        this.socket = socket;
    }
    
    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            );
            
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                System.out.println("Nhận được: " + inputLine);
                
                // Echo lại cho client
                out.println("Echo: " + inputLine);
                
                if (inputLine.equals("quit")) {
                    break;
                }
            }
            
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## TCP Client tương tác

```java
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class InteractiveClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 8080);
            
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            );
            
            Scanner scanner = new Scanner(System.in);
            String userInput;
            
            System.out.println("Kết nối thành công! Gõ 'quit' để thoát.");
            
            while (true) {
                System.out.print("Nhập tin nhắn: ");
                userInput = scanner.nextLine();
                
                out.println(userInput);
                
                if (userInput.equals("quit")) {
                    break;
                }
                
                String response = in.readLine();
                System.out.println("Server: " + response);
            }
            
            socket.close();
            scanner.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Xử lý lỗi và đóng kết nối

Luôn nhớ:
- Đóng các stream trước khi đóng socket
- Xử lý ngoại lệ một cách cẩn thận
- Sử dụng try-with-resources để tự động đóng tài nguyên

```java
try (Socket socket = new Socket("localhost", 8080);
     BufferedReader in = new BufferedReader(
         new InputStreamReader(socket.getInputStream())
     );
     PrintWriter out = new PrintWriter(
         socket.getOutputStream(), true
     )) {
    // Sử dụng socket
} catch (IOException e) {
    e.printStackTrace();
}
```

## Thực hành

Hãy thử xây dựng một chat server đơn giản cho phép nhiều client chat với nhau!

