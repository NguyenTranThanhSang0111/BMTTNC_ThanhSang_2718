---
title: "Bài 7: RESTful API - Best Practices"
date: 2024-12-30
draft: false
weight: 7
categories: ["Java"]
tags: ["java", "rest", "api", "best practices"]
description: "Tìm hiểu các nguyên tắc và best practices khi thiết kế RESTful API"
featuredImage: "/images/bai-7-restful-api.jpg"
featuredImagePreview: "/images/bai-7-restful-api.jpg"
images: ["/images/bai-7-restful-api.jpg"]
---

## REST là gì?

REST (Representational State Transfer) là kiến trúc phần mềm để thiết kế web services. RESTful API sử dụng các phương thức HTTP chuẩn để thao tác với tài nguyên.

## Nguyên tắc REST

### 1. Resource-Based URLs

URLs nên đại diện cho tài nguyên, không phải hành động:

```
✅ Tốt:
GET    /api/users
GET    /api/users/1
POST   /api/users
PUT    /api/users/1
DELETE /api/users/1

❌ Không tốt:
GET    /api/getUsers
POST   /api/createUser
POST   /api/updateUser?id=1
```

### 2. HTTP Methods

Sử dụng đúng phương thức HTTP:

- **GET**: Lấy dữ liệu (idempotent, safe)
- **POST**: Tạo mới tài nguyên
- **PUT**: Cập nhật toàn bộ tài nguyên (idempotent)
- **PATCH**: Cập nhật một phần tài nguyên
- **DELETE**: Xóa tài nguyên (idempotent)

### 3. HTTP Status Codes

Trả về đúng status code:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        
        if (user == null) {
            return ResponseEntity.notFound().build(); // 404
        }
        return ResponseEntity.ok(user); // 200
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.save(user);
        return ResponseEntity
            .status(HttpStatus.CREATED) // 201
            .body(created);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        if (userService.delete(id)) {
            return ResponseEntity.noContent().build(); // 204
        }
        return ResponseEntity.notFound().build(); // 404
    }
}
```

## Response Format chuẩn

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Nguyễn Văn A",
    "email": "a@example.com"
  }
}
```

### Error Response

```json
{
  "status": "error",
  "message": "User not found",
  "code": 404,
  "timestamp": "2024-12-30T10:00:00Z"
}
```

### Wrapper Class

```java
public class ApiResponse<T> {
    private String status;
    private T data;
    private String message;
    private int code;
    
    public static <T> ApiResponse<T> success(T data) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("success");
        response.setData(data);
        return response;
    }
    
    public static <T> ApiResponse<T> error(String message, int code) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("error");
        response.setMessage(message);
        response.setCode(code);
        return response;
    }
    
    // Getters and setters
}
```

## Pagination

Khi trả về danh sách lớn, sử dụng pagination:

```java
@GetMapping
public ResponseEntity<Page<User>> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {
    
    Pageable pageable = PageRequest.of(page, size);
    Page<User> users = userService.findAll(pageable);
    
    return ResponseEntity.ok(users);
}
```

Response:
```json
{
  "content": [...],
  "totalElements": 100,
  "totalPages": 10,
  "number": 0,
  "size": 10
}
```

## Filtering và Sorting

```java
@GetMapping
public ResponseEntity<List<User>> getUsers(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) String email,
        @RequestParam(defaultValue = "id") String sortBy,
        @RequestParam(defaultValue = "asc") String sortDir) {
    
    List<User> users = userService.findWithFilters(
        name, email, sortBy, sortDir
    );
    
    return ResponseEntity.ok(users);
}
```

URL: `/api/users?name=Nguyễn&sortBy=name&sortDir=desc`

## Versioning API

Có nhiều cách versioning:

### 1. URL Versioning
```
/api/v1/users
/api/v2/users
```

### 2. Header Versioning
```
Accept: application/vnd.api.v1+json
```

### 3. Query Parameter
```
/api/users?version=1
```

## Security Best Practices

1. **Authentication**: Sử dụng JWT hoặc OAuth2
2. **HTTPS**: Luôn sử dụng HTTPS trong production
3. **Rate Limiting**: Giới hạn số request
4. **Input Validation**: Validate tất cả input
5. **CORS**: Cấu hình CORS đúng cách

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
        // Chỉ admin mới tạo được user
    }
}
```

## Documentation

Sử dụng Swagger/OpenAPI để tạo documentation:

```java
@Configuration
public class SwaggerConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("User API")
                .version("1.0")
                .description("API quản lý người dùng"));
    }
}
```

## Kết luận

RESTful API tốt cần:
- URLs rõ ràng, nhất quán
- Sử dụng đúng HTTP methods và status codes
- Response format chuẩn
- Hỗ trợ pagination, filtering
- Bảo mật tốt
- Documentation đầy đủ

