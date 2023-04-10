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

    private List<String> urlWithLastModifiedDate = null;
    public List<PageContent> getCrawledContent() {
        return crawledContent;
    }

    public List<String> getUrlWithLastModifiedDate() {
        return urlWithLastModifiedDate;
    }

    public void removeCrawledContent() {
        crawledContent = new ArrayList<>();
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

//        crawQueue.add("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm, Thu Jun 16 16:47:33 HKT 2022");
//        crawQueue_tmp.add("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm, Thu Jun 16 16:47:33 HKT 2022");
//        fullURLList.add("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm, Thu Jun 16 16:47:33 HKT 2022");

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
        urlWithLastModifiedDate = new ArrayList<>();
        List<String> fullUrlList = getFullUrlList(url);

        System.out.println("URLs found: " + fullUrlList.size());
        for (String childUrl : fullUrlList) {
            PageContent pageContent = getPageContent(childUrl);
            crawledContent.add(pageContent);
            urlWithLastModifiedDate.add(childUrl+", "+pageContent.getModifiedDate());
        }
    }
}
