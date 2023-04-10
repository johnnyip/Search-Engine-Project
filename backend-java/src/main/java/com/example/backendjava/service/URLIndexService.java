package com.example.backendjava.service;

import com.example.backendjava.entity.PageContent;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class URLIndexService {

    public Map<String, List<String>> getUrlInvertedIndex(List<PageContent> pageContents) {
        Map<String, List<String>> indexMap = new HashMap<>();

        for (PageContent pageContent : pageContents) {
            List<String> childURL = new ArrayList<>();
            for (PageContent child : pageContent.getChildList()) {
                childURL.add(child.getUrl());
            }
            indexMap.put(pageContent.getUrl(), childURL);
        }

        return indexMap;
    }

    public Map<String, List<String>> getUrlForwardIndex(List<PageContent> pageContents) {
        Map<String, List<String>> indexMap = new HashMap<>();

        for (PageContent pageContent : pageContents) {
            for (PageContent child : pageContent.getChildList()) {
                List<String> indexOfChild = indexMap.get(child.getUrl());

                //init if not indexed yet
                if (indexOfChild == null) {
                    indexOfChild = new ArrayList<>();
                }
                //Add current page as parent, to child key
                indexOfChild.add(pageContent.getUrl());

                indexMap.put(child.getUrl(),indexOfChild);
            }
        }

        return indexMap;
    }


}
