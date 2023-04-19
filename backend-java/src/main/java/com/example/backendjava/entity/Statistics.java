package com.example.backendjava.entity;

import java.util.List;

public class Statistics {
    private float duration;
    private int totalPageCrawled;
    private int totalTerms;
    private int totalStems;
    private List<MaxTF> maxTFList;
    private List<StemFrequency> stemFrequencies;


    public float getDuration() {
        return duration;
    }

    public void setDuration(float duration) {
        this.duration = duration;
    }

    public int getTotalPageCrawled() {
        return totalPageCrawled;
    }

    public void setTotalPageCrawled(int totalPageCrawled) {
        this.totalPageCrawled = totalPageCrawled;
    }

    public int getTotalTerms() {
        return totalTerms;
    }

    public void setTotalTerms(int totalTerms) {
        this.totalTerms = totalTerms;
    }

    public int getTotalStems() {
        return totalStems;
    }

    public void setTotalStems(int totalStems) {
        this.totalStems = totalStems;
    }

    public List<MaxTF> getMaxTFList() {
        return maxTFList;
    }

    public void setMaxTFList(List<MaxTF> maxTFList) {
        this.maxTFList = maxTFList;
    }

    public List<StemFrequency> getStemFrequencies() {
        return stemFrequencies;
    }

    public void setStemFrequencies(List<StemFrequency> stemFrequencies) {
        this.stemFrequencies = stemFrequencies;
    }
}
