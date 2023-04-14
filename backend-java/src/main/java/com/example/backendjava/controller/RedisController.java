package com.example.backendjava.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/redis")
public class RedisController {

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @PostMapping("/save")
    public String save(@RequestParam String id, @RequestBody String data) {
        System.out.println(data);
        redisTemplate.opsForValue().set(id, data);
        return "saved";
    }

    @GetMapping("/get")
    public String get(@RequestParam String id) {
        String value = redisTemplate.opsForValue().get(id);
        return (value != null) ? value:"[]";
    }

}
