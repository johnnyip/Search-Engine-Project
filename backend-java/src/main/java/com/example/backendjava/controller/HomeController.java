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

    @PostMapping("/receive")
    public void receive(@RequestBody List<PageContent> body){
        System.out.println("Received: ");
        for(PageContent content: body){
            System.out.println(content);
        }

    }
    @GetMapping("/send")
    public void test() {
        try {
            URL url = new URL("http://localhost:5000/");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Set the request method (GET is the default)
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            connection.setRequestProperty("Accept", "application/json");
            connection.setDoOutput(true);

            ArrayList<PageContent> data = new ArrayList<>();
            data.add(new PageContent("title1"));
            data.add(new PageContent("title2"));


            // Convert the ArrayList to a JSON string
            Gson gson = new Gson();
            String jsonBody = gson.toJson(data);

            OutputStream outputStream = connection.getOutputStream();
            outputStream.write(jsonBody.getBytes("UTF-8"));
            outputStream.close();
            System.out.println("Sent: ");
            System.out.println(jsonBody);
            System.out.println();

            // Get the response code
            int responseCode = connection.getResponseCode();
//            System.out.println("Response Code: " + responseCode);

            // Read the response
            BufferedReader inputReader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder content = new StringBuilder();
            while ((inputLine = inputReader.readLine()) != null) {
                content.append(inputLine);
            }

            // Close the connections
            inputReader.close();
            connection.disconnect();

            // Print the response content
//            System.out.println("Response Content: " + content.toString());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }

    }
}
