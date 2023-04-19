package com.example.backendjava.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("")
public class HomeController {

    @GetMapping("/")
    public String Home() {
        return "Hello World";
    }


}
