package com.example.backendjava.entity;

import java.util.List;

public class Statistics {
    private float duration;
    private int totalPageCrawled;
    private int totalTerms;
    private int totalStems;


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

}
