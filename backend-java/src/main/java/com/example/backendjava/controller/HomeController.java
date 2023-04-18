package com.example.backendjava.controller;

import com.example.backendjava.entity.PageContent;
import com.google.gson.Gson;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("")
public class HomeController {

    @GetMapping("/")
    public String Home() {
        return "Hello World";
    }


}
