package com.example.backendjava.service.utils;

public class StopWatch {
    
    private long startTime;
    private long stopTime;
    private float elapsedTime;
    
    public void start() {
        this.startTime = System.currentTimeMillis();
    }
    
    public void stop() {
        this.stopTime = System.currentTimeMillis();
        this.elapsedTime = (stopTime - startTime)/1000F;
    }
    
    public float getElapsedTimeInSecond() {
        
        return this.elapsedTime;
    }
    
    public void printElapseTimeInSecond() {
        System.out.println("(" + this.elapsedTime + " seconds)");
    }
    
    public void printOverallElapseTimeInSecond() {
        System.out.println("\n[Overall Duration: " + this.elapsedTime + " seconds]");
    }

    public static void main(String[] args) {
        
        try {
            
            StopWatch sw = new StopWatch();
            sw.start();
            Thread.sleep(6355);
            sw.stop();
            sw.printElapseTimeInSecond();
            
            
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

}
