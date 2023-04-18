package com.example.backendjava.controller;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.service.CrawlService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/crawl")
public class CrawlController {

    @Autowired
    private CrawlService crawlService;


    @GetMapping("/remove")
    public String removeCrawled() throws IOException {
        crawlService.remove();
        return "ok";
    }

    @GetMapping("/start")
    public String startCrawling() {
        System.out.println("Start crawling");
        crawlService.start();
        System.out.println("Finish crawling");

        return "done";
    }

//    @GetMapping("/count")
//    public int getCrawledPageCount() {
//        if (crawlService.getCrawledContent() != null) {
//            return crawlService.getCrawledContent().size();
//        }
//        return 0;
//    }
//
//    @GetMapping("/")
//    public List<PageContent> getCrawledContent() {
//        if (crawlService.getCrawledContent() == null) {
//            crawlService.startCrawling("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm");
//        }
//        return crawlService.getCrawledContent();
//    }
}
