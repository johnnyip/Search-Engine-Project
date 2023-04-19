package com.example.backendjava.service;

import com.example.backendjava.entity.Statistics;
import com.example.backendjava.service.core.Indexer;
import com.example.backendjava.service.core.SearchEngine;
import com.example.backendjava.service.utils.StopWatch;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;


@Service
public class CrawlService {
    private StopWatch timer;
    private Statistics statistics;

    public CrawlService() {
        this.timer = new StopWatch();
        this.statistics = new Statistics();
    }

    public Statistics getStatistics() {
        return statistics;
    }

    @Transactional
    public void start() {
        timer.start();
        Indexer idxr = new Indexer();
        idxr.reBuildAllIndexes();

        timer.stop();
        statistics.setDuration(timer.getElapsedTimeInSecond());
        statistics.setTotalPageCrawled(SearchEngine.getFullUrlList(false).size());

    }

    @Transactional
    public void remove() throws IOException {
        Path sourceFile = Paths.get("db_init/", "csit5930");
        Path destinationFile = Paths.get("db/", "csit5930");

        // Copy the file from sourceFolder to destinationFolder, replacing it if it exists
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);

        //Reset stat
        statistics = new Statistics();
    }
}
