package com.example.backendjava.entity;

import java.util.Date;
import java.util.List;

public class PageContent {
    private String url;
    private String title;
    private String[] words;
    private Date modifiedDate;
    private List<PageContentChildLink> childList;

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String[] getWords() {
        return words;
    }

    public void setWords(String[] words) {
        this.words = words;
    }

    public Date getModifiedDate() {
        return modifiedDate;
    }

    public void setModifiedDate(Date modifiedDate) {
        this.modifiedDate = modifiedDate;
    }

    public List<PageContentChildLink> getChildList() {
        return childList;
    }

    public void setChildList(List<PageContentChildLink> childList) {
        this.childList = childList;
    }

    @Override
    public String toString() {
        return "PageContent{" +
                "url='" + url + '\'' +
                ", title='" + title + '\'' +
                ", words=" + words +
                ", modifiedDate=" + modifiedDate +
                ", childList=" + childList +
                '}';
    }
}
