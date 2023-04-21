package com.example.backendjava.entity;

import java.util.List;

public class Statistics {
    private float buildDuration;
    private float updateDuration;
    private int totalPageCrawled;
    private int totalTerms;
    private int totalStems;

    public Statistics(boolean fake) {
        if (fake) {
            this.buildDuration = 101.775F;
            this.updateDuration = 13.728F;
        }
    }

    public float getBuildDuration() {
        return buildDuration;
    }

    public void setBuildDuration(float buildDuration) {
        this.buildDuration = buildDuration;
    }

    public float getUpdateDuration() {
        return updateDuration;
    }

    public void setUpdateDuration(float updateDuration) {
        this.updateDuration = updateDuration;
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
