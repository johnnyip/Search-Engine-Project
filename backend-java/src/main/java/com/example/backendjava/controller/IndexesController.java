package com.example.backendjava.controller;

import com.example.backendjava.service.CrawlService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/index")
public class IndexesController {
    private CrawlService crawlService;

    public IndexesController(CrawlService crawlService) {
        this.crawlService = crawlService;
    }

    //    @GetMapping("/url_forward")
//    public Map<String, List<String>> getURLForwardIndex() {
//        return urlIndexService.getUrlForwardIndex(crawlService.getCrawledContent());
//    }
//
//    @GetMapping("/url_inverted")
//    public Map<String, List<String>> getURLInvertedIndex() {
//        return urlIndexService.getUrlInvertedIndex(crawlService.getCrawledContent());
//    }

}
