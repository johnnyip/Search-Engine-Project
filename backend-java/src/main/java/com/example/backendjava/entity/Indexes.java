package com.example.backendjava.entity;

import java.util.List;

public class Indexes {
    private List<MaxTF> maxTFList;
    private List<TermFrequency> stemFrequencies;
    private List<TermFrequency> rawFrequencies;

    public List<MaxTF> getMaxTFList() {
        return maxTFList;
    }

    public void setMaxTFList(List<MaxTF> maxTFList) {
        this.maxTFList = maxTFList;
    }

    public List<TermFrequency> getStemFrequencies() {
        return stemFrequencies;
    }

    public void setStemFrequencies(List<TermFrequency> stemFrequencies) {
        this.stemFrequencies = stemFrequencies;
    }

    public List<TermFrequency> getRawFrequencies() {
        return rawFrequencies;
    }

    public void setRawFrequencies(List<TermFrequency> rawFrequencies) {
        this.rawFrequencies = rawFrequencies;
    }
}
