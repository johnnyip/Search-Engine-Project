package com.example.backendjava.service;

import com.example.backendjava.service.core.Indexer;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;


@Service
public class CrawlService {

    @Transactional
    public void start(){
        Indexer idxr = new Indexer();
        idxr.reBuildAllIndexes();
    }

    @Transactional
    public void remove() throws IOException {
        Path sourceFile = Paths.get("db_init/", "csit5930");
        Path destinationFile = Paths.get("db/", "csit5930");

        // Copy the file from sourceFolder to destinationFolder, replacing it if it exists
        Files.copy(sourceFile, destinationFile, StandardCopyOption.REPLACE_EXISTING);

    }
}
