package com.example.backendjava.entity;

import java.util.List;
import java.util.Map;

public class Indexes {
    private List<MaxTF> maxTFList;
    private List<TermFrequency> stemFrequencies;
    private List<TermFrequency> rawFrequencies;
    private Map<String, String> rawContentMap;

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

    public Map<String, String> getRawContentMap() {
        return rawContentMap;
    }

    public void setRawContentMap(Map<String, String> rawContentMap) {
        this.rawContentMap = rawContentMap;
    }
}
