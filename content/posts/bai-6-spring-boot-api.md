---
title: "Bài 6: Xây dựng Web API với Spring Boot"
date: 2024-12-29
draft: false
weight: 6
categories: ["Java"]
tags: ["java", "spring boot", "rest api", "web"]
description: "Học cách tạo RESTful API với Spring Boot framework"
featuredImage: "images/bai-6-spring-boot-api.jpg"
featuredImagePreview: "images/bai-6-spring-boot-api.jpg"
images: ["images/bai-6-spring-boot-api.jpg"]
---

## Spring Boot là gì?

Spring Boot là framework Java giúp tạo ứng dụng độc lập, production-ready một cách nhanh chóng. Nó tự động cấu hình và giảm thiểu boilerplate code.

## Tạo Spring Boot Project

### Sử dụng Spring Initializr

1. Truy cập https://start.spring.io/
2. Chọn dependencies: Spring Web, Spring Data JPA
3. Generate và tải project

### Cấu trúc Project

```
src/
  main/
    java/
      com/example/demo/
        DemoApplication.java
        controller/
          UserController.java
        model/
          User.java
        repository/
          UserRepository.java
    resources/
      application.properties
```

## Tạo REST Controller

```java
package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private List<User> users = new ArrayList<>();
    
    // GET - Lấy tất cả users
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(users);
    }
    
    // GET - Lấy user theo ID
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        User user = users.stream()
            .filter(u -> u.getId().equals(id))
            .findFirst()
            .orElse(null);
        
        if (user != null) {
            return ResponseEntity.ok(user);
        }
        return ResponseEntity.notFound().build();
    }
    
    // POST - Tạo user mới
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        user.setId((long) (users.size() + 1));
        users.add(user);
        return ResponseEntity.status(201).body(user);
    }
    
    // PUT - Cập nhật user
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(
            @PathVariable Long id, 
            @RequestBody User updatedUser) {
        
        for (int i = 0; i < users.size(); i++) {
            if (users.get(i).getId().equals(id)) {
                updatedUser.setId(id);
                users.set(i, updatedUser);
                return ResponseEntity.ok(updatedUser);
            }
        }
        return ResponseEntity.notFound().build();
    }
    
    // DELETE - Xóa user
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        users.removeIf(u -> u.getId().equals(id));
        return ResponseEntity.noContent().build();
    }
}
```

## Model Class

```java
package com.example.demo.model;

public class User {
    private Long id;
    private String name;
    private String email;
    
    // Constructors
    public User() {}
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

## Cấu hình Application

```properties
# application.properties
server.port=8080
spring.application.name=my-api

# CORS Configuration
spring.web.cors.allowed-origins=*
spring.web.cors.allowed-methods=GET,POST,PUT,DELETE
```

## Xử lý Exception

```java
package com.example.demo.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
            ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
}

class ErrorResponse {
    private int status;
    private String message;
    
    public ErrorResponse(int status, String message) {
        this.status = status;
        this.message = message;
    }
    
    // Getters
    public int getStatus() { return status; }
    public String getMessage() { return message; }
}
```

## Chạy ứng dụng

```bash
# Build project
./mvnw clean install

# Chạy ứng dụng
./mvnw spring-boot:run
```

Ứng dụng sẽ chạy tại: `http://localhost:8080`

## Test API với cURL

```bash
# GET all users
curl http://localhost:8080/api/users

# POST new user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Nguyễn Văn A","email":"a@example.com"}'

# GET user by ID
curl http://localhost:8080/api/users/1

# DELETE user
curl -X DELETE http://localhost:8080/api/users/1
```

## Kết luận

Spring Boot giúp tạo REST API nhanh chóng và dễ dàng. Đây là nền tảng quan trọng cho phát triển ứng dụng web hiện đại.

