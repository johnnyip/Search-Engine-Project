package com.example.backendjava.service;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.service.function.LinkExtractor;
import com.example.backendjava.service.function.StringExtractor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class CrawlService {

    private List<PageContent> crawledContent = null;

    public List<PageContent> getCrawledContent() {
        return crawledContent;
    }

    public void setCrawledContent(List<PageContent> crawledContent) {
        this.crawledContent = crawledContent;
    }

    public List<String> getFullUrlList(String baseUrl) {
        ArrayList<String> fullURLList = new ArrayList<>();
        ArrayList<String> crawQueue = new ArrayList<>();
        ArrayList<String> crawQueue_tmp = new ArrayList<>(); //not remove

        LinkExtractor le = new LinkExtractor();
        List<String> allLinks = le.getAllLinks(baseUrl);

        crawQueue.addAll(allLinks);
        crawQueue_tmp.addAll(allLinks);
        fullURLList.addAll(allLinks);

        while (!crawQueue.isEmpty()) {
            for (String url : crawQueue_tmp) {
                List<String> allLinks_ = le.getAllLinks(url);

                for (String url_ : allLinks_) {
                    if (!fullURLList.contains(url_)) {
                        crawQueue.add(url_);
                        fullURLList.add(url_);
                    }
                }

                crawQueue.remove(url);
            }
            crawQueue_tmp = new ArrayList<>(crawQueue);
        }

        return fullURLList;
    }

    public PageContent getPageContent(String url) {
        StringExtractor stringExtractor = new StringExtractor();
        return stringExtractor.getPageContent(url);
    }

    public void startCrawling(String url) {
        crawledContent = new ArrayList<>();
        List<String> fullUrlList = getFullUrlList(url);

        System.out.println("URLs found: "+fullUrlList.size());
        for (String childUrl : fullUrlList) {
            crawledContent.add(getPageContent(childUrl));
        }
    }
}
