---
title: "Bài 4: Giao tiếp UDP trong Java"
date: 2024-12-27
draft: false
weight: 4
categories: ["Java"]
tags: ["java", "udp", "datagram"]
description: "Tìm hiểu về UDP và cách sử dụng DatagramSocket trong Java"
featuredImage: "images/bai-4-udp-communication.jpg"
featuredImagePreview: "images/bai-4-udp-communication.jpg"
images: ["images/bai-4-udp-communication.jpg"]
---

## UDP vs TCP

### TCP (Transmission Control Protocol)
- Kết nối có thiết lập (connection-oriented)
- Đảm bảo thứ tự và độ tin cậy
- Chậm hơn nhưng an toàn hơn
- Phù hợp: Web, Email, File Transfer

### UDP (User Datagram Protocol)
- Không kết nối (connectionless)
- Không đảm bảo thứ tự và độ tin cậy
- Nhanh hơn nhưng có thể mất gói tin
- Phù hợp: Video streaming, Game online, DNS

## UDP Server

```java
import java.net.*;

public class UDPServer {
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket(8080);
            byte[] buffer = new byte[1024];
            
            System.out.println("UDP Server đang chờ dữ liệu...");
            
            while (true) {
                DatagramPacket packet = new DatagramPacket(
                    buffer, buffer.length
                );
                
                socket.receive(packet);
                
                String message = new String(
                    packet.getData(), 
                    0, 
                    packet.getLength()
                );
                
                System.out.println("Nhận được từ " + 
                    packet.getAddress() + ": " + message);
                
                // Gửi phản hồi
                String response = "Echo: " + message;
                byte[] responseData = response.getBytes();
                
                DatagramPacket responsePacket = new DatagramPacket(
                    responseData,
                    responseData.length,
                    packet.getAddress(),
                    packet.getPort()
                );
                
                socket.send(responsePacket);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## UDP Client

```java
import java.net.*;
import java.util.Scanner;

public class UDPClient {
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket();
            InetAddress serverAddress = InetAddress.getByName("localhost");
            
            Scanner scanner = new Scanner(System.in);
            
            while (true) {
                System.out.print("Nhập tin nhắn: ");
                String message = scanner.nextLine();
                
                if (message.equals("quit")) {
                    break;
                }
                
                byte[] sendData = message.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(
                    sendData,
                    sendData.length,
                    serverAddress,
                    8080
                );
                
                socket.send(sendPacket);
                
                // Nhận phản hồi
                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(
                    receiveData,
                    receiveData.length
                );
                
                socket.receive(receivePacket);
                
                String response = new String(
                    receivePacket.getData(),
                    0,
                    receivePacket.getLength()
                );
                
                System.out.println("Server phản hồi: " + response);
            }
            
            socket.close();
            scanner.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Broadcast với UDP

UDP cho phép gửi broadcast đến tất cả các máy trong mạng:

```java
import java.net.*;

public class UDPBroadcast {
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket();
            socket.setBroadcast(true);
            
            String message = "Hello từ broadcast!";
            byte[] data = message.getBytes();
            
            // Broadcast đến tất cả máy trong mạng local
            InetAddress broadcastAddress = 
                InetAddress.getByName("255.255.255.255");
            
            DatagramPacket packet = new DatagramPacket(
                data,
                data.length,
                broadcastAddress,
                8080
            );
            
            socket.send(packet);
            System.out.println("Đã gửi broadcast!");
            
            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Khi nào dùng UDP?

- **Game online**: Cần tốc độ, mất một vài gói tin không quan trọng
- **Video streaming**: Tốc độ quan trọng hơn độ chính xác
- **DNS queries**: Yêu cầu nhanh, đơn giản
- **IoT sensors**: Gửi dữ liệu cảm biến định kỳ

## Lưu ý

- UDP không đảm bảo gói tin đến đích
- Cần tự xử lý thứ tự và kiểm tra dữ liệu
- Phù hợp cho ứng dụng có thể chấp nhận mất mát dữ liệu

