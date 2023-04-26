package com.example.backendjava.service;

import com.example.backendjava.entity.Indexes;
import com.example.backendjava.entity.Statistics;
import com.example.backendjava.service.core.Indexer;
import com.example.backendjava.service.core.SearchEngine;
import com.example.backendjava.service.utils.StopWatch;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;


@Service
public class CrawlService {
    private StopWatch buildTimer;
    private StopWatch updateTimer;
    private Statistics statistics;
    private Indexes indexes;
    private boolean crawled;

    public CrawlService() {
        this.buildTimer = new StopWatch();
        this.updateTimer = new StopWatch();
        this.statistics = new Statistics(true);
        this.indexes = new Indexes();
        this.crawled = false;
    }

    public Statistics getStatistics() {
//        statistics.setDuration(timer.getElapsedTimeInSecond());
        if (crawled) {
            statistics.setBuildDuration(buildTimer.getElapsedTimeInSecond());
            statistics.setUpdateDuration(updateTimer.getElapsedTimeInSecond());
        }
        statistics.setTotalPageCrawled(SearchEngine.getFullUrlList(false).size());
        statistics.setTotalTerms(SearchEngine.getTerms());
        statistics.setTotalStems(SearchEngine.getStem());
        return statistics;
    }

    public Indexes getIndexesContent() {
        indexes.setMaxTFList(SearchEngine.getTitleMaxTF());
        indexes.setStemFrequencies(SearchEngine.getStemFrequency());
        indexes.setRawFrequencies(SearchEngine.getRawFrequency());
        indexes.setRawContentMap(SearchEngine.getRawContent());
        return indexes;
    }

    @Transactional
    public void start() {
        buildTimer.start();
        Indexer idxr = new Indexer();
        idxr.reBuildAllIndexes();

        buildTimer.stop();
    }

    @Transactional
    public void restore() throws IOException {
        //File remove, prevent .journal file exist in the folder

        File folder = new File("db/");
        if (folder.exists() && folder.isDirectory()) {
            File[] files = folder.listFiles();
            if (files != null) {
                for (File file : files) {
                    if (file.isFile()) {
                        file.delete();
                    }
                }
            }
        }


        Path sourceFile = Paths.get("db_init/", "csit5930_full");
        Path destinationFile = Paths.get("db/", "csit5930");

        // Copy the file from sourceFolder to destinationFolder, replacing it if it exists
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);


    }

    @Transactional
    public void update() {
        updateTimer.start();
        Indexer idxr = new Indexer();
        idxr.checkAndUpdateIndex();

        updateTimer.stop();
    }

    @Transactional
    public void outputDB() throws IOException {
        Path sourceFile = Paths.get("db/", "csit5930");
        Path destinationFile = Paths.get("db_output/", "csit5930");

        // Copy the file from sourceFolder to destinationFolder, replacing it if it exists
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);
    }

    @Transactional
    public void remove() throws IOException {
        Path sourceFile = Paths.get("db_init/", "csit5930");
        Path destinationFile = Paths.get("db/", "csit5930");

        // Copy the file from sourceFolder to destinationFolder, replacing it if it exists
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);

        //Reset stat
        statistics = new Statistics(false);
    }
}
