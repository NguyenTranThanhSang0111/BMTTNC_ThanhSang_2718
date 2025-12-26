---
title: "Bài 5: HTTP Client với Java"
date: 2024-12-28
draft: false
weight: 5
categories: ["Java"]
tags: ["java", "http", "client", "api"]
description: "Học cách sử dụng HTTP Client trong Java để gọi REST API"
featuredImage: "images/bai-5-http-client.jpg"
featuredImagePreview: "images/bai-5-http-client.jpg"
images: ["images/bai-5-http-client.jpg"]
---

## HTTP Client trong Java

Java cung cấp nhiều cách để tạo HTTP request:
- `HttpURLConnection` (từ Java 1.1)
- `HttpClient` (từ Java 11) - Khuyến nghị sử dụng
- Thư viện bên thứ ba: Apache HttpClient, OkHttp

## Sử dụng HttpClient (Java 11+)

`HttpClient` là API hiện đại, dễ sử dụng và hỗ trợ HTTP/2.

### GET Request

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class HTTPClientExample {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.github.com/users/octocat"))
            .GET()
            .build();
        
        try {
            HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
            );
            
            System.out.println("Status Code: " + response.statusCode());
            System.out.println("Response Body: " + response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### POST Request với JSON

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class HTTPPostExample {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        
        String jsonBody = """
            {
                "name": "Nguyễn Văn A",
                "email": "nguyenvana@example.com"
            }
            """;
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/users"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
            .build();
        
        try {
            HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
            );
            
            System.out.println("Status: " + response.statusCode());
            System.out.println("Response: " + response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Async Request

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.util.concurrent.CompletableFuture;

public class AsyncHTTPClient {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/data"))
            .GET()
            .build();
        
        CompletableFuture<HttpResponse<String>> future = 
            client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
        
        future.thenApply(HttpResponse::body)
              .thenAccept(System.out::println)
              .join();
    }
}
```

## Xử lý JSON với Jackson

Để làm việc với JSON dễ dàng hơn, sử dụng thư viện Jackson:

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class JSONClient {
    private static final ObjectMapper mapper = new ObjectMapper();
    
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/user/1"))
            .GET()
            .build();
        
        try {
            HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
            );
            
            // Parse JSON thành object
            User user = mapper.readValue(response.body(), User.class);
            System.out.println("User: " + user.getName());
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class User {
    private String name;
    private String email;
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

## Xử lý lỗi và timeout

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.time.Duration;

public class HTTPClientWithTimeout {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .build();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/data"))
            .timeout(Duration.ofSeconds(5))
            .GET()
            .build();
        
        try {
            HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
            );
            
            if (response.statusCode() == 200) {
                System.out.println("Success: " + response.body());
            } else {
                System.err.println("Error: " + response.statusCode());
            }
        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
    }
}
```

## Thực hành

Hãy thử tạo một ứng dụng Java gọi API thời tiết hoặc API công khai khác!

