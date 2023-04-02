package com.example.backendjava.controller;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.service.CrawlService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/crawl")
public class CrawlController {

    private CrawlService crawlService;
    private List<PageContent> crawledContent;

    @Autowired
    public CrawlController(CrawlService crawlService) {
        this.crawlService = crawlService;
        this.crawledContent = null;
    }

    @GetMapping("/childLinks")
    public List<String> getFullUrlList(@RequestParam String url) {
        List<String> fullUrlList = crawlService.getFullUrlList(url);
        return fullUrlList;
    }

    @GetMapping("/single")
    public List<String> getSinglePageContent(@RequestParam String url) {
        List<String> fullUrlList = crawlService.getFullUrlList(url);
        return fullUrlList;
    }

    @GetMapping("/start")
    public String startCrawling(@RequestParam String url) {
        System.out.println("Start crawling");
        crawledContent = new ArrayList<>();
        List<String> fullUrlList = crawlService.getFullUrlList(url);

        for (String childUrl : fullUrlList) {
            crawledContent.add(crawlService.getPageContent(childUrl));
        }
        System.out.println("Finish crawling");
        return "done";

    }

    @GetMapping("/")
    public List<PageContent> getCrawledContent() {
        if (crawledContent == null) {
            crawledContent = new ArrayList<>();
            List<String> fullUrlList = crawlService.getFullUrlList("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm");

            for (String childUrl : fullUrlList) {
                crawledContent.add(crawlService.getPageContent(childUrl));
            }
        }
        return crawledContent;
    }
}
