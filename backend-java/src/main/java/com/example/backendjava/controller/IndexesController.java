package com.example.backendjava.controller;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.service.CrawlService;
import com.example.backendjava.service.URLIndexService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/index")
public class IndexesController {

    private CrawlService crawlService;
    private URLIndexService urlIndexService;

    public IndexesController(CrawlService crawlService, URLIndexService urlIndexService) {
        this.crawlService = crawlService;
        this.urlIndexService = urlIndexService;
    }

    @GetMapping("/url_forward")
    public Map<String, List<String>> getURLForwardIndex() {
        return urlIndexService.getUrlForwardIndex(crawlService.getCrawledContent());
    }

    @GetMapping("/url_inverted")
    public Map<String, List<String>> getURLInvertedIndex() {
        return urlIndexService.getUrlInvertedIndex(crawlService.getCrawledContent());
    }

}
