package com.example.backendjava.controller;

import com.example.backendjava.entity.Indexes;
import com.example.backendjava.entity.Statistics;
import com.example.backendjava.service.CrawlService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/crawl")
public class CrawlController {

    private CrawlService crawlService;

    public CrawlController(CrawlService crawlService) {
        this.crawlService = crawlService;
    }

    @GetMapping("/remove")
    public Statistics removeCrawled() throws IOException {
        crawlService.remove();
        return crawlService.getStatistics();
    }

    @GetMapping("/start")
    @Transactional(timeout = 1000)
    public Statistics startCrawling() throws IOException {
        System.out.println("Start crawling and build index");
        crawlService.start();
        System.out.println("Finish crawling and build index");
//        crawlService.outputDB();

        return crawlService.getStatistics();
    }

    @GetMapping("/update")
    @Transactional(timeout = 1000)
    public Statistics startUpdate() throws IOException {
        System.out.println("Start crawling and update index");
        crawlService.update();
        System.out.println("Finish crawling and update index");
//        crawlService.outputDB();

        return crawlService.getStatistics();
    }

    @GetMapping("/stat")
    public Statistics getStat(){
        return crawlService.getStatistics();
    }

    @GetMapping("/index")
    public Indexes getIndexes(){
        return crawlService.getIndexesContent();
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
