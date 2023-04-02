package com.example.backendjava.controller;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.service.CrawlService;
import org.htmlparser.lexer.Page;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/crawl")
public class CrawlController {

    private CrawlService crawlService;

    @Autowired
    public CrawlController(CrawlService crawlService) {
        this.crawlService = crawlService;
//        this.crawlService.startCrawling("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm");
    }

    @GetMapping("/remove")
    public String removeCrawled(){
        crawlService.removeCrawledContent();
        return "ok";
    }

    @GetMapping("/start")
    public String startCrawling(@RequestParam String url) {
        System.out.println("Start crawling");
        crawlService.startCrawling(url);
        System.out.println("Finish crawling");
        return "done";
    }

    @GetMapping("/count")
    public int getCrawledPageCount() {
        return crawlService.getCrawledContent().size();
    }

    @GetMapping("/")
    public List<PageContent> getCrawledContent() {
        if (crawlService.getCrawledContent() == null) {
            crawlService.startCrawling("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm");
        }
        return crawlService.getCrawledContent();
    }
}
